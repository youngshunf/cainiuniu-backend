"""奇偶分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class OddEvenAnalyzer(BaseAnalyzer):
    """奇偶分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析奇偶比例

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 奇偶分析结果
        """
        odd_even_patterns = []  # 奇偶模式列表
        odd_counts = []
        even_counts = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            odd_count = sum(1 for num in red_balls if int(num) % 2 == 1)
            even_count = len(red_balls) - odd_count
            
            odd_counts.append(odd_count)
            even_counts.append(even_count)
            odd_even_patterns.append(f'{odd_count}:{even_count}')
        
        # 统计模式频率
        pattern_counter = Counter(odd_even_patterns)
        
        # 计算平均比例
        avg_odd = sum(odd_counts) / len(odd_counts)
        avg_even = sum(even_counts) / len(even_counts)
        
        return {
            'pattern_frequency': dict(pattern_counter.most_common()),
            'most_common_pattern': pattern_counter.most_common(1)[0] if pattern_counter else None,
            'avg_odd_count': round(avg_odd, 2),
            'avg_even_count': round(avg_even, 2),
            'odd_counts': odd_counts,
            'even_counts': even_counts,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于奇偶比例预测

        :param analysis_result: 分析结果
        :param params: 参数（可选：target_odd_count）
        """
        if not params:
            params = {}
        
        # 获取最常见的奇偶模式
        most_common = analysis_result.get('most_common_pattern')
        if most_common:
            odd_count, even_count = map(int, most_common[0].split(':'))
        else:
            odd_count = int(analysis_result.get('avg_odd_count', 3))
            even_count = int(analysis_result.get('avg_even_count', 3))
        
        # 覆盖参数
        odd_count = params.get('target_odd_count', odd_count)
        
        return {
            'recommended_pattern': f'{odd_count}:{even_count}',
            'odd_count': odd_count,
            'even_count': even_count,
            'method': 'odd_even',
            'confidence': 0.6,
        }

