"""间隔分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class IntervalAnalyzer(BaseAnalyzer):
    """间隔分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析号码间隔

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 间隔分析结果
        """
        intervals_list = []
        avg_intervals = []
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            numbers = sorted([int(num) for num in red_balls])
            
            # 计算相邻号码间隔
            intervals = []
            for i in range(len(numbers) - 1):
                interval = numbers[i + 1] - numbers[i]
                intervals.append(interval)
            
            intervals_list.append(intervals)
            if intervals:
                avg_intervals.append(sum(intervals) / len(intervals))
        
        # 统计间隔频率
        all_intervals = [interval for intervals in intervals_list for interval in intervals]
        interval_counter = Counter(all_intervals)
        
        # 计算平均间隔
        overall_avg_interval = sum(avg_intervals) / len(avg_intervals) if avg_intervals else 0
        
        return {
            'interval_frequency': dict(interval_counter.most_common()),
            'most_common_intervals': [interval for interval, _ in interval_counter.most_common(10)],
            'avg_interval': round(overall_avg_interval, 2),
            'intervals_list': intervals_list,
            'avg_intervals': avg_intervals,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于间隔预测

        :param analysis_result: 分析结果
        :param params: 参数
        """
        most_common_intervals = analysis_result.get('most_common_intervals', [])
        avg_interval = analysis_result.get('avg_interval', 3)
        
        return {
            'recommended_intervals': most_common_intervals[:5],
            'avg_interval': avg_interval,
            'method': 'interval',
            'confidence': 0.5,
        }

