"""跨度分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class SpanAnalyzer(BaseAnalyzer):
    """跨度分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析跨度（最大号 - 最小号）

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 跨度分析结果
        """
        spans = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = [int(num) for num in red_balls]
            span = max(numbers) - min(numbers)
            spans.append(span)
        
        # 统计跨度频率
        span_counter = Counter(spans)
        
        # 计算统计指标
        avg_span = sum(spans) / len(spans)
        max_span = max(spans)
        min_span = min(spans)
        
        return {
            'span_frequency': dict(span_counter.most_common()),
            'most_common_spans': [span for span, _ in span_counter.most_common(10)],
            'avg_span': round(avg_span, 2),
            'max_span': max_span,
            'min_span': min_span,
            'spans': spans,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于跨度预测

        :param analysis_result: 分析结果
        :param params: 参数（可选：target_span）
        """
        if not params:
            params = {}
        
        most_common_spans = analysis_result.get('most_common_spans', [])
        avg_span = analysis_result.get('avg_span', 20)
        
        target_span = params.get('target_span', most_common_spans[0] if most_common_spans else int(avg_span))
        
        return {
            'target_span': target_span,
            'recommended_spans': most_common_spans[:5],
            'avg_span': avg_span,
            'method': 'span',
            'confidence': 0.6,
        }

