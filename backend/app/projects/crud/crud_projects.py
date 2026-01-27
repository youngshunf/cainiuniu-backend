from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.projects.model import Projects
from backend.app.projects.schema.projects import CreateProjectsParam, UpdateProjectsParam


class CRUDProjects(CRUDPlus[Projects]):
    async def get(self, db: AsyncSession, pk: int) -> Projects | None:
        """
        获取项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :param pk: 项目表 - 工作区的核心上下文 ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_select(self) -> Select:
        """获取项目表 - 工作区的核心上下文列表查询表达式"""
        return await self.select_order('id', 'desc')

    async def get_all(self, db: AsyncSession) -> Sequence[Projects]:
        """
        获取所有项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj: CreateProjectsParam) -> None:
        """
        创建项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :param obj: 创建项目表 - 工作区的核心上下文参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateProjectsParam) -> int:
        """
        更新项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :param pk: 项目表 - 工作区的核心上下文 ID
        :param obj: 更新 项目表 - 工作区的核心上下文参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :param pks: 项目表 - 工作区的核心上下文 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


projects_dao: CRUDProjects = CRUDProjects(Projects)
