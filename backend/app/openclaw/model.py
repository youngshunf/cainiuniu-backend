"""Openclaw Gateway 配置表"""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, TimeZone, id_key


class GatewayConfig(Base):
    """Openclaw Gateway 配置表
    
    存储用户的 Gateway 认证 token 和 Openclaw 配置。
    关联现有用户表，不重复存储用户信息。
    """

    __tablename__ = 'openclaw_gateway_configs'

    id: Mapped[id_key] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, 
        unique=True, 
        index=True, 
        comment='用户 ID (关联现有用户表)'
    )
    gateway_token: Mapped[str] = mapped_column(
        sa.String(128), 
        unique=True, 
        index=True, 
        comment='Gateway 认证 token'
    )
    gateway_token_hash: Mapped[str] = mapped_column(
        sa.String(64), 
        unique=True, 
        index=True, 
        comment='Gateway token SHA-256 哈希 (用于快速查找)'
    )
    openclaw_config: Mapped[dict | None] = mapped_column(
        sa.JSON, 
        default=None, 
        comment='Openclaw 配置 (JSON)'
    )
    status: Mapped[str] = mapped_column(
        sa.String(16), 
        default='active', 
        index=True, 
        comment='状态: active, suspended, expired'
    )
    last_sync_at: Mapped[datetime | None] = mapped_column(
        TimeZone, 
        init=False, 
        default=None, 
        comment='最后同步时间'
    )
    metadata_: Mapped[dict | None] = mapped_column(
        'metadata', 
        sa.JSON, 
        default=None, 
        comment='元数据'
    )
