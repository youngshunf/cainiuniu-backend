from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.projects.schema.project_topics import (
    CreateProjectTopicsParam,
    DeleteProjectTopicsParam,
    GetProjectTopicsDetail,
    UpdateProjectTopicsParam,
)
from backend.app.projects.service.project_topics_service import project_topics_service
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取项目私有选题详情', dependencies=[DependsJwtAuth])
async def get_project_topics(
    db: CurrentSession, pk: Annotated[int, Path(description='项目私有选题 ID')]
) -> ResponseSchemaModel[GetProjectTopicsDetail]:
    project_topics = await project_topics_service.get(db=db, pk=pk)
    return response_base.success(data=project_topics)


@router.get(
    '',
    summary='分页获取所有项目私有选题',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_project_topicss_paginated(db: CurrentSession) -> ResponseSchemaModel[PageData[GetProjectTopicsDetail]]:
    page_data = await project_topics_service.get_list(db=db)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建项目私有选题',
    dependencies=[
        Depends(RequestPermission('project:topics:add')),
        DependsRBAC,
    ],
)
async def create_project_topics(db: CurrentSessionTransaction, obj: CreateProjectTopicsParam) -> ResponseModel:
    await project_topics_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新项目私有选题',
    dependencies=[
        Depends(RequestPermission('project:topics:edit')),
        DependsRBAC,
    ],
)
async def update_project_topics(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='项目私有选题 ID')], obj: UpdateProjectTopicsParam
) -> ResponseModel:
    count = await project_topics_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除项目私有选题',
    dependencies=[
        Depends(RequestPermission('project:topics:del')),
        DependsRBAC,
    ],
)
async def delete_project_topics(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='项目私有选题 ID')]
) -> ResponseModel:
    count = await project_topics_service.delete(db=db, obj=DeleteProjectTopicsParam(pks=[pk]))
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除项目私有选题',
    dependencies=[
        Depends(RequestPermission('project:topics:del')),
        DependsRBAC,
    ],
)
async def delete_project_topicss(db: CurrentSessionTransaction, obj: DeleteProjectTopicsParam) -> ResponseModel:
    count = await project_topics_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
