"""012路分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class Road012Analyzer(BaseAnalyzer):
    """012路分析器"""

    def get_road(self, num: int) -> int:
        """
        获取号码所属路数（0路、1路、2路）
        
        :param num: 号码
        :return: 路数（0/1/2）
        """
        return num % 3

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析012路分布

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 012路分析结果
        """
        road_patterns = []
        road_0_counts = []
        road_1_counts = []
        road_2_counts = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            road_counter = Counter()
            
            for num_str in red_balls:
                num = int(num_str)
                road = self.get_road(num)
                road_counter[road] += 1
            
            road_0 = road_counter.get(0, 0)
            road_1 = road_counter.get(1, 0)
            road_2 = road_counter.get(2, 0)
            
            road_0_counts.append(road_0)
            road_1_counts.append(road_1)
            road_2_counts.append(road_2)
            road_patterns.append(f'{road_0}:{road_1}:{road_2}')
        
        # 统计模式频率
        pattern_counter = Counter(road_patterns)
        
        # 计算平均分布
        avg_road_0 = sum(road_0_counts) / len(road_0_counts)
        avg_road_1 = sum(road_1_counts) / len(road_1_counts)
        avg_road_2 = sum(road_2_counts) / len(road_2_counts)
        
        return {
            'pattern_frequency': dict(pattern_counter.most_common()),
            'most_common_pattern': pattern_counter.most_common(1)[0] if pattern_counter else None,
            'avg_road_0_count': round(avg_road_0, 2),
            'avg_road_1_count': round(avg_road_1, 2),
            'avg_road_2_count': round(avg_road_2, 2),
            'road_0_counts': road_0_counts,
            'road_1_counts': road_1_counts,
            'road_2_counts': road_2_counts,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于012路分布预测

        :param analysis_result: 分析结果
        :param params: 参数
        """
        # 获取最常见的012路模式
        most_common = analysis_result.get('most_common_pattern')
        if most_common:
            road_0, road_1, road_2 = map(int, most_common[0].split(':'))
        else:
            road_0 = int(analysis_result.get('avg_road_0_count', 2))
            road_1 = int(analysis_result.get('avg_road_1_count', 2))
            road_2 = int(analysis_result.get('avg_road_2_count', 2))
        
        return {
            'recommended_pattern': f'{road_0}:{road_1}:{road_2}',
            'road_0_count': road_0,
            'road_1_count': road_1,
            'road_2_count': road_2,
            'method': 'road_012',
            'confidence': 0.6,
        }

