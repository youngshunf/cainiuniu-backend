from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class AnalysisMethodBase(SchemaBase):
    """分析方法基础"""

    code: str = Field(description='方法代码')
    name: str = Field(description='方法名称')
    category: str = Field(description='分类')
    description: str = Field(description='方法描述')
    algorithm_type: str = Field(description='算法类型')
    applicable_lotteries: str = Field(description='适用彩种JSON')
    default_params: str | None = Field(default=None, description='默认参数JSON')
    required_history_count: int = Field(default=30, description='所需最少历史期数')
    complexity: str = Field(default='low', description='计算复杂度')
    is_premium: bool = Field(default=False, description='是否高级功能')


class AddMethodParam(AnalysisMethodBase):
    """添加分析方法"""

    pass


class UpdateMethodParam(SchemaBase):
    """更新分析方法"""

    name: str | None = None
    description: str | None = None
    applicable_lotteries: str | None = None
    default_params: str | None = None
    required_history_count: int | None = None
    complexity: str | None = None
    is_premium: bool | None = None
    status: int | None = None


class GetMethodListDetails(AnalysisMethodBase):
    """分析方法列表详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: int
    created_time: datetime
    updated_time: datetime | None

