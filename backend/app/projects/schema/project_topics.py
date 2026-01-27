from datetime import datetime, date
from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ProjectTopicsSchemaBase(SchemaBase):
    """项目私有选题基础模型"""
    uid: str = Field(description='主键 UID')
    project_uid: str = Field(description='项目 UID')
    user_uid: str = Field(description='用户 UID')
    title: str = Field(description='选题标题')
    potential_score: float = Field(description='选题潜力分数')
    heat_index: float = Field(description='热度指数')
    reason: str = Field(description='推荐理由')
    keywords: dict = Field(description='标签/关键词')
    platform_heat: dict = Field(description='平台热度分布')
    heat_sources: dict = Field(description='热度来源')
    trend: dict = Field(description='趋势走势')
    industry_tags: dict = Field(description='适配行业')
    target_audience: dict = Field(description='目标人群')
    creative_angles: dict = Field(description='创作角度')
    content_outline: dict = Field(description='内容结构要点')
    format_suggestions: dict = Field(description='形式建议')
    material_clues: dict = Field(description='素材线索')
    risk_notes: dict = Field(description='风险点')
    source_info: dict = Field(description='来源信息')
    batch_date: date | None = Field(None, description='生成批次日期')
    source_uid: str | None = Field(None, description='幂等键')
    status: int = Field(description='状态(0:待选 1:已采纳 2:已忽略)')
    is_deleted: bool = Field(description='是否已删除')
    deleted_at: datetime | None = Field(None, description='删除时间')
    last_sync_at: datetime | None = Field(None, description='最近同步时间')
    server_version: int = Field(description='服务器版本号')


class CreateProjectTopicsParam(ProjectTopicsSchemaBase):
    """创建项目私有选题参数"""


class UpdateProjectTopicsParam(ProjectTopicsSchemaBase):
    """更新项目私有选题参数"""


class DeleteProjectTopicsParam(SchemaBase):
    """删除项目私有选题参数"""

    pks: list[int] = Field(description='项目私有选题 ID 列表')


class GetProjectTopicsDetail(ProjectTopicsSchemaBase):
    """项目私有选题详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
