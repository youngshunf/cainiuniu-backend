from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.projects.crud.crud_projects import projects_dao
from backend.app.projects.model import Projects
from backend.app.projects.schema.projects import CreateProjectsParam, DeleteProjectsParam, UpdateProjectsParam
from backend.common.exception import errors
from backend.common.pagination import paging_data


class ProjectsService:
    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Projects:
        """
        获取项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :param pk: 项目表 - 工作区的核心上下文 ID
        :return:
        """
        projects = await projects_dao.get(db, pk)
        if not projects:
            raise errors.NotFoundError(msg='项目表 - 工作区的核心上下文不存在')
        return projects

    @staticmethod
    async def get_list(db: AsyncSession) -> dict[str, Any]:
        """
        获取项目表 - 工作区的核心上下文列表

        :param db: 数据库会话
        :return:
        """
        projects_select = await projects_dao.get_select()
        return await paging_data(db, projects_select)

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[Projects]:
        """
        获取所有项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :return:
        """
        projectss = await projects_dao.get_all(db)
        return projectss

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateProjectsParam) -> None:
        """
        创建项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :param obj: 创建项目表 - 工作区的核心上下文参数
        :return:
        """
        await projects_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateProjectsParam) -> int:
        """
        更新项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :param pk: 项目表 - 工作区的核心上下文 ID
        :param obj: 更新项目表 - 工作区的核心上下文参数
        :return:
        """
        count = await projects_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteProjectsParam) -> int:
        """
        删除项目表 - 工作区的核心上下文

        :param db: 数据库会话
        :param obj: 项目表 - 工作区的核心上下文 ID 列表
        :return:
        """
        count = await projects_dao.delete(db, obj.pks)
        return count


projects_service: ProjectsService = ProjectsService()
