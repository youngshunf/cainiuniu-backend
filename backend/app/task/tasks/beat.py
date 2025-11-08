from celery.schedules import schedule

from backend.app.task.utils.tzcrontab import TzAwareCrontab

# 参考：https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
LOCAL_BEAT_SCHEDULE = {
    '测试同步任务': {
        'task': 'task_demo',
        'schedule': schedule(30),
    },
    '测试异步任务': {
        'task': 'task_demo_async',
        'schedule': TzAwareCrontab('1'),
    },
    '测试传参任务': {
        'task': 'task_demo_params',
        'schedule': TzAwareCrontab('1'),
        'args': ['你好，'],
        'kwargs': {'world': '世界'},
    },
    '清理操作日志': {
        'task': 'backend.app.task.tasks.db_log.tasks.delete_db_opera_log',
        'schedule': TzAwareCrontab('0', '0', day_of_week='6'),
    },
    '清理登录日志': {
        'task': 'backend.app.task.tasks.db_log.tasks.delete_db_login_log',
        'schedule': TzAwareCrontab('0', '0', day_of_month='15'),
    },
    # 彩票数据同步任务
    '每日同步最新开奖': {
        'task': 'lottery.sync_latest_draw',
        'schedule': TzAwareCrontab('30', '21'),  # 每天21:30执行
    },
    # 彩票预测任务
    '每日自动预测': {
        'task': 'lottery.daily_auto_prediction',
        'schedule': TzAwareCrontab('0', '9'),  # 每天09:00执行
    },
    '验证预测结果': {
        'task': 'lottery.verify_predictions',
        'schedule': TzAwareCrontab('0', '22'),  # 每天22:00执行
    },
    '重置每日配额': {
        'task': 'lottery.reset_daily_quota',
        'schedule': TzAwareCrontab('0', '0'),  # 每天00:00执行
    },
    '计算组合准确率': {
        'task': 'lottery.calculate_combination_accuracy',
        'schedule': TzAwareCrontab('0', '23'),  # 每天23:00执行
    },
}
