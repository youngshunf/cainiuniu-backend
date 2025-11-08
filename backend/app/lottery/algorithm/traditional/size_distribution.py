"""大小号分布分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class SizeDistributionAnalyzer(BaseAnalyzer):
    """大小号分布分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析大小号分布

        :param history_data: 历史开奖数据
        :param params: 参数（可选：threshold=中位数）
        :return: 大小号分析结果
        """
        if not params:
            params = {}
        
        # 大小号分界线（默认为号码范围的中位数）
        threshold = params.get('threshold', 17)  # 示例：对于1-33，中位数为17
        
        size_patterns = []
        large_counts = []
        small_counts = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            large_count = sum(1 for num in red_balls if int(num) > threshold)
            small_count = len(red_balls) - large_count
            
            large_counts.append(large_count)
            small_counts.append(small_count)
            size_patterns.append(f'{large_count}:{small_count}')
        
        # 统计模式频率
        pattern_counter = Counter(size_patterns)
        
        # 计算平均分布
        avg_large = sum(large_counts) / len(large_counts)
        avg_small = sum(small_counts) / len(small_counts)
        
        return {
            'threshold': threshold,
            'pattern_frequency': dict(pattern_counter.most_common()),
            'most_common_pattern': pattern_counter.most_common(1)[0] if pattern_counter else None,
            'avg_large_count': round(avg_large, 2),
            'avg_small_count': round(avg_small, 2),
            'large_counts': large_counts,
            'small_counts': small_counts,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于大小号分布预测

        :param analysis_result: 分析结果
        :param params: 参数（可选：target_large_count）
        """
        if not params:
            params = {}
        
        # 获取最常见的大小号模式
        most_common = analysis_result.get('most_common_pattern')
        if most_common:
            large_count, small_count = map(int, most_common[0].split(':'))
        else:
            large_count = int(analysis_result.get('avg_large_count', 3))
            small_count = int(analysis_result.get('avg_small_count', 3))
        
        # 覆盖参数
        large_count = params.get('target_large_count', large_count)
        
        return {
            'recommended_pattern': f'{large_count}:{small_count}',
            'large_count': large_count,
            'small_count': small_count,
            'threshold': analysis_result.get('threshold', 17),
            'method': 'size_distribution',
            'confidence': 0.6,
        }

