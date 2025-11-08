from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class MembershipPlanBase(SchemaBase):
    """会员套餐基础"""

    name: str = Field(description='套餐名称')
    price: Decimal = Field(description='价格')
    duration_days: int = Field(description='有效天数')
    features: str = Field(description='功能权限JSON')
    max_predictions_per_day: int = Field(description='每日最大预测次数')
    max_custom_combinations: int = Field(description='最大自定义组合数')
    can_use_ml_methods: bool = Field(default=False, description='是否可使用机器学习方法')
    can_use_api: bool = Field(default=False, description='是否可使用API')
    api_quota_per_day: int = Field(default=0, description='API每日配额')


class AddMembershipPlanParam(MembershipPlanBase):
    """添加会员套餐"""

    pass


class UpdateMembershipPlanParam(SchemaBase):
    """更新会员套餐"""

    name: str | None = None
    price: Decimal | None = None
    duration_days: int | None = None
    features: str | None = None
    max_predictions_per_day: int | None = None
    max_custom_combinations: int | None = None
    can_use_ml_methods: bool | None = None
    can_use_api: bool | None = None
    api_quota_per_day: int | None = None
    sort_order: int | None = None
    status: int | None = None


class GetMembershipPlanListDetails(MembershipPlanBase):
    """会员套餐列表详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sort_order: int
    status: int
    created_time: datetime
    updated_time: datetime | None


class UserMembershipBase(SchemaBase):
    """用户会员基础"""

    user_id: int = Field(description='用户ID')
    plan_id: int = Field(description='套餐ID')
    start_date: datetime = Field(description='开始日期')
    end_date: datetime = Field(description='结束日期')


class AddUserMembershipParam(UserMembershipBase):
    """添加用户会员"""

    auto_renew: bool = Field(default=False, description='是否自动续费')


class GetUserMembershipDetails(UserMembershipBase):
    """用户会员详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    auto_renew: bool
    remaining_predictions_today: int
    remaining_api_quota_today: int
    created_time: datetime
    updated_time: datetime | None

