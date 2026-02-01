from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.projects.schema.projects import (
    CreateProjectsParam,
    DeleteProjectsParam,
    GetProjectsDetail,
    UpdateProjectsParam,
)
from backend.app.projects.service.projects_service import projects_service
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取项目表 - 工作区的核心上下文详情', dependencies=[DependsJwtAuth])
async def get_projects(
    db: CurrentSession, pk: Annotated[int, Path(description='项目表 - 工作区的核心上下文 ID')]
) -> ResponseSchemaModel[GetProjectsDetail]:
    projects = await projects_service.get(db=db, pk=pk)
    return response_base.success(data=projects)


@router.get(
    '',
    summary='分页获取所有项目表 - 工作区的核心上下文',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_projectss_paginated(db: CurrentSession) -> ResponseSchemaModel[PageData[GetProjectsDetail]]:
    page_data = await projects_service.get_list(db=db)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建项目表 - 工作区的核心上下文',
    dependencies=[
        Depends(RequestPermission('projects:add')),
        DependsRBAC,
    ],
)
async def create_projects(db: CurrentSessionTransaction, obj: CreateProjectsParam) -> ResponseModel:
    await projects_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新项目表 - 工作区的核心上下文',
    dependencies=[
        Depends(RequestPermission('projects:edit')),
        DependsRBAC,
    ],
)
async def update_projects(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='项目表 - 工作区的核心上下文 ID')], obj: UpdateProjectsParam
) -> ResponseModel:
    count = await projects_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除项目',
    dependencies=[
        Depends(RequestPermission('projects:del')),
        DependsRBAC,
    ],
)
async def delete_projects(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='项目 ID')]
) -> ResponseModel:
    count = await projects_service.delete(db=db, obj=DeleteProjectsParam(pks=[pk]))
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除项目表 - 工作区的核心上下文',
    dependencies=[
        Depends(RequestPermission('projects:del')),
        DependsRBAC,
    ],
)
async def delete_projectss(db: CurrentSessionTransaction, obj: DeleteProjectsParam) -> ResponseModel:
    count = await projects_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
