"""连号分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class ConsecutiveAnalyzer(BaseAnalyzer):
    """连号分析器"""

    def find_consecutive_groups(self, numbers: list[int]) -> list[list[int]]:
        """
        查找连号组合
        
        :param numbers: 号码列表
        :return: 连号组合列表
        """
        if not numbers:
            return []
        
        sorted_numbers = sorted(numbers)
        consecutive_groups = []
        current_group = [sorted_numbers[0]]
        
        for i in range(1, len(sorted_numbers)):
            if sorted_numbers[i] == sorted_numbers[i-1] + 1:
                current_group.append(sorted_numbers[i])
            else:
                if len(current_group) >= 2:
                    consecutive_groups.append(current_group)
                current_group = [sorted_numbers[i]]
        
        if len(current_group) >= 2:
            consecutive_groups.append(current_group)
        
        return consecutive_groups

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析连号出现规律

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 连号分析结果
        """
        consecutive_counts = []
        consecutive_max_lengths = []
        has_consecutive_count = 0
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = [int(num) for num in red_balls]
            consecutive_groups = self.find_consecutive_groups(numbers)
            
            if consecutive_groups:
                has_consecutive_count += 1
                total_consecutive = sum(len(group) for group in consecutive_groups)
                max_length = max(len(group) for group in consecutive_groups)
                consecutive_counts.append(total_consecutive)
                consecutive_max_lengths.append(max_length)
            else:
                consecutive_counts.append(0)
                consecutive_max_lengths.append(0)
        
        # 统计连号长度频率
        length_counter = Counter(consecutive_max_lengths)
        
        # 连号出现概率
        consecutive_probability = has_consecutive_count / len(history_data)
        
        return {
            'consecutive_probability': round(consecutive_probability, 4),
            'length_frequency': dict(length_counter.most_common()),
            'avg_consecutive_count': round(sum(consecutive_counts) / len(consecutive_counts), 2),
            'consecutive_counts': consecutive_counts,
            'max_lengths': consecutive_max_lengths,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于连号分析预测

        :param analysis_result: 分析结果
        :param params: 参数
        """
        consecutive_probability = analysis_result.get('consecutive_probability', 0)
        avg_count = analysis_result.get('avg_consecutive_count', 0)
        
        return {
            'has_consecutive': consecutive_probability > 0.5,
            'consecutive_probability': consecutive_probability,
            'expected_consecutive_count': int(avg_count),
            'method': 'consecutive',
            'confidence': 0.5,
        }

