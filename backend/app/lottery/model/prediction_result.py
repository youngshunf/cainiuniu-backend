from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, TimeZone, UniversalText, id_key


class PredictionResult(Base):
    """预测结果表"""

    __tablename__ = 'l_prediction_result'

    id: Mapped[id_key] = mapped_column(init=False)
    lottery_code: Mapped[str] = mapped_column(sa.String(20), index=True, comment='彩种代码')
    target_period: Mapped[str] = mapped_column(sa.String(20), index=True, comment='目标期号')
    method_details: Mapped[str] = mapped_column(UniversalText, comment='各方法分析详情JSON')
    predicted_numbers: Mapped[str] = mapped_column(UniversalText, comment='预测号码组合JSON')
    analysis_article: Mapped[str] = mapped_column(UniversalText, comment='分析文章(富文本)')
    combination_id: Mapped[int | None] = mapped_column(
        sa.BigInteger, default=None, comment='使用的组合ID'
    )
    user_id: Mapped[int | None] = mapped_column(sa.BigInteger, default=None, comment='用户ID')
    confidence_score: Mapped[float | None] = mapped_column(
        sa.Float, default=None, comment='置信度'
    )
    actual_result: Mapped[str | None] = mapped_column(
        sa.String(200), default=None, comment='实际开奖结果JSON'
    )
    hit_count: Mapped[int | None] = mapped_column(default=None, comment='命中个数')
    is_verified: Mapped[bool] = mapped_column(default=False, comment='是否已验证')
    verify_time: Mapped[datetime | None] = mapped_column(
        TimeZone, init=False, default=None, comment='验证时间'
    )

    __table_args__ = (
        sa.Index('ix_lottery_period', 'lottery_code', 'target_period'),
        {'comment': '预测结果表'},
    )

