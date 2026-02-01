"""Openclaw Gateway API 端点"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status

from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession
from backend.core.conf import settings
from backend.app.openclaw import service
from backend.app.openclaw.schema import (
    ConfigSyncResponse,
    GatewayConfigCreate,
    GatewayConfigUpdate,
    GatewayTokenResponse,
)

router = APIRouter()


# ==================== 服务认证依赖 ====================

async def verify_service_auth(
    authorization: Annotated[str | None, Header()] = None,
) -> None:
    """验证服务间认证
    
    Gateway 调用时需要携带服务 token。
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format",
        )
    
    token = authorization[7:]  # Remove "Bearer " prefix
    expected_token = getattr(settings, "OPENCLAW_SERVICE_TOKEN", None)
    
    if not expected_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service token not configured",
        )
    
    if not service.verify_service_token(token, expected_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service token",
        )


DependsServiceAuth = Depends(verify_service_auth)


# ==================== 用户 API (需要用户登录) ====================

@router.post(
    "/token",
    response_model=GatewayTokenResponse,
    summary="生成 Gateway Token",
    description="为当前用户生成 Gateway 认证 token。如果已有 token 则重新生成。",
    dependencies=[DependsJwtAuth],
    name="openclaw_create_gateway_token",
)
async def create_gateway_token(
    request: Request,
    data: GatewayConfigCreate,
    db: CurrentSession,
) -> GatewayTokenResponse:
    """为当前用户生成 Gateway token"""
    user_id = request.user.id
    return await service.create_gateway_config(db, user_id, data)


@router.patch(
    "/config",
    summary="更新 Gateway 配置",
    description="更新当前用户的 Openclaw 配置。",
    dependencies=[DependsJwtAuth],
    name="openclaw_update_gateway_config",
)
async def update_gateway_config(
    request: Request,
    data: GatewayConfigUpdate,
    db: CurrentSession,
):
    """更新用户的 Gateway 配置"""
    user_id = request.user.id
    config = await service.update_gateway_config(
        db,
        user_id,
        openclaw_config=data.openclaw_config,
        status=data.status,
    )
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gateway config not found. Please create one first.",
        )
    return {"message": "Config updated successfully"}


# ==================== Gateway API (服务间调用) ====================

@router.post(
    "/verify-token",
    summary="验证 Gateway Token",
    description="Gateway 实时验证用户 token，返回用户信息和配置。",
    name="openclaw_verify_gateway_token",
)
async def verify_gateway_token(
    db: CurrentSession,
    token: Annotated[str, Query(description="要验证的 Gateway Token")],
):
    """验证 Gateway Token 并返回用户信息
    
    此接口不需要服务认证，但 token 本身就是认证凭证。
    """
    result = await service.verify_gateway_token(db, token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired gateway token",
        )
    # Wrap in 'data' to match OpenClaw gateway expectations
    return {"data": result}


@router.get(
    "/configs",
    response_model=ConfigSyncResponse,
    summary="同步 Gateway 配置",
    description="Gateway 调用此接口同步用户配置。支持增量同步。",
    dependencies=[DependsServiceAuth],
    name="openclaw_sync_gateway_configs",
)
async def sync_gateway_configs(
    db: CurrentSession,
    since: Annotated[str | None, Query(description="增量同步起始时间 (ISO 格式)")] = None,
    limit: Annotated[int, Query(ge=1, le=500, description="每页数量")] = 100,
    cursor: Annotated[str | None, Query(description="分页游标")] = None,
) -> ConfigSyncResponse:
    """获取 Gateway 配置用于同步"""
    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid since format. Use ISO 8601.",
            )
    
    return await service.sync_gateway_configs(db, since_dt, limit, cursor)

