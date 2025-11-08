"""同尾号分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class SameTailAnalyzer(BaseAnalyzer):
    """同尾号分析器"""

    def get_tail(self, num: int) -> int:
        """获取号码尾数"""
        return num % 10

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析同尾号分布

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 同尾号分析结果
        """
        tail_patterns = []
        same_tail_counts = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = [int(num) for num in red_balls]
            tails = [self.get_tail(num) for num in numbers]
            
            # 统计各尾数出现次数
            tail_counter = Counter(tails)
            
            # 同尾号个数（尾数出现次数>1的）
            same_tail_count = sum(1 for count in tail_counter.values() if count > 1)
            same_tail_counts.append(same_tail_count)
            
            # 记录尾数模式
            tail_pattern = '-'.join(str(tail) for tail in sorted(tails))
            tail_patterns.append(tail_pattern)
        
        # 统计同尾号个数频率
        same_tail_counter = Counter(same_tail_counts)
        
        # 统计各尾数出现频率
        all_tails = []
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = [int(num) for num in red_balls]
            tails = [self.get_tail(num) for num in numbers]
            all_tails.extend(tails)
        
        tail_frequency = Counter(all_tails)
        
        return {
            'same_tail_count_frequency': dict(same_tail_counter.most_common()),
            'avg_same_tail_count': round(sum(same_tail_counts) / len(same_tail_counts), 2),
            'tail_frequency': dict(tail_frequency.most_common()),
            'hot_tails': [tail for tail, _ in tail_frequency.most_common(5)],
            'same_tail_counts': same_tail_counts,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于同尾号分析预测

        :param analysis_result: 分析结果
        :param params: 参数
        """
        hot_tails = analysis_result.get('hot_tails', [])
        avg_same_tail_count = int(analysis_result.get('avg_same_tail_count', 1))
        
        return {
            'recommended_tails': hot_tails,
            'expected_same_tail_count': avg_same_tail_count,
            'method': 'same_tail',
            'confidence': 0.5,
        }

