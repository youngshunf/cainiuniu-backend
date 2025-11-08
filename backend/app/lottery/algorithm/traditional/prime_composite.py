"""质合分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class PrimeCompositeAnalyzer(BaseAnalyzer):
    """质合分析器"""

    def __init__(self, lottery_code: str):
        super().__init__(lottery_code)
        # 质数列表（1-99）
        self.primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}

    def is_prime(self, num: int) -> bool:
        """判断是否为质数"""
        return num in self.primes

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析质合比例

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 质合分析结果
        """
        prime_composite_patterns = []
        prime_counts = []
        composite_counts = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            prime_count = sum(1 for num in red_balls if self.is_prime(int(num)))
            composite_count = len(red_balls) - prime_count
            
            prime_counts.append(prime_count)
            composite_counts.append(composite_count)
            prime_composite_patterns.append(f'{prime_count}:{composite_count}')
        
        # 统计模式频率
        pattern_counter = Counter(prime_composite_patterns)
        
        # 计算平均比例
        avg_prime = sum(prime_counts) / len(prime_counts)
        avg_composite = sum(composite_counts) / len(composite_counts)
        
        return {
            'pattern_frequency': dict(pattern_counter.most_common()),
            'most_common_pattern': pattern_counter.most_common(1)[0] if pattern_counter else None,
            'avg_prime_count': round(avg_prime, 2),
            'avg_composite_count': round(avg_composite, 2),
            'prime_counts': prime_counts,
            'composite_counts': composite_counts,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于质合比例预测

        :param analysis_result: 分析结果
        :param params: 参数（可选：target_prime_count）
        """
        if not params:
            params = {}
        
        # 获取最常见的质合模式
        most_common = analysis_result.get('most_common_pattern')
        if most_common:
            prime_count, composite_count = map(int, most_common[0].split(':'))
        else:
            prime_count = int(analysis_result.get('avg_prime_count', 2))
            composite_count = int(analysis_result.get('avg_composite_count', 4))
        
        # 覆盖参数
        prime_count = params.get('target_prime_count', prime_count)
        
        return {
            'recommended_pattern': f'{prime_count}:{composite_count}',
            'prime_count': prime_count,
            'composite_count': composite_count,
            'method': 'prime_composite',
            'confidence': 0.6,
        }

