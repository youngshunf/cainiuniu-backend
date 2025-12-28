"""LLM API 路由注册"""

from fastapi import APIRouter

from backend.app.llm.api.v1 import api_keys, models, providers, proxy, usage

v1 = APIRouter()

# 模型管理
v1.include_router(models.router, prefix='/models', tags=['LLM 模型管理'])

# 供应商管理
v1.include_router(providers.router, prefix='/providers', tags=['LLM 供应商管理'])

# API Key 管理
v1.include_router(api_keys.router, prefix='/api-keys', tags=['LLM API Key 管理'])

# 代理 API
v1.include_router(proxy.router, prefix='/proxy', tags=['LLM 代理'])

# 用量统计
v1.include_router(usage.router, prefix='/usage', tags=['LLM 用量统计'])
