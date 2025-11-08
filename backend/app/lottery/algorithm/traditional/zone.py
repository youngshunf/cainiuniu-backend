"""区间分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class ZoneAnalyzer(BaseAnalyzer):
    """区间分析器"""

    def get_zone(self, num: int, zone_count: int = 3, max_number: int = 33) -> int:
        """
        获取号码所属区间
        
        :param num: 号码
        :param zone_count: 区间数量
        :param max_number: 最大号码
        :return: 区间编号（0开始）
        """
        zone_size = max_number // zone_count
        return min((num - 1) // zone_size, zone_count - 1)

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析区间分布

        :param history_data: 历史开奖数据
        :param params: 参数（可选：zone_count=3, max_number=33）
        :return: 区间分析结果
        """
        if not params:
            params = {}
        
        zone_count = params.get('zone_count', 3)
        max_number = params.get('max_number', 33)
        
        zone_patterns = []
        zone_distributions = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = [int(num) for num in red_balls]
            
            # 统计各区间号码数量
            zone_counter = Counter()
            for num in numbers:
                zone = self.get_zone(num, zone_count, max_number)
                zone_counter[zone] += 1
            
            # 记录分布模式
            zone_dist = [zone_counter.get(i, 0) for i in range(zone_count)]
            zone_distributions.append(zone_dist)
            zone_pattern = ':'.join(str(count) for count in zone_dist)
            zone_patterns.append(zone_pattern)
        
        # 统计模式频率
        pattern_counter = Counter(zone_patterns)
        
        # 计算各区间平均出号数
        avg_zone_counts = []
        for i in range(zone_count):
            zone_i_counts = [dist[i] for dist in zone_distributions]
            avg_zone_counts.append(round(sum(zone_i_counts) / len(zone_i_counts), 2))
        
        return {
            'zone_count': zone_count,
            'max_number': max_number,
            'pattern_frequency': dict(pattern_counter.most_common()),
            'most_common_pattern': pattern_counter.most_common(1)[0] if pattern_counter else None,
            'avg_zone_counts': avg_zone_counts,
            'zone_distributions': zone_distributions,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于区间分析预测

        :param analysis_result: 分析结果
        :param params: 参数
        """
        most_common = analysis_result.get('most_common_pattern')
        if most_common:
            zone_counts = list(map(int, most_common[0].split(':')))
        else:
            zone_counts = analysis_result.get('avg_zone_counts', [2, 2, 2])
        
        return {
            'recommended_zone_distribution': zone_counts,
            'zone_count': analysis_result.get('zone_count', 3),
            'method': 'zone',
            'confidence': 0.6,
        }

