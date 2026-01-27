from datetime import datetime, date
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key, UniversalText, TimeZone
from backend.utils.timezone import timezone


class ProjectTopics(Base):
    """项目私有选题表"""

    __tablename__ = 'project_topics'

    id: Mapped[id_key] = mapped_column(init=False)
    uid: Mapped[str] = mapped_column(sa.String(36), default='', comment='主键 UID')
    project_uid: Mapped[str] = mapped_column(sa.String(36), default='', comment='项目 UID')
    user_uid: Mapped[str] = mapped_column(sa.String(36), default='', comment='用户 UID')
    title: Mapped[str] = mapped_column(sa.String(255), default='', comment='选题标题')
    potential_score: Mapped[float] = mapped_column(sa.Double(), default=0.0, comment='选题潜力分数')
    heat_index: Mapped[float] = mapped_column(sa.Double(), default=0.0, comment='热度指数')
    reason: Mapped[str] = mapped_column(UniversalText, default='', comment='推荐理由')
    keywords: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='标签/关键词')
    platform_heat: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='平台热度分布')
    heat_sources: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='热度来源')
    trend: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='趋势走势')
    industry_tags: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='适配行业')
    target_audience: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='目标人群')
    creative_angles: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='创作角度')
    content_outline: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='内容结构要点')
    format_suggestions: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='形式建议')
    material_clues: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='素材线索')
    risk_notes: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='风险点')
    source_info: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='来源信息')
    batch_date: Mapped[date | None] = mapped_column(sa.DATE(), default=None, comment='生成批次日期')
    source_uid: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='幂等键')
    status: Mapped[int] = mapped_column(sa.INTEGER(), default=0, comment='状态(0:待选 1:已采纳 2:已忽略)')
    is_deleted: Mapped[bool] = mapped_column(sa.BOOLEAN(), default=True, comment='是否已删除')
    deleted_at: Mapped[datetime | None] = mapped_column(TimeZone, default=None, comment='删除时间')
    last_sync_at: Mapped[datetime | None] = mapped_column(TimeZone, default=None, comment='最近同步时间')
    server_version: Mapped[int] = mapped_column(sa.INTEGER(), default=0, comment='服务器版本号')
