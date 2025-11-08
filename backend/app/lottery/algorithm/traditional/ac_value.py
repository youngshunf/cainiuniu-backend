"""AC值分析算法"""

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class ACValueAnalyzer(BaseAnalyzer):
    """AC值分析器（算术复杂性）"""

    def calculate_ac_value(self, numbers: list[int]) -> int:
        """
        计算AC值
        
        AC值 = 号码两两之差的绝对值的不重复个数 - (号码个数 - 1)
        
        :param numbers: 号码列表
        :return: AC值
        """
        if len(numbers) < 2:
            return 0
        
        diffs = set()
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                diff = abs(numbers[i] - numbers[j])
                diffs.add(diff)
        
        ac_value = len(diffs) - (len(numbers) - 1)
        return ac_value

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析AC值分布

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: AC值分析结果
        """
        from collections import Counter
        
        ac_values = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = sorted([int(num) for num in red_balls])
            ac_value = self.calculate_ac_value(numbers)
            ac_values.append(ac_value)
        
        # 统计AC值频率
        ac_counter = Counter(ac_values)
        
        # 计算统计指标
        avg_ac = sum(ac_values) / len(ac_values)
        max_ac = max(ac_values)
        min_ac = min(ac_values)
        
        return {
            'ac_frequency': dict(ac_counter.most_common()),
            'most_common_ac': ac_counter.most_common(1)[0] if ac_counter else None,
            'avg_ac': round(avg_ac, 2),
            'max_ac': max_ac,
            'min_ac': min_ac,
            'ac_values': ac_values,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于AC值预测

        :param analysis_result: 分析结果
        :param params: 参数（可选：target_ac）
        """
        if not params:
            params = {}
        
        # 获取最常见的AC值
        most_common = analysis_result.get('most_common_ac')
        target_ac = params.get('target_ac', most_common[0] if most_common else int(analysis_result.get('avg_ac', 5)))
        
        return {
            'target_ac_value': target_ac,
            'avg_ac': analysis_result.get('avg_ac', 0),
            'method': 'ac_value',
            'confidence': 0.55,
        }

