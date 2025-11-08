"""尾数和值分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class TailSumAnalyzer(BaseAnalyzer):
    """尾数和值分析器"""

    def get_tail(self, num: int) -> int:
        """获取号码尾数"""
        return num % 10

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析尾数和值

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 尾数和值分析结果
        """
        tail_sums = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = [int(num) for num in red_balls]
            tails = [self.get_tail(num) for num in numbers]
            tail_sum = sum(tails)
            tail_sums.append(tail_sum)
        
        # 统计尾数和值频率
        tail_sum_counter = Counter(tail_sums)
        
        # 计算统计指标
        avg_tail_sum = sum(tail_sums) / len(tail_sums)
        max_tail_sum = max(tail_sums)
        min_tail_sum = min(tail_sums)
        
        return {
            'tail_sum_frequency': dict(tail_sum_counter.most_common()),
            'most_common_tail_sums': [ts for ts, _ in tail_sum_counter.most_common(10)],
            'avg_tail_sum': round(avg_tail_sum, 2),
            'max_tail_sum': max_tail_sum,
            'min_tail_sum': min_tail_sum,
            'tail_sums': tail_sums,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于尾数和值预测

        :param analysis_result: 分析结果
        :param params: 参数
        """
        most_common_tail_sums = analysis_result.get('most_common_tail_sums', [])
        avg_tail_sum = analysis_result.get('avg_tail_sum', 25)
        
        return {
            'recommended_tail_sums': most_common_tail_sums[:5],
            'avg_tail_sum': avg_tail_sum,
            'method': 'tail_sum',
            'confidence': 0.55,
        }

