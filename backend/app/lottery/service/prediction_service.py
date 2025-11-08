"""预测服务"""

import json

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.lottery.algorithm.combiner import combiner
from backend.app.lottery.crud import (
    combination_dao,
    draw_result_dao,
    lottery_type_dao,
    method_dao,
    prediction_dao,
)
from backend.app.lottery.schema.prediction import AddPredictionParam
from backend.app.lottery.service.sync_service import sync_service
from backend.common.exception import errors
from backend.common.log import log


class PredictionService:
    """预测服务"""

    @staticmethod
    async def create_prediction(
        db: AsyncSession,
        lottery_code: str,
        combination_id: int | None,
        history_periods: int,
        user_id: int | None = None,
    ) -> dict:
        """
        创建预测

        :param db: 数据库会话
        :param lottery_code: 彩种代码
        :param combination_id: 组合ID
        :param history_periods: 历史期数
        :param user_id: 用户ID
        :return: 预测结果
        """
        # 获取彩票类型
        lottery_type = await lottery_type_dao.get_by_code(db, lottery_code)
        if not lottery_type:
            raise errors.NotFoundError(msg='彩种不存在')

        # 获取组合配置
        if combination_id:
            combination = await combination_dao.get(db, combination_id)
            if not combination:
                raise errors.NotFoundError(msg='组合不存在')
            
            method_configs = json.loads(combination.method_configs)
            history_periods = combination.history_periods
        else:
            # 使用默认配置（频率分析）
            method_configs = [
                {'code': 'frequency', 'weight': 1.0, 'params': {}},
            ]

        # 获取历史开奖数据
        history_data = await draw_result_dao.get_history_by_lottery(db, lottery_code, history_periods)
        if not history_data:
            raise errors.NotFoundError(msg='暂无历史开奖数据')

        # 转换为字典格式
        history_data_dict = []
        for draw in history_data:
            history_data_dict.append({
                'period': draw.period,
                'draw_date': str(draw.draw_date),
                'red_balls': draw.red_balls,
                'blue_balls': draw.blue_balls,
            })

        # 计算下期期号
        next_period = await sync_service.calculate_next_period(db, lottery_code)

        # 创建组合分析器
        analyzer = combiner(lottery_code)

        try:
            # 执行组合分析
            analysis_data = await analyzer.combine_methods(method_configs, history_data_dict, history_periods)

            # 生成分析文章
            lottery_info = {
                'name': lottery_type.name,
                'code': lottery_type.code,
            }
            article = await analyzer.generate_article(analysis_data, lottery_info, next_period)

            # 格式化号码
            combined_prediction = analysis_data.get('combined_prediction', {})
            formatted = await analyzer.format_numbers(lottery_code, combined_prediction)

            # 保存预测结果
            prediction_param = AddPredictionParam(
                lottery_code=lottery_code,
                target_period=next_period,
                combination_id=combination_id,
                method_details=json.dumps(analysis_data.get('method_predictions', []), ensure_ascii=False),
                predicted_numbers=json.dumps(formatted, ensure_ascii=False),
                analysis_article=article,
                confidence_score=combined_prediction.get('confidence', 0.5),
            )

            await prediction_dao.add(db, prediction_param, user_id)
            await db.commit()

            # 增加组合使用次数
            if combination_id:
                await combination_dao.increment_use_count(db, combination_id)
                await db.commit()

            return {
                'success': True,
                'lottery_code': lottery_code,
                'target_period': next_period,
                'predicted_numbers': formatted,
                'analysis_article': article,
                'confidence': combined_prediction.get('confidence', 0.5),
            }

        except Exception as e:
            log.error(f'预测失败: {e}')
            raise errors.ServerError(msg=f'预测失败: {str(e)}')

    @staticmethod
    async def verify_prediction(db: AsyncSession, prediction_id: int) -> dict:
        """
        验证预测结果

        :param db: 数据库会话
        :param prediction_id: 预测ID
        :return: 验证结果
        """
        # 获取预测记录
        prediction = await prediction_dao.get(db, prediction_id)
        if not prediction:
            raise errors.NotFoundError(msg='预测记录不存在')

        # 获取实际开奖结果
        actual_draw = await draw_result_dao.get_by_lottery_and_period(
            db, prediction.lottery_code, prediction.target_period
        )
        if not actual_draw:
            return {
                'success': False,
                'msg': '实际开奖结果尚未公布',
            }

        # 解析预测号码和实际号码
        predicted_numbers = json.loads(prediction.predicted_numbers)
        actual_red = json.loads(actual_draw.red_balls)
        actual_blue = json.loads(actual_draw.blue_balls) if actual_draw.blue_balls else None

        # 计算命中数（使用第一注单式）
        formatted_numbers = predicted_numbers.get('formatted_numbers', [])
        if not formatted_numbers:
            return {'success': False, 'msg': '预测号码格式错误'}

        # 找到单式号码
        single_bet = None
        for bet in formatted_numbers:
            if bet.get('type') == '单式':
                single_bet = bet
                break

        if not single_bet:
            single_bet = formatted_numbers[0]

        predicted_red = single_bet.get('red_balls', single_bet.get('numbers', []))
        predicted_blue = single_bet.get('blue_balls')

        # 计算红球命中数
        red_hits = len(set(predicted_red) & set(actual_red))

        # 计算蓝球命中数
        blue_hits = 0
        if predicted_blue and actual_blue:
            blue_hits = len(set(predicted_blue) & set(actual_blue))

        total_hits = red_hits + blue_hits

        # 更新预测记录
        from backend.app.lottery.schema.prediction import UpdatePredictionParam
        from backend.utils.timezone import timezone

        update_param = UpdatePredictionParam(
            actual_result=json.dumps({'red_balls': actual_red, 'blue_balls': actual_blue}, ensure_ascii=False),
            hit_count=total_hits,
            is_verified=True,
        )

        await prediction_dao.update(db, prediction_id, update_param)
        await db.commit()

        # 更新组合准确率（如果有组合）
        if prediction.combination_id:
            await PredictionService._update_combination_accuracy(db, prediction.combination_id)

        return {
            'success': True,
            'prediction_id': prediction_id,
            'red_hits': red_hits,
            'blue_hits': blue_hits,
            'total_hits': total_hits,
            'predicted': {'red': predicted_red, 'blue': predicted_blue},
            'actual': {'red': actual_red, 'blue': actual_blue},
        }

    @staticmethod
    async def _update_combination_accuracy(db: AsyncSession, combination_id: int) -> None:
        """
        更新组合准确率

        :param db: 数据库会话
        :param combination_id: 组合ID
        """
        try:
            # 获取该组合的所有已验证预测
            from sqlalchemy import select
            from backend.app.lottery.model import PredictionResult

            stmt = select(PredictionResult).where(
                PredictionResult.combination_id == combination_id,
                PredictionResult.is_verified == True  # noqa: E712
            )
            result = await db.execute(stmt)
            predictions = result.scalars().all()

            if not predictions:
                return

            # 计算平均命中率
            total_hits = sum(p.hit_count or 0 for p in predictions)
            total_possible = len(predictions) * 6  # 假设平均每注6个号码
            accuracy_rate = total_hits / total_possible if total_possible > 0 else 0

            # 更新组合准确率
            await combination_dao.update_accuracy_rate(db, combination_id, accuracy_rate)
            await db.commit()

        except Exception as e:
            log.error(f'更新组合准确率失败: {e}')


prediction_service = PredictionService()

