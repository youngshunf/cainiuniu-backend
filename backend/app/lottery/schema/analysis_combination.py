from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class CombinationBase(SchemaBase):
    """组合基础"""

    name: str = Field(description='组合名称')
    lottery_code: str = Field(description='适用彩种')
    method_configs: str = Field(description='方法配置JSON')
    history_periods: int = Field(default=100, description='历史期数')
    is_auto: bool = Field(default=False, description='是否自动预测')


class AddCombinationParam(CombinationBase):
    """添加组合"""

    pass


class UpdateCombinationParam(SchemaBase):
    """更新组合"""

    name: str | None = None
    method_configs: str | None = None
    history_periods: int | None = None
    is_auto: bool | None = None
    status: int | None = None


class GetCombinationListDetails(CombinationBase):
    """组合列表详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    accuracy_rate: float | None
    use_count: int
    status: int
    created_time: datetime
    updated_time: datetime | None

