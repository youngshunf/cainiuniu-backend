"""Openclaw Gateway Pydantic schemas"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ==================== Gateway Config ====================

class GatewayConfigBase(BaseModel):
    """Gateway 配置基础字段"""
    openclaw_config: dict[str, Any] | None = Field(
        default=None, 
        description="Openclaw 配置 (JSON)"
    )


class GatewayConfigCreate(GatewayConfigBase):
    """创建 Gateway 配置"""
    pass


class GatewayConfigUpdate(BaseModel):
    """更新 Gateway 配置"""
    openclaw_config: dict[str, Any] | None = Field(
        default=None, 
        description="Openclaw 配置"
    )
    status: str | None = Field(
        default=None, 
        description="状态: active, suspended, expired"
    )


class GatewayConfigResponse(GatewayConfigBase):
    """Gateway 配置响应"""
    id: int
    user_id: int
    gateway_token: str = Field(description="Gateway 认证 token (仅创建时返回完整值)")
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class GatewayTokenResponse(BaseModel):
    """Gateway Token 响应 (仅创建时返回)"""
    gateway_token: str = Field(description="完整的 Gateway token")
    user_id: int
    status: str


# ==================== Config Sync ====================

class CloudUserConfig(BaseModel):
    """云端用户配置 (供 Gateway 同步)"""
    user_id: str = Field(description="用户 ID")
    gateway_token: str = Field(description="Gateway 认证 token")
    openclaw_config: dict[str, Any] = Field(
        default_factory=dict, 
        description="Openclaw 配置"
    )
    status: str = Field(default="active", description="状态")
    llm_api_key: str | None = Field(default=None, description="用户的 LLM API key")
    updated_at: str = Field(description="最后更新时间 (ISO 格式)")


class ConfigSyncResponse(BaseModel):
    """配置同步响应"""
    users: list[CloudUserConfig] = Field(description="用户配置列表")
    sync_timestamp: str = Field(description="同步时间戳 (用于增量同步)")
    has_more: bool = Field(default=False, description="是否有更多数据")
    next_cursor: str | None = Field(default=None, description="分页游标")


# ==================== Service Auth ====================

class ServiceAuthHeader(BaseModel):
    """服务间认证 Header"""
    authorization: str = Field(description="Bearer token")
