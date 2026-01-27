from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.projects.crud.crud_project_topics import project_topics_dao
from backend.app.projects.model import ProjectTopics
from backend.app.projects.schema.project_topics import CreateProjectTopicsParam, DeleteProjectTopicsParam, UpdateProjectTopicsParam
from backend.common.exception import errors
from backend.common.pagination import paging_data


class ProjectTopicsService:
    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> ProjectTopics:
        """
        获取项目私有选题

        :param db: 数据库会话
        :param pk: 项目私有选题 ID
        :return:
        """
        project_topics = await project_topics_dao.get(db, pk)
        if not project_topics:
            raise errors.NotFoundError(msg='项目私有选题不存在')
        return project_topics

    @staticmethod
    async def get_list(db: AsyncSession) -> dict[str, Any]:
        """
        获取项目私有选题列表

        :param db: 数据库会话
        :return:
        """
        project_topics_select = await project_topics_dao.get_select()
        return await paging_data(db, project_topics_select)

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[ProjectTopics]:
        """
        获取所有项目私有选题

        :param db: 数据库会话
        :return:
        """
        project_topicss = await project_topics_dao.get_all(db)
        return project_topicss

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateProjectTopicsParam) -> None:
        """
        创建项目私有选题

        :param db: 数据库会话
        :param obj: 创建项目私有选题参数
        :return:
        """
        await project_topics_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateProjectTopicsParam) -> int:
        """
        更新项目私有选题

        :param db: 数据库会话
        :param pk: 项目私有选题 ID
        :param obj: 更新项目私有选题参数
        :return:
        """
        count = await project_topics_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteProjectTopicsParam) -> int:
        """
        删除项目私有选题

        :param db: 数据库会话
        :param obj: 项目私有选题 ID 列表
        :return:
        """
        count = await project_topics_dao.delete(db, obj.pks)
        return count


project_topics_service: ProjectTopicsService = ProjectTopicsService()
