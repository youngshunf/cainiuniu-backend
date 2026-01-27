from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.projects.model import ProjectTopics
from backend.app.projects.schema.project_topics import CreateProjectTopicsParam, UpdateProjectTopicsParam


class CRUDProjectTopics(CRUDPlus[ProjectTopics]):
    async def get(self, db: AsyncSession, pk: int) -> ProjectTopics | None:
        """
        获取项目私有选题

        :param db: 数据库会话
        :param pk: 项目私有选题 ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_select(self) -> Select:
        """获取项目私有选题列表查询表达式"""
        return await self.select_order('id', 'desc')

    async def get_all(self, db: AsyncSession) -> Sequence[ProjectTopics]:
        """
        获取所有项目私有选题

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj: CreateProjectTopicsParam) -> None:
        """
        创建项目私有选题

        :param db: 数据库会话
        :param obj: 创建项目私有选题参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateProjectTopicsParam) -> int:
        """
        更新项目私有选题

        :param db: 数据库会话
        :param pk: 项目私有选题 ID
        :param obj: 更新 项目私有选题参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除项目私有选题

        :param db: 数据库会话
        :param pks: 项目私有选题 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


project_topics_dao: CRUDProjectTopics = CRUDProjectTopics(ProjectTopics)
