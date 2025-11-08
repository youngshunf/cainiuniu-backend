from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class LotteryTypeBase(SchemaBase):
    """彩票类型基础"""

    code: str = Field(description='彩种代码')
    name: str = Field(description='彩种名称')
    category: str = Field(description='类别')
    red_ball_count: int = Field(description='红球数量')
    blue_ball_count: int = Field(default=0, description='蓝球数量')
    red_ball_range: str = Field(description='红球范围')
    blue_ball_range: str | None = Field(default=None, description='蓝球范围')
    draw_time: str = Field(description='开奖时间规则')
    api_url: str = Field(description='官方API地址')
    web_url: str = Field(description='官方网页地址')
    game_no: str | None = Field(default=None, description='体彩游戏编号')


class AddLotteryTypeParam(LotteryTypeBase):
    """添加彩票类型"""

    pass


class UpdateLotteryTypeParam(SchemaBase):
    """更新彩票类型"""

    name: str | None = None
    draw_time: str | None = None
    api_url: str | None = None
    web_url: str | None = None
    game_no: str | None = None
    status: int | None = None


class GetLotteryTypeListDetails(LotteryTypeBase):
    """彩票类型列表详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: int
    created_time: datetime
    updated_time: datetime | None

