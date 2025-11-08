"""分析API"""

from fastapi import APIRouter, Body, Query

from backend.app.lottery.service.analysis_service import analysis_service
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/methods', summary='获取分析方法列表', dependencies=[DependsJwtAuth])
async def get_analysis_methods() -> ResponseModel:
    """获取所有可用的分析方法"""
    methods = await analysis_service.get_method_list()
    return response_base.success(data=methods)


@router.post('/analyze', summary='单个方法分析', dependencies=[DependsJwtAuth])
async def analyze_single_method(
    db: CurrentSession,
    lottery_code: str = Query(..., description='彩种代码'),
    method_code: str = Query(..., description='方法代码'),
    history_periods: int = Query(100, description='历史期数', ge=10, le=1000),
    params: dict = Body(default={}, description='分析参数'),
) -> ResponseModel:
    """单个方法分析"""
    result = await analysis_service.analyze_single_method(
        db, lottery_code, method_code, history_periods, params
    )
    return response_base.success(data=result)

