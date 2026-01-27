from fastapi import APIRouter

from backend.app.projects.api.v1.project_topics import router as project_topics_router
from backend.app.projects.api.v1.projects import router as projects_router
from backend.core.conf import settings

v1 = APIRouter(prefix=settings.FASTAPI_API_V1_PATH, tags=['项目私有选题'])

v1.include_router(projects_router, prefix='/projectss')
v1.include_router(project_topics_router, prefix='/project/topicss')
