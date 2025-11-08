#!/usr/bin/env bash

# 使用 uv 环境启动 FastAPI 服务
cd "$(dirname "$0")"

echo "🚀 启动 FastAPI 服务..."
uv run fba run

