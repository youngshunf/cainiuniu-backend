"""彩种管理API"""

from fastapi import APIRouter, Query

from backend.app.lottery.crud import lottery_type_dao
from backend.app.lottery.schema.lottery_type import (
    AddLotteryTypeParam,
    UpdateLotteryTypeParam,
)
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/list', summary='获取彩种列表', dependencies=[DependsJwtAuth, DependsPagination])
async def get_lottery_type_list(
    db: CurrentSession,
    category: str | None = Query(None, description='类别'),
    status: int | None = Query(None, description='状态'),
) -> ResponseModel:
    """获取彩种列表"""
    lottery_type_select = await lottery_type_dao.get_select(category=category, status=status)
    page_data = await paging_data(db, lottery_type_select)
    return response_base.success(data=page_data)


@router.get('/{pk}', summary='获取彩种详情', dependencies=[DependsJwtAuth])
async def get_lottery_type(db: CurrentSession, pk: int) -> ResponseModel:
    """获取彩种详情"""
    lottery_type = await lottery_type_dao.get(db, pk)
    if not lottery_type:
        return response_base.fail(msg='彩种不存在')
    return response_base.success(data=lottery_type)


@router.post('/create', summary='添加彩种', dependencies=[DependsJwtAuth])
async def create_lottery_type(db: CurrentSession, obj: AddLotteryTypeParam) -> ResponseModel:
    """添加彩种"""
    # 检查代码是否已存在
    existing = await lottery_type_dao.get_by_code(db, obj.code)
    if existing:
        return response_base.fail(msg='彩种代码已存在')
    
    await lottery_type_dao.add(db, obj)
    await db.commit()
    return response_base.success()


@router.put('/{pk}', summary='更新彩种', dependencies=[DependsJwtAuth])
async def update_lottery_type(
    db: CurrentSession, pk: int, obj: UpdateLotteryTypeParam
) -> ResponseModel:
    """更新彩种"""
    lottery_type = await lottery_type_dao.get(db, pk)
    if not lottery_type:
        return response_base.fail(msg='彩种不存在')
    
    await lottery_type_dao.update(db, pk, obj)
    await db.commit()
    return response_base.success()


@router.delete('/{pk}', summary='删除彩种', dependencies=[DependsJwtAuth])
async def delete_lottery_type(db: CurrentSession, pk: int) -> ResponseModel:
    """删除彩种"""
    lottery_type = await lottery_type_dao.get(db, pk)
    if not lottery_type:
        return response_base.fail(msg='彩种不存在')
    
    await lottery_type_dao.delete(db, pk)
    await db.commit()
    return response_base.success()

