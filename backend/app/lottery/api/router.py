from fastapi import APIRouter

from backend.app.lottery.api.v1 import analysis, combination, draw_result, lottery_type, prediction
from backend.core.conf import settings

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/lottery', tags=['彩票系统'])

v1.include_router(lottery_type.router, prefix='/lottery-type', tags=['彩种管理'])
v1.include_router(draw_result.router, prefix='/draw', tags=['开奖数据'])
v1.include_router(analysis.router, prefix='/analysis', tags=['分析方法'])
v1.include_router(prediction.router, prefix='/prediction', tags=['预测管理'])
v1.include_router(combination.router, prefix='/combination', tags=['组合管理'])

