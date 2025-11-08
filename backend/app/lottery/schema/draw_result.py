from datetime import date, datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class DrawResultBase(SchemaBase):
    """开奖结果基础"""

    lottery_code: str = Field(description='彩种代码')
    period: str = Field(description='期号')
    draw_date: date = Field(description='开奖日期')
    red_balls: str = Field(description='红球号码JSON')
    blue_balls: str | None = Field(default=None, description='蓝球号码JSON')
    extra_info: str | None = Field(default=None, description='额外信息JSON')


class AddDrawResultParam(DrawResultBase):
    """添加开奖结果"""

    lottery_type_id: int = Field(description='彩种ID')
    sync_source: str = Field(default='manual', description='数据来源')


class UpdateDrawResultParam(SchemaBase):
    """更新开奖结果"""

    red_balls: str | None = None
    blue_balls: str | None = None
    extra_info: str | None = None
    is_verified: bool | None = None


class GetDrawResultListDetails(DrawResultBase):
    """开奖结果列表详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    lottery_type_id: int
    sync_source: str
    is_verified: bool
    sync_time: datetime | None
    created_time: datetime
    updated_time: datetime | None

