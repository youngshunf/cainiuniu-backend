#!/usr/bin/env bash

# 使用 uv 环境启动 Celery 服务
cd "$(dirname "$0")"

echo "启动 Celery Worker..."
uv run fba celery worker > /tmp/celery_worker.log 2>&1 &
WORKER_PID=$!
echo "Worker PID: $WORKER_PID"

sleep 2

echo "启动 Celery Beat..."
uv run fba celery beat > /tmp/celery_beat.log 2>&1 &
BEAT_PID=$!
echo "Beat PID: $BEAT_PID"

sleep 2

echo "启动 Celery Flower..."
uv run fba celery flower > /tmp/celery_flower.log 2>&1 &
FLOWER_PID=$!
echo "Flower PID: $FLOWER_PID"

echo ""
echo "✅ Celery 服务已启动！"
echo ""
echo "📊 Flower 监控: http://127.0.0.1:5555"
echo ""
echo "日志文件:"
echo "  - Worker: /tmp/celery_worker.log"
echo "  - Beat: /tmp/celery_beat.log"
echo "  - Flower: /tmp/celery_flower.log"
echo ""
echo "查看日志: tail -f /tmp/celery_worker.log"
echo "停止服务: pkill -f 'fba celery'"

