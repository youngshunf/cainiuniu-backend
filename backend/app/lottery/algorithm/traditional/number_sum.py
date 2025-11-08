"""号码和分布分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class NumberSumAnalyzer(BaseAnalyzer):
    """号码和分布分析器（任意两个号码之和的分布）"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析号码两两之和的分布

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 号码和分布分析结果
        """
        pair_sums = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = [int(num) for num in red_balls]
            
            # 计算所有两两之和
            for i in range(len(numbers)):
                for j in range(i + 1, len(numbers)):
                    pair_sum = numbers[i] + numbers[j]
                    pair_sums.append(pair_sum)
        
        # 统计和值频率
        sum_counter = Counter(pair_sums)
        
        # 计算统计指标
        avg_pair_sum = sum(pair_sums) / len(pair_sums)
        
        return {
            'pair_sum_frequency': dict(sum_counter.most_common(20)),
            'most_common_pair_sums': [ps for ps, _ in sum_counter.most_common(15)],
            'avg_pair_sum': round(avg_pair_sum, 2),
            'total_pairs': len(pair_sums),
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于号码和分布预测

        :param analysis_result: 分析结果
        :param params: 参数
        """
        most_common_pair_sums = analysis_result.get('most_common_pair_sums', [])
        
        return {
            'recommended_pair_sums': most_common_pair_sums[:10],
            'method': 'number_sum',
            'confidence': 0.5,
        }

