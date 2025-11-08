"""预测相关Celery任务"""

from sqlalchemy import select

from backend.app.lottery.crud import combination_dao, lottery_type_dao, prediction_dao
from backend.app.lottery.service.prediction_service import prediction_service
from backend.app.task.celery import celery_app
from backend.database.db import async_db_session
from backend.common.log import log


@celery_app.task(name='lottery.daily_auto_prediction')
async def daily_auto_prediction():
    """
    每日自动预测任务
    
    执行时间: 每天09:00
    功能: 对所有启用自动预测的组合生成预测
    """
    log.info('开始执行每日自动预测...')
    results = []
    
    async with async_db_session() as db:
        # 获取所有启用自动预测的组合
        from backend.app.lottery.model import AnalysisCombination
        stmt = select(AnalysisCombination).where(
            AnalysisCombination.is_auto == True,  # noqa: E712
            AnalysisCombination.status == 1
        )
        result = await db.execute(stmt)
        auto_combinations = result.scalars().all()
        
        log.info(f'找到 {len(auto_combinations)} 个自动预测组合')
        
        for combination in auto_combinations:
            try:
                log.info(f'执行组合预测: {combination.name} ({combination.lottery_code})')
                
                # 创建预测
                prediction_result = await prediction_service.create_prediction(
                    db=db,
                    lottery_code=combination.lottery_code,
                    combination_id=combination.id,
                    history_periods=combination.history_periods,
                    user_id=combination.user_id if combination.user_id != 0 else None,
                )
                
                results.append({
                    'success': True,
                    'combination_id': combination.id,
                    'combination_name': combination.name,
                    'lottery_code': combination.lottery_code,
                    'target_period': prediction_result.get('target_period'),
                })
                
                log.info(f'预测完成: {combination.name}')
                
            except Exception as e:
                log.error(f'预测失败 {combination.name}: {e}')
                results.append({
                    'success': False,
                    'combination_id': combination.id,
                    'combination_name': combination.name,
                    'error': str(e),
                })
    
    log.info(f'每日自动预测完成，共处理 {len(results)} 个组合')
    return {
        'total': len(results),
        'success': sum(1 for r in results if r['success']),
        'failed': sum(1 for r in results if not r['success']),
        'results': results,
    }


@celery_app.task(name='lottery.verify_predictions')
async def verify_predictions():
    """
    验证预测结果任务
    
    执行时间: 每天22:00
    功能: 验证所有未验证的预测结果
    """
    log.info('开始验证预测结果...')
    results = []
    
    async with async_db_session() as db:
        # 获取所有未验证的预测
        from backend.app.lottery.model import PredictionResult
        stmt = select(PredictionResult).where(
            PredictionResult.is_verified == False  # noqa: E712
        ).order_by(PredictionResult.created_time.desc()).limit(100)
        
        result = await db.execute(stmt)
        unverified_predictions = result.scalars().all()
        
        log.info(f'找到 {len(unverified_predictions)} 个待验证预测')
        
        for prediction in unverified_predictions:
            try:
                log.info(f'验证预测: {prediction.lottery_code} {prediction.target_period}')
                
                # 执行验证
                verify_result = await prediction_service.verify_prediction(db, prediction.id)
                
                if verify_result.get('success'):
                    results.append({
                        'success': True,
                        'prediction_id': prediction.id,
                        'lottery_code': prediction.lottery_code,
                        'target_period': prediction.target_period,
                        'hit_count': verify_result.get('total_hits'),
                    })
                    log.info(f'验证成功: 命中 {verify_result.get("total_hits")} 个')
                else:
                    # 开奖结果尚未公布
                    log.info(f'跳过验证: {verify_result.get("msg")}')
                    
            except Exception as e:
                log.error(f'验证失败 {prediction.id}: {e}')
                results.append({
                    'success': False,
                    'prediction_id': prediction.id,
                    'error': str(e),
                })
    
    log.info(f'预测验证完成，共处理 {len(results)} 个预测')
    return {
        'total': len(results),
        'verified': sum(1 for r in results if r['success']),
        'failed': sum(1 for r in results if not r['success']),
        'results': results,
    }


@celery_app.task(name='lottery.reset_daily_quota')
async def reset_daily_quota():
    """
    重置每日配额任务
    
    执行时间: 每天00:00
    功能: 重置所有会员的每日预测次数和API配额
    """
    log.info('开始重置每日配额...')
    
    from backend.app.lottery.service.membership_service import membership_service
    
    async with async_db_session() as db:
        result = await membership_service.reset_daily_quota(db)
        log.info(f'每日配额重置完成: {result}')
        return result


@celery_app.task(name='lottery.calculate_combination_accuracy')
async def calculate_combination_accuracy():
    """
    计算组合准确率任务
    
    执行时间: 每天23:00
    功能: 重新计算所有组合的准确率
    """
    log.info('开始计算组合准确率...')
    updated_count = 0
    
    async with async_db_session() as db:
        # 获取所有组合
        from backend.app.lottery.model import AnalysisCombination
        stmt = select(AnalysisCombination).where(AnalysisCombination.status == 1)
        result = await db.execute(stmt)
        combinations = result.scalars().all()
        
        for combination in combinations:
            try:
                # 更新准确率
                await prediction_service._update_combination_accuracy(db, combination.id)
                updated_count += 1
            except Exception as e:
                log.error(f'更新组合准确率失败 {combination.id}: {e}')
    
    log.info(f'组合准确率计算完成，共更新 {updated_count} 个组合')
    return {
        'total': len(combinations),
        'updated': updated_count,
    }

