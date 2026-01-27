from datetime import datetime
from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ProjectsSchemaBase(SchemaBase):
    """项目表 - 工作区的核心上下文基础模型"""
    uid: str = Field(description='主键 UID')
    user_uid: str = Field(description='用户 UID')
    industry: str | None = Field(None, description='行业')
    sub_industries: dict = Field(description='子行业列表')
    brand_name: str | None = Field(None, description='品牌名称')
    brand_tone: str | None = Field(None, description='品牌调性')
    brand_keywords: dict = Field(description='品牌关键词')
    topics: dict = Field(description='关注话题')
    keywords: dict = Field(description='内容关键词')
    account_tags: dict = Field(description='账号标签')
    preferred_platforms: dict = Field(description='偏好平台')
    content_style: str | None = Field(None, description='内容风格')
    settings: dict = Field(description='其他设置')
    is_default: bool = Field(description='是否默认项目')
    is_deleted: bool = Field(description='是否已删除')
    deleted_at: datetime | None = Field(None, description='删除时间')
    server_version: int = Field(description='服务器版本号')


class CreateProjectsParam(ProjectsSchemaBase):
    """创建项目表 - 工作区的核心上下文参数"""


class UpdateProjectsParam(ProjectsSchemaBase):
    """更新项目表 - 工作区的核心上下文参数"""


class DeleteProjectsParam(SchemaBase):
    """删除项目表 - 工作区的核心上下文参数"""

    pks: list[int] = Field(description='项目表 - 工作区的核心上下文 ID 列表')


class GetProjectsDetail(ProjectsSchemaBase):
    """项目表 - 工作区的核心上下文详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
