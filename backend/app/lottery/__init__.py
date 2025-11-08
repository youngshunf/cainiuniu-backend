"""彩票分析预测模块"""

# 导入所有model以便Alembic检测
from backend.app.lottery.model import (  # noqa: F401
    AnalysisCombination,
    AnalysisMethod,
    ApiUsage,
    DrawResult,
    LotteryType,
    MembershipPlan,
    PredictionResult,
    UserMembership,
)

__all__ = [
    'LotteryType',
    'DrawResult',
    'AnalysisMethod',
    'AnalysisCombination',
    'PredictionResult',
    'MembershipPlan',
    'UserMembership',
    'ApiUsage',
]

