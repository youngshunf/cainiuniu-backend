"""Openclaw Gateway API 路由汇总"""

from fastapi import APIRouter

from backend.app.openclaw.api.v1.gateway import router as gateway_router

v1 = APIRouter(prefix="/api/v1/openclaw", tags=["Openclaw Gateway"])
v1.include_router(gateway_router, prefix="/gateway")
