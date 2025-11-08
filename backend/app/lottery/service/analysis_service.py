"""分析服务"""

import json

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.lottery.algorithm.combiner import combiner
from backend.app.lottery.crud import draw_result_dao, lottery_type_dao
from backend.common.exception import errors


class AnalysisService:
    """分析服务"""

    @staticmethod
    async def analyze_single_method(
        db: AsyncSession,
        lottery_code: str,
        method_code: str,
        history_periods: int = 100,
        params: dict | None = None,
    ) -> dict:
        """
        单个方法分析

        :param db: 数据库会话
        :param lottery_code: 彩种代码
        :param method_code: 方法代码
        :param history_periods: 历史期数
        :param params: 分析参数
        :return: 分析结果
        """
        # 获取彩票类型
        lottery_type = await lottery_type_dao.get_by_code(db, lottery_code)
        if not lottery_type:
            raise errors.NotFoundError(msg='彩种不存在')

        # 获取历史数据
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

        # 获取分析器
        analyzer_class = combiner.ANALYZER_MAP.get(method_code)
        if not analyzer_class:
            raise errors.NotFoundError(msg=f'分析方法 {method_code} 不存在')

        analyzer = analyzer_class(lottery_code)

        # 执行分析
        analysis_result = await analyzer.analyze(history_data_dict, params)

        # 执行预测
        prediction = await analyzer.predict(analysis_result, params)

        return {
            'lottery_code': lottery_code,
            'method_code': method_code,
            'history_periods': history_periods,
            'analysis_result': analysis_result,
            'prediction': prediction,
        }

    @staticmethod
    async def get_method_list() -> list[dict]:
        """
        获取所有可用的分析方法

        :return: 方法列表
        """
        methods = []
        for code, analyzer_class in combiner.ANALYZER_MAP.items():
            methods.append({
                'code': code,
                'name': analyzer_class.__name__.replace('Analyzer', ''),
                'description': analyzer_class.__doc__ or '',
            })
        return methods


analysis_service = AnalysisService()

