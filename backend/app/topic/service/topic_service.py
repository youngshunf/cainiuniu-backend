import hashlib
import random

from collections.abc import Sequence
from datetime import date

from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.llm.core.gateway import llm_gateway
from backend.app.topic.model.topic import Topic
from backend.app.topic.schema.topic import CreateTopicParam, UpdateTopicParam
from backend.app.topic.service.industry_service import IndustryService
from backend.common.exception import errors
from backend.core.conf import settings


class TopicService:
    @staticmethod
    async def get(db: AsyncSession, id: int) -> Topic | None:
        """获取单个选题"""
        return await db.get(Topic, id)

    @staticmethod
    async def create(db: AsyncSession, obj: CreateTopicParam) -> Topic:
        """创建选题"""
        topic = Topic(**obj.model_dump())
        db.add(topic)
        await db.commit()
        await db.refresh(topic)
        return topic

    @staticmethod
    async def update(db: AsyncSession, id: int, obj: UpdateTopicParam) -> Topic:
        """更新选题"""
        topic = await TopicService.get(db, id)
        if not topic:
            raise errors.NotFoundError(msg='选题不存在')

        update_data = obj.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(topic, key, value)

        await db.commit()
        await db.refresh(topic)
        return topic

    @staticmethod
    async def delete(db: AsyncSession, id: int) -> None:
        """删除选题"""
        topic = await TopicService.get(db, id)
        if not topic:
            raise errors.NotFoundError(msg='选题不存在')

        await db.delete(topic)
        await db.commit()

    @staticmethod
    async def get_recommendations(
        db: AsyncSession,
        industry_id: int | None = None,
        limit: int = 20
    ) -> Sequence[Topic]:
        """获取推荐选题列表"""
        stmt = select(Topic).where(Topic.status == 0)

        if industry_id:
            stmt = stmt.where(Topic.industry_id == industry_id)

        stmt = stmt.order_by(desc(Topic.potential_score)).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def generate_daily_topics(db: AsyncSession) -> dict:
        """生成每日选题（核心任务逻辑）"""
        # 功能已禁用：缺少 agent_core
        return {"status": "skipped", "message": "agent_core dependency missing"}
