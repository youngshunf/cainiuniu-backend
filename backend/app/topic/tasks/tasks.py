from backend.database.db import async_db_session
from backend.app.task.celery import celery_app
from backend.app.topic.service.topic_service import TopicService


@celery_app.task(name='daily_topic_recommendation_task')
async def daily_topic_recommendation_task() -> str:
    """每日选题推荐生成任务"""
    async with async_db_session() as db:
        result = await TopicService.generate_daily_topics(db)
        return f"Generated {result['generated']} topics. Errors: {len(result['errors'])}"
