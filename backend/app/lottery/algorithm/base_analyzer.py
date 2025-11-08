"""分析器基类"""

from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    """分析器基类"""

    def __init__(self, lottery_code: str):
        self.lottery_code = lottery_code

    @abstractmethod
    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析历史数据

        :param history_data: 历史开奖数据列表
        :param params: 分析参数
        :return: 分析结果
        """
        pass

    @abstractmethod
    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于分析结果预测号码

        :param analysis_result: 分析结果
        :param params: 预测参数
        :return: 推荐号码列表
        """
        pass

    def get_red_balls(self, draw_result: dict) -> list[str]:
        """
        获取红球号码

        :param draw_result: 开奖结果
        :return: 红球列表
        """
        import json
        return json.loads(draw_result.get('red_balls', '[]'))

    def get_blue_balls(self, draw_result: dict) -> list[str] | None:
        """
        获取蓝球号码

        :param draw_result: 开奖结果
        :return: 蓝球列表
        """
        import json
        blue_balls_str = draw_result.get('blue_balls')
        return json.loads(blue_balls_str) if blue_balls_str else None

    def is_number_lottery(self) -> bool:
        """判断是否为数字型彩票（如3D、排列三）"""
        return self.lottery_code in ['3d', 'pls', 'plw', 'qxc']

