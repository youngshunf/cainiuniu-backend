"""三分区分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class ThreeZoneAnalyzer(BaseAnalyzer):
    """三分区分析器（前区、中区、后区）"""

    def get_three_zone(self, num: int, max_number: int = 33) -> str:
        """
        获取号码所属三分区
        
        :param num: 号码
        :param max_number: 最大号码
        :return: 区域名称（前区/中区/后区）
        """
        zone_size = max_number // 3
        if num <= zone_size:
            return '前区'
        elif num <= zone_size * 2:
            return '中区'
        else:
            return '后区'

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析三分区分布

        :param history_data: 历史开奖数据
        :param params: 参数（可选：max_number=33）
        :return: 三分区分析结果
        """
        if not params:
            params = {}
        
        max_number = params.get('max_number', 33)
        
        zone_patterns = []
        zone_distributions = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = [int(num) for num in red_balls]
            
            # 统计各区间号码数量
            zone_counter = Counter()
            for num in numbers:
                zone = self.get_three_zone(num, max_number)
                zone_counter[zone] += 1
            
            # 记录分布模式
            front = zone_counter.get('前区', 0)
            middle = zone_counter.get('中区', 0)
            back = zone_counter.get('后区', 0)
            
            zone_distributions.append({'前区': front, '中区': middle, '后区': back})
            zone_pattern = f'{front}:{middle}:{back}'
            zone_patterns.append(zone_pattern)
        
        # 统计模式频率
        pattern_counter = Counter(zone_patterns)
        
        # 计算各区间平均出号数
        avg_front = sum(d['前区'] for d in zone_distributions) / len(zone_distributions)
        avg_middle = sum(d['中区'] for d in zone_distributions) / len(zone_distributions)
        avg_back = sum(d['后区'] for d in zone_distributions) / len(zone_distributions)
        
        return {
            'max_number': max_number,
            'pattern_frequency': dict(pattern_counter.most_common()),
            'most_common_pattern': pattern_counter.most_common(1)[0] if pattern_counter else None,
            'avg_front_count': round(avg_front, 2),
            'avg_middle_count': round(avg_middle, 2),
            'avg_back_count': round(avg_back, 2),
            'zone_distributions': zone_distributions,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于三分区分析预测

        :param analysis_result: 分析结果
        :param params: 参数
        """
        most_common = analysis_result.get('most_common_pattern')
        if most_common:
            front, middle, back = map(int, most_common[0].split(':'))
        else:
            front = int(analysis_result.get('avg_front_count', 2))
            middle = int(analysis_result.get('avg_middle_count', 2))
            back = int(analysis_result.get('avg_back_count', 2))
        
        return {
            'recommended_distribution': {
                '前区': front,
                '中区': middle,
                '后区': back,
            },
            'pattern': f'{front}:{middle}:{back}',
            'method': 'three_zone',
            'confidence': 0.6,
        }

