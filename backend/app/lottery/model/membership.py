from __future__ import annotations

from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, TimeZone, UniversalText, id_key


class MembershipPlan(Base):
    """会员套餐表"""

    __tablename__ = 'l_membership_plan'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(50), unique=True, comment='套餐名称')
    price: Mapped[Decimal] = mapped_column(sa.Numeric(10, 2), comment='价格')
    duration_days: Mapped[int] = mapped_column(comment='有效天数')
    features: Mapped[str] = mapped_column(UniversalText, comment='功能权限JSON')
    max_predictions_per_day: Mapped[int] = mapped_column(comment='每日最大预测次数')
    max_custom_combinations: Mapped[int] = mapped_column(comment='最大自定义组合数')
    can_use_ml_methods: Mapped[bool] = mapped_column(default=False, comment='是否可使用机器学习方法')
    can_use_api: Mapped[bool] = mapped_column(default=False, comment='是否可使用API')
    api_quota_per_day: Mapped[int] = mapped_column(default=0, comment='API每日配额')
    sort_order: Mapped[int] = mapped_column(default=0, comment='排序')
    status: Mapped[int] = mapped_column(default=1, comment='状态(0停用 1启用)')


class UserMembership(Base):
    """用户会员表"""

    __tablename__ = 'l_user_membership'

    id: Mapped[id_key] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, index=True, comment='用户ID')
    plan_id: Mapped[int] = mapped_column(sa.BigInteger, comment='套餐ID')
    start_date: Mapped[datetime] = mapped_column(TimeZone, comment='开始日期')
    end_date: Mapped[datetime] = mapped_column(TimeZone, comment='结束日期')
    is_active: Mapped[bool] = mapped_column(default=True, comment='是否激活')
    auto_renew: Mapped[bool] = mapped_column(default=False, comment='是否自动续费')
    remaining_predictions_today: Mapped[int] = mapped_column(default=0, comment='今日剩余预测次数')
    remaining_api_quota_today: Mapped[int] = mapped_column(default=0, comment='今日剩余API配额')

