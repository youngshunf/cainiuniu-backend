# Cloud Backend - AI 上下文文档

> **路径**: `services/cloud-backend/`
> **类型**: FastAPI 云端后端服务
> **作者**: @Ysf

---

## 📋 模块概览

**Cloud Backend** 是 CreatorFlow 的云端后端服务，基于 fastapi_best_architecture 框架构建。

### 核心定位

- 提供云端 Agent 执行能力
- 管理云端浏览器池
- 凭证同步服务
- 用户认证与授权
- 订阅与计费

### 技术栈

- **框架**: FastAPI + SQLAlchemy 2.0 + Pydantic v2
- **数据库**: PostgreSQL + Redis
- **任务队列**: Celery
- **存储**: MinIO/S3
- **搜索**: Meilisearch

---

## 🏗️ 目录结构

```
services/cloud-backend/
├── pyproject.toml                       # 包配置
├── README.md                            # 包说明
├── CLAUDE.md                            # 本文档
│
└── backend/                             # 源代码
    ├── __init__.py                      # 版本信息
    ├── cli.py                           # CLI 工具
    │
    ├── app/                             # 应用层
    │   ├── main.py                      # FastAPI 应用入口
    │   │
    │   ├── api/                         # API 路由
    │   │   ├── v1/                      # API v1
    │   │   │   ├── auth.py              # 认证接口
    │   │   │   ├── agent.py             # Agent 接口
    │   │   │   ├── credential.py        # 凭证接口
    │   │   │   └── llm.py               # LLM 接口
    │   │   └── router.py                # 路由注册
    │   │
    │   ├── agent/                       # Agent 模块
    │   │   ├── __init__.py
    │   │   ├── executor.py              # CloudExecutor
    │   │   └── tools/                   # 云端工具
    │   │       ├── __init__.py
    │   │       └── browser.py           # 云端浏览器工具
    │   │
    │   ├── credential/                  # 凭证模块
    │   │   ├── __init__.py
    │   │   ├── model.py                 # 数据模型
    │   │   ├── schema.py                # Pydantic Schema
    │   │   ├── service.py               # 业务服务
    │   │   └── api.py                   # REST API
    │   │
    │   ├── services/                    # 业务服务
    │   │   ├── __init__.py
    │   │   └── browser_pool.py          # 浏览器池管理
    │   │
    │   ├── models/                      # 数据模型
    │   │   ├── __init__.py
    │   │   ├── user.py                  # 用户模型
    │   │   └── subscription.py          # 订阅模型
    │   │
    │   └── task/                        # 异步任务
    │       ├── __init__.py
    │       └── agent_task.py            # Agent 任务
    │
    ├── plugin/                          # 插件系统
    │   ├── oauth2/                      # OAuth2 插件
    │   ├── notice/                      # 通知插件
    │   ├── email/                       # 邮件插件
    │   └── config/                      # 配置插件
    │
    └── alembic/                         # 数据库迁移
        ├── versions/                    # 迁移脚本
        └── env.py                       # Alembic 配置
```

---




## 📦 依赖管理

### pyproject.toml

```toml
[project]
name = "fastapi_best_architecture"
requires-python = ">=3.10"

dependencies = [
    "alembic>=1.17.2",
    "fastapi[standard-no-fastapi-cloud-cli]>=0.123.5",
    "sqlalchemy[asyncio]>=2.0.44",
    "celery>=5.6.0",
    "redis[hiredis]>=7.1.0",
    "litellm>=1.0.0",
]
```

---

## 🧪 开发

### 启动服务



### 数据库迁移

```bash
# 生成迁移脚本
uv run alembic revision --autogenerate -m "description"

# 执行迁移
uv run alembic upgrade head

# 回滚迁移
uv run alembic downgrade -1
```

---




## 🔼 导航

[← 返回根目录](../../CLAUDE.md)
