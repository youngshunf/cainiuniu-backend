"""预测API"""

from fastapi import APIRouter, Query, Request

from backend.app.lottery.crud import prediction_dao
from backend.app.lottery.service.prediction_service import prediction_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/list', summary='获取预测列表', dependencies=[DependsJwtAuth, DependsPagination])
async def get_prediction_list(
    db: CurrentSession,
    request: Request,
    lottery_code: str | None = Query(None, description='彩种代码'),
    is_verified: bool | None = Query(None, description='是否已验证'),
) -> ResponseModel:
    """获取预测列表"""
    user_id = None  # 管理员可以看到所有预测，如需只看自己的预测，使用 request.user.id
    prediction_select = await prediction_dao.get_select(
        user_id=user_id,
        lottery_code=lottery_code,
        target_period=None,
        is_verified=is_verified,
    )
    page_data = await paging_data(db, prediction_select)
    return response_base.success(data=page_data)


@router.get('/{pk}', summary='获取预测详情', dependencies=[DependsJwtAuth])
async def get_prediction(db: CurrentSession, pk: int) -> ResponseModel:
    """获取预测详情"""
    prediction = await prediction_dao.get(db, pk)
    if not prediction:
        return response_base.fail(msg='预测不存在')
    return response_base.success(data=prediction)


@router.post('/create', summary='创建预测', dependencies=[DependsJwtAuth])
async def create_prediction(
    db: CurrentSession,
    request: Request,
    lottery_code: str = Query(..., description='彩种代码'),
    combination_id: int | None = Query(None, description='组合ID'),
    history_periods: int = Query(100, description='历史期数', ge=10, le=1000),
) -> ResponseModel:
    """创建预测"""
    user_id = request.user.id if hasattr(request, 'user') else None
    result = await prediction_service.create_prediction(
        db, lottery_code, combination_id, history_periods, user_id
    )
    return response_base.success(data=result)


@router.post('/{prediction_id}/verify', summary='验证预测结果', dependencies=[DependsJwtAuth])
async def verify_prediction(
    db: CurrentSession, prediction_id: int
) -> ResponseModel:
    """验证预测结果"""
    result = await prediction_service.verify_prediction(db, prediction_id)
    return response_base.success(data=result)

