"""机器学习分析器基类"""

from abc import abstractmethod

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class BaseMLAnalyzer(BaseAnalyzer):
    """机器学习分析器基类"""

    def __init__(self, lottery_code: str):
        super().__init__(lottery_code)
        self.model = None
        self.model_path = None

    @abstractmethod
    async def train_model(self, history_data: list, params: dict | None = None) -> dict:
        """
        训练模型

        :param history_data: 历史数据
        :param params: 训练参数
        :return: 训练结果
        """
        pass

    @abstractmethod
    async def load_model(self, model_path: str) -> None:
        """
        加载已训练的模型

        :param model_path: 模型路径
        """
        pass

    @abstractmethod
    async def save_model(self, model_path: str) -> None:
        """
        保存模型

        :param model_path: 模型路径
        """
        pass

    def preprocess_data(self, history_data: list) -> tuple:
        """
        数据预处理

        :param history_data: 历史数据
        :return: (特征, 标签)
        """
        # 子类实现具体的预处理逻辑
        pass

    def evaluate_model(self, test_data: list) -> dict:
        """
        评估模型

        :param test_data: 测试数据
        :return: 评估指标
        """
        # 子类实现具体的评估逻辑
        pass

