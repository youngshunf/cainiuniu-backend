from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class UserSubscriptionSchemaBase(SchemaBase):
    """用户订阅基础模型"""
    user_id: int = Field(description='用户 ID')
    tier: str = Field(description='订阅等级 (free:免费版/basic:基础版/pro:专业版/enterprise:企业版)')
    monthly_credits: Decimal = Field(description='每月积分配额')
    current_credits: Decimal = Field(description='当前剩余积分')
    used_credits: Decimal = Field(description='本周期已使用积分')
    purchased_credits: Decimal = Field(description='购买的额外积分')
    billing_cycle_start: datetime = Field(description='计费周期开始时间')
    billing_cycle_end: datetime = Field(description='计费周期结束时间')
    status: str = Field(description='订阅状态 (active:激活/expired:已过期/cancelled:已取消)')
    auto_renew: bool = Field(description='是否自动续费')


class CreateUserSubscriptionParam(UserSubscriptionSchemaBase):
    """创建用户订阅参数"""


class UpdateUserSubscriptionParam(UserSubscriptionSchemaBase):
    """更新用户订阅参数"""


class DeleteUserSubscriptionParam(SchemaBase):
    """删除用户订阅参数"""

    pks: list[int] = Field(description='用户订阅 ID 列表')


class GetUserSubscriptionDetail(UserSubscriptionSchemaBase):
    """用户订阅详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
