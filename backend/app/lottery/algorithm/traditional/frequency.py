"""频率分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class FrequencyAnalyzer(BaseAnalyzer):
    """频率分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        统计号码出现频率

        :param history_data: 历史开奖数据
        :param params: 参数（可选：is_red_ball=True/False）
        :return: 频率统计结果
        """
        if not params:
            params = {}
        
        is_red_ball = params.get('is_red_ball', True)
        red_counter = Counter()
        blue_counter = Counter()
        
        for draw in history_data:
            red_balls = self.get_red_balls(draw)
            red_counter.update(red_balls)
            
            blue_balls = self.get_blue_balls(draw)
            if blue_balls:
                blue_counter.update(blue_balls)
        
        # 计算频率和概率
        total_draws = len(history_data)
        
        red_frequency = {
            num: {
                'count': count,
                'probability': round(count / total_draws, 4),
            }
            for num, count in red_counter.most_common()
        }
        
        blue_frequency = {
            num: {
                'count': count,
                'probability': round(count / total_draws, 4),
            }
            for num, count in blue_counter.most_common()
        }
        
        return {
            'red_frequency': red_frequency,
            'blue_frequency': blue_frequency,
            'total_draws': total_draws,
            'red_top10': [num for num, _ in red_counter.most_common(10)],
            'blue_top5': [num for num, _ in blue_counter.most_common(5)] if blue_counter else [],
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于频率预测号码

        :param analysis_result: 分析结果
        :param params: 参数（可选：red_count, blue_count）
        """
        if not params:
            params = {}
        
        red_count = params.get('red_count', 6)
        blue_count = params.get('blue_count', 1)
        
        # 取频率最高的号码
        red_numbers = analysis_result.get('red_top10', [])[:red_count]
        blue_numbers = analysis_result.get('blue_top5', [])[:blue_count]
        
        return {
            'red_balls': red_numbers,
            'blue_balls': blue_numbers if blue_numbers else None,
            'method': 'frequency',
            'confidence': 0.7,
        }

