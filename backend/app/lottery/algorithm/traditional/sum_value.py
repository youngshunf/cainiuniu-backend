"""和值分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class SumValueAnalyzer(BaseAnalyzer):
    """和值分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析号码和值

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 和值分析结果
        """
        sum_values = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            sum_value = sum(int(num) for num in red_balls)
            sum_values.append(sum_value)
        
        # 统计和值频率
        sum_counter = Counter(sum_values)
        
        # 计算统计指标
        avg_sum = sum(sum_values) / len(sum_values)
        max_sum = max(sum_values)
        min_sum = min(sum_values)
        
        # 和值分布区间
        ranges = {
            '低': (min_sum, int(avg_sum * 0.8)),
            '中': (int(avg_sum * 0.8), int(avg_sum * 1.2)),
            '高': (int(avg_sum * 1.2), max_sum),
        }
        
        range_counts = {'低': 0, '中': 0, '高': 0}
        for sv in sum_values:
            if sv <= ranges['低'][1]:
                range_counts['低'] += 1
            elif sv <= ranges['中'][1]:
                range_counts['中'] += 1
            else:
                range_counts['高'] += 1
        
        return {
            'sum_frequency': dict(sum_counter.most_common(20)),
            'avg_sum': round(avg_sum, 2),
            'max_sum': max_sum,
            'min_sum': min_sum,
            'sum_values': sum_values,
            'ranges': ranges,
            'range_counts': range_counts,
            'most_common_sums': [sv for sv, _ in sum_counter.most_common(10)],
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于和值预测

        :param analysis_result: 分析结果
        :param params: 参数（可选：target_range='低'/'中'/'高'）
        """
        if not params:
            params = {}
        
        target_range = params.get('target_range', '中')
        ranges = analysis_result.get('ranges', {})
        target_min, target_max = ranges.get(target_range, (0, 100))
        
        # 推荐和值范围
        recommended_sum_range = (target_min, target_max)
        
        # 从历史最常见的和值中选择
        most_common_sums = analysis_result.get('most_common_sums', [])
        recommended_sums = [s for s in most_common_sums if target_min <= s <= target_max][:3]
        
        return {
            'recommended_sum_range': recommended_sum_range,
            'recommended_sums': recommended_sums,
            'target_range': target_range,
            'method': 'sum_value',
            'confidence': 0.65,
        }

