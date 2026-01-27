from datetime import datetime
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key, TimeZone
from backend.utils.timezone import timezone


class Projects(Base):
    """项目表 - 工作区的核心上下文"""

    __tablename__ = 'projects'

    id: Mapped[id_key] = mapped_column(init=False)
    uid: Mapped[str] = mapped_column(sa.String(36), default='', comment='主键 UID')
    user_uid: Mapped[str] = mapped_column(sa.String(36), default='', comment='用户 UID')
    industry: Mapped[str | None] = mapped_column(sa.String(50), default=None, comment='行业')
    sub_industries: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='子行业列表')
    brand_name: Mapped[str | None] = mapped_column(sa.String(100), default=None, comment='品牌名称')
    brand_tone: Mapped[str | None] = mapped_column(sa.String(50), default=None, comment='品牌调性')
    brand_keywords: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='品牌关键词')
    topics: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='关注话题')
    keywords: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='内容关键词')
    account_tags: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='账号标签')
    preferred_platforms: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='偏好平台')
    content_style: Mapped[str | None] = mapped_column(sa.String(50), default=None, comment='内容风格')
    settings: Mapped[dict] = mapped_column(postgresql.JSONB(), default_factory=dict, comment='其他设置')
    is_default: Mapped[bool] = mapped_column(sa.BOOLEAN(), default=True, comment='是否默认项目')
    is_deleted: Mapped[bool] = mapped_column(sa.BOOLEAN(), default=True, comment='是否已删除')
    deleted_at: Mapped[datetime | None] = mapped_column(TimeZone, default=None, comment='删除时间')
    server_version: Mapped[int] = mapped_column(sa.INTEGER(), default=0, comment='服务器版本号')
