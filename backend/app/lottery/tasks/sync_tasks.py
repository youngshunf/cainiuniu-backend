"""开奖数据同步Celery任务"""

from backend.app.lottery.crud import lottery_type_dao
from backend.app.lottery.service.sync_service import sync_service
from backend.app.task.celery import celery_app
from backend.database.db import async_db_session
from backend.common.log import log


@celery_app.task(name='lottery.sync_latest_draw')
async def sync_latest_draw():
    """
    同步最新开奖数据（所有彩种）
    
    每天21:30自动执行
    """
    log.info('开始同步最新开奖数据...')
    results = []
    
    async with async_db_session() as db:
        # 获取所有启用的彩票类型
        lottery_types = await lottery_type_dao.get_all_active(db)
        
        for lottery_type in lottery_types:
            try:
                log.info(f'同步彩种: {lottery_type.name}({lottery_type.code})')
                result = await sync_service.sync_lottery_data(db, lottery_type.code, page_size=10)
                results.append(result)
                log.info(f'同步完成: {result}')
            except Exception as e:
                log.error(f'同步失败 {lottery_type.code}: {e}')
                results.append({
                    'success': False,
                    'lottery_code': lottery_type.code,
                    'error': str(e),
                })
    
    log.info(f'全部同步完成: {results}')
    return results


@celery_app.task(name='lottery.sync_single_lottery')
async def sync_single_lottery(lottery_code: str, page_size: int = 30):
    """
    同步单个彩种历史数据
    
    :param lottery_code: 彩种代码
    :param page_size: 同步数量
    """
    log.info(f'开始同步彩种 {lottery_code}，数量: {page_size}')
    
    async with async_db_session() as db:
        try:
            result = await sync_service.sync_lottery_data(db, lottery_code, page_size)
            log.info(f'同步完成: {result}')
            return result
        except Exception as e:
            log.error(f'同步失败: {e}')
            return {
                'success': False,
                'lottery_code': lottery_code,
                'error': str(e),
            }


@celery_app.task(name='lottery.sync_all_history')
async def sync_all_history(lottery_code: str):
    """
    首次全量同步历史数据
    
    :param lottery_code: 彩种代码
    """
    log.info(f'开始全量同步 {lottery_code} 历史数据')
    
    # 分批同步，避免一次性请求过多
    batch_size = 100
    max_batches = 100  # 最多同步10000期
    
    results = []
    for i in range(max_batches):
        result = await sync_single_lottery(lottery_code, batch_size)
        results.append(result)
        
        # 如果没有新数据了，停止
        if not result.get('success') or result.get('success_count', 0) == 0:
            break
    
    log.info(f'全量同步完成: {lottery_code}')
    return {
        'lottery_code': lottery_code,
        'batches': len(results),
        'results': results,
    }

