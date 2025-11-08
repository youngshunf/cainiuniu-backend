"""组合管理API"""

from fastapi import APIRouter, Query, Request

from backend.app.lottery.crud import combination_dao
from backend.app.lottery.schema.analysis_combination import (
    AddCombinationParam,
    UpdateCombinationParam,
)
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/list', summary='获取组合列表', dependencies=[DependsJwtAuth, DependsPagination])
async def get_combination_list(
    db: CurrentSession,
    request: Request,
    lottery_code: str | None = Query(None, description='彩种代码'),
    is_auto: bool | None = Query(None, description='是否自动预测'),
) -> ResponseModel:
    """获取组合列表"""
    user_id = request.user.id if hasattr(request, 'user') else None
    combination_select = await combination_dao.get_select(
        user_id=user_id, lottery_code=lottery_code, is_auto=is_auto, status=1
    )
    page_data = await paging_data(db, combination_select)
    return response_base.success(data=page_data)


@router.get('/{pk}', summary='获取组合详情', dependencies=[DependsJwtAuth])
async def get_combination(db: CurrentSession, pk: int) -> ResponseModel:
    """获取组合详情"""
    combination = await combination_dao.get(db, pk)
    if not combination:
        return response_base.fail(msg='组合不存在')
    return response_base.success(data=combination)


@router.post('/create', summary='创建组合', dependencies=[DependsJwtAuth])
async def create_combination(
    db: CurrentSession, request: Request, obj: AddCombinationParam
) -> ResponseModel:
    """创建组合"""
    user_id = request.user.id if hasattr(request, 'user') else 0
    await combination_dao.add(db, obj, user_id)
    await db.commit()
    return response_base.success()


@router.put('/{pk}', summary='更新组合', dependencies=[DependsJwtAuth])
async def update_combination(
    db: CurrentSession, pk: int, obj: UpdateCombinationParam
) -> ResponseModel:
    """更新组合"""
    combination = await combination_dao.get(db, pk)
    if not combination:
        return response_base.fail(msg='组合不存在')

    await combination_dao.update(db, pk, obj)
    await db.commit()
    return response_base.success()


@router.delete('/{pk}', summary='删除组合', dependencies=[DependsJwtAuth])
async def delete_combination(db: CurrentSession, pk: int) -> ResponseModel:
    """删除组合"""
    combination = await combination_dao.get(db, pk)
    if not combination:
        return response_base.fail(msg='组合不存在')

    await combination_dao.delete(db, pk)
    await db.commit()
    return response_base.success()

