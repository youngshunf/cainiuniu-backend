"""邻号分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class AdjacentAnalyzer(BaseAnalyzer):
    """邻号分析器（与上期号码相邻的号码）"""

    def get_adjacent_numbers(self, numbers: list[str]) -> set[str]:
        """
        获取号码的邻号（±1）
        
        :param numbers: 号码列表
        :return: 邻号集合
        """
        adjacent = set()
        for num_str in numbers:
            num = int(num_str)
            if num > 1:
                adjacent.add(str(num - 1).zfill(2))
            if num < 99:  # 假设最大号码为99
                adjacent.add(str(num + 1).zfill(2))
        return adjacent

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析邻号规律

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 邻号分析结果
        """
        adjacent_counts = []
        adjacent_numbers_list = []
        has_adjacent_count = 0
        
        for i in range(1, len(history_data)):
            prev_draw = history_data[i]
            curr_draw = history_data[i-1]
            
            prev_balls = self.get_red_balls(prev_draw)
            curr_balls = set(self.get_red_balls(curr_draw))
            
            # 获取上期号码的邻号
            adjacent_nums = self.get_adjacent_numbers(prev_balls)
            
            # 计算本期出现的邻号
            appeared_adjacent = adjacent_nums & curr_balls
            adjacent_count = len(appeared_adjacent)
            
            adjacent_counts.append(adjacent_count)
            adjacent_numbers_list.append(list(appeared_adjacent))
            
            if adjacent_count > 0:
                has_adjacent_count += 1
        
        # 统计邻号个数频率
        adjacent_counter = Counter(adjacent_counts)
        
        # 邻号出现概率
        adjacent_probability = has_adjacent_count / len(adjacent_counts) if adjacent_counts else 0
        avg_adjacent_count = sum(adjacent_counts) / len(adjacent_counts) if adjacent_counts else 0
        
        return {
            'adjacent_probability': round(adjacent_probability, 4),
            'adjacent_count_frequency': dict(adjacent_counter.most_common()),
            'avg_adjacent_count': round(avg_adjacent_count, 2),
            'adjacent_counts': adjacent_counts,
            'adjacent_numbers_list': adjacent_numbers_list,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于邻号分析预测

        :param analysis_result: 分析结果
        :param params: 参数（需要提供上期号码）
        """
        if not params or 'prev_numbers' not in params:
            return {
                'method': 'adjacent',
                'confidence': 0.55,
                'note': '需要提供上期号码',
            }
        
        prev_numbers = params.get('prev_numbers', [])
        avg_adjacent_count = int(analysis_result.get('avg_adjacent_count', 2))
        
        # 获取所有邻号
        adjacent_nums = list(self.get_adjacent_numbers(prev_numbers))
        
        return {
            'potential_adjacent_numbers': adjacent_nums[:avg_adjacent_count * 2] if adjacent_nums else [],
            'expected_adjacent_count': avg_adjacent_count,
            'adjacent_probability': analysis_result.get('adjacent_probability', 0),
            'method': 'adjacent',
            'confidence': 0.55,
        }

