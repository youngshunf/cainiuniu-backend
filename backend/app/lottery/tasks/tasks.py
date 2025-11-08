"""彩票分析Celery任务入口"""

# 导入所有任务以便Celery自动发现
from backend.app.lottery.tasks.prediction_tasks import (  # noqa: F401
    calculate_combination_accuracy,
    daily_auto_prediction,
    reset_daily_quota,
    verify_predictions,
)
from backend.app.lottery.tasks.sync_tasks import (  # noqa: F401
    sync_all_history,
    sync_latest_draw,
    sync_single_lottery,
)

__all__ = [
    # 同步任务
    'sync_latest_draw',
    'sync_single_lottery',
    'sync_all_history',
    # 预测任务
    'daily_auto_prediction',
    'verify_predictions',
    'reset_daily_quota',
    'calculate_combination_accuracy',
]

