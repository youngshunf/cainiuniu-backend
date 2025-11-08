from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class PredictionBase(SchemaBase):
    """预测基础"""

    lottery_code: str = Field(description='彩种代码')
    target_period: str = Field(description='目标期号')
    combination_id: int | None = Field(default=None, description='使用的组合ID')
    method_details: str = Field(description='各方法分析详情JSON')
    predicted_numbers: str = Field(description='预测号码组合JSON')
    analysis_article: str = Field(description='分析文章')
    confidence_score: float | None = Field(default=None, description='置信度')


class AddPredictionParam(PredictionBase):
    """添加预测"""

    pass


class UpdatePredictionParam(SchemaBase):
    """更新预测"""

    actual_result: str | None = None
    hit_count: int | None = None
    is_verified: bool | None = None


class GetPredictionListDetails(PredictionBase):
    """预测列表详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    actual_result: str | None
    hit_count: int | None
    is_verified: bool
    verify_time: datetime | None
    created_time: datetime
    updated_time: datetime | None

