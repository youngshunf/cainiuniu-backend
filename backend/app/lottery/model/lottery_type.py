from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.lottery.model import DrawResult


class LotteryType(Base):
    """彩票类型表"""

    __tablename__ = 'l_lottery_type'

    id: Mapped[id_key] = mapped_column(init=False)
    code: Mapped[str] = mapped_column(sa.String(20), unique=True, index=True, comment='彩种代码')
    name: Mapped[str] = mapped_column(sa.String(50), comment='彩种名称')
    category: Mapped[str] = mapped_column(sa.String(20), comment='类别(福彩/体彩)')
    red_ball_count: Mapped[int] = mapped_column(comment='红球数量')
    red_ball_range: Mapped[str] = mapped_column(sa.String(20), comment='红球范围')
    draw_time: Mapped[str] = mapped_column(sa.String(100), comment='开奖时间规则')
    api_url: Mapped[str] = mapped_column(sa.String(500), comment='官方API地址')
    web_url: Mapped[str] = mapped_column(sa.String(500), comment='官方网页地址')
    blue_ball_count: Mapped[int] = mapped_column(default=0, comment='蓝球数量')
    blue_ball_range: Mapped[str | None] = mapped_column(sa.String(20), default=None, comment='蓝球范围')
    game_no: Mapped[str | None] = mapped_column(sa.String(20), default=None, comment='体彩游戏编号')
    status: Mapped[int] = mapped_column(default=1, comment='状态(0停用 1启用)')

    # 关联开奖结果
    draw_results: Mapped[list[DrawResult]] = relationship(init=False, back_populates='lottery_type')

