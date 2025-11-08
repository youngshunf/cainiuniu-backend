"""开奖数据API"""

from datetime import date

from fastapi import APIRouter, Query

from backend.app.lottery.crud import draw_result_dao
from backend.app.lottery.service.sync_service import sync_service
from backend.app.lottery.tasks.sync_tasks import sync_all_history, sync_single_lottery
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/list', summary='获取开奖列表', dependencies=[DependsJwtAuth, DependsPagination])
async def get_draw_result_list(
    db: CurrentSession,
    lottery_code: str | None = Query(None, description='彩种代码'),
    period: str | None = Query(None, description='期号'),
    start_date: date | None = Query(None, description='开始日期'),
    end_date: date | None = Query(None, description='结束日期'),
) -> ResponseModel:
    """获取开奖列表"""
    draw_result_select = await draw_result_dao.get_select(
        lottery_code=lottery_code, period=period, start_date=start_date, end_date=end_date
    )
    page_data = await paging_data(db, draw_result_select)
    return response_base.success(data=page_data)


@router.get('/{lottery_code}/{period}', summary='获取单期开奖详情', dependencies=[DependsJwtAuth])
async def get_draw_result(
    db: CurrentSession, lottery_code: str, period: str
) -> ResponseModel:
    """获取单期开奖详情"""
    draw_result = await draw_result_dao.get_by_lottery_and_period(db, lottery_code, period)
    if not draw_result:
        return response_base.fail(msg='开奖数据不存在')
    return response_base.success(data=draw_result)


@router.get('/{lottery_code}/latest', summary='获取最新开奖', dependencies=[DependsJwtAuth])
async def get_latest_draw_result(db: CurrentSession, lottery_code: str) -> ResponseModel:
    """获取最新开奖"""
    draw_result = await draw_result_dao.get_latest_by_lottery(db, lottery_code)
    if not draw_result:
        return response_base.fail(msg='暂无开奖数据')
    return response_base.success(data=draw_result)


@router.get('/{lottery_code}/history', summary='获取历史开奖', dependencies=[DependsJwtAuth])
async def get_history_draw_results(
    db: CurrentSession,
    lottery_code: str,
    limit: int = Query(100, description='数量', ge=1, le=1000),
) -> ResponseModel:
    """获取历史开奖"""
    draw_results = await draw_result_dao.get_history_by_lottery(db, lottery_code, limit)
    return response_base.success(data=draw_results)


@router.post('/sync/{lottery_code}', summary='手动同步开奖数据', dependencies=[DependsJwtAuth])
async def sync_draw_data(
    db: CurrentSession,
    lottery_code: str,
    page_size: int = Query(30, description='同步数量', ge=1, le=100),
) -> ResponseModel:
    """手动同步开奖数据"""
    result = await sync_service.sync_lottery_data(db, lottery_code, page_size)
    return response_base.success(data=result)


@router.post('/sync/{lottery_code}/history', summary='全量同步历史数据', dependencies=[DependsJwtAuth])
async def sync_history_data(lottery_code: str) -> ResponseModel:
    """全量同步历史数据（异步任务）"""
    task = sync_all_history.delay(lottery_code)
    return response_base.success(data={'task_id': task.id, 'status': 'started'})


@router.get('/{lottery_code}/next-period', summary='获取下期期号', dependencies=[DependsJwtAuth])
async def get_next_period(db: CurrentSession, lottery_code: str) -> ResponseModel:
    """获取下期期号"""
    next_period = await sync_service.calculate_next_period(db, lottery_code)
    return response_base.success(data={'next_period': next_period})

