from __future__ import annotations

from datetime import date, datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, TimeZone, UniversalText, id_key

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.lottery.model import LotteryType


class DrawResult(Base):
    """开奖结果表"""

    __tablename__ = 'l_draw_result'

    id: Mapped[id_key] = mapped_column(init=False)
    lottery_type_id: Mapped[int] = mapped_column(
        sa.BigInteger, sa.ForeignKey('l_lottery_type.id'), comment='彩种ID'
    )
    lottery_code: Mapped[str] = mapped_column(sa.String(20), index=True, comment='彩种代码')
    period: Mapped[str] = mapped_column(sa.String(20), index=True, comment='期号')
    draw_date: Mapped[date] = mapped_column(sa.Date, index=True, comment='开奖日期')
    red_balls: Mapped[str] = mapped_column(sa.String(200), comment='红球号码JSON')
    blue_balls: Mapped[str | None] = mapped_column(sa.String(100), default=None, comment='蓝球号码JSON')
    extra_info: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='额外信息JSON')
    sync_source: Mapped[str] = mapped_column(sa.String(20), default='api', comment='数据来源')
    is_verified: Mapped[bool] = mapped_column(default=True, comment='是否已验证')
    sync_time: Mapped[datetime] = mapped_column(
        TimeZone, init=False, default=None, comment='同步时间'
    )

    # 关联彩票类型
    lottery_type: Mapped[LotteryType] = relationship(init=False, back_populates='draw_results')

    __table_args__ = (
        sa.UniqueConstraint('lottery_code', 'period', name='uk_lottery_period'),
        {'comment': '开奖结果表'},
    )

