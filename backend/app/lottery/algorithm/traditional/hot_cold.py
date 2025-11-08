"""冷热号分析算法"""

from collections import Counter

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class HotColdAnalyzer(BaseAnalyzer):
    """冷热号分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析冷热号

        :param history_data: 历史开奖数据
        :param params: 参数（可选：recent_periods=30）
        :return: 冷热号分析结果
        """
        if not params:
            params = {}
        
        recent_periods = params.get('recent_periods', 30)
        recent_data = history_data[:recent_periods]
        
        red_counter = Counter()
        blue_counter = Counter()
        
        for draw in recent_data:
            red_balls = self.get_red_balls(draw)
            red_counter.update(red_balls)
            
            blue_balls = self.get_blue_balls(draw)
            if blue_balls:
                blue_counter.update(blue_balls)
        
        # 获取所有可能的号码范围
        # 这里简化处理，实际应根据彩种确定范围
        all_red_numbers = set(str(i).zfill(2) for i in range(1, 34))  # 示例：1-33
        all_blue_numbers = set(str(i).zfill(2) for i in range(1, 17))  # 示例：1-16
        
        # 热号：出现次数最多的号码
        hot_red = [num for num, _ in red_counter.most_common(10)]
        hot_blue = [num for num, _ in blue_counter.most_common(5)] if blue_counter else []
        
        # 冷号：出现次数少或未出现的号码
        appeared_red = set(red_counter.keys())
        appeared_blue = set(blue_counter.keys())
        
        cold_red = list(all_red_numbers - appeared_red)[:10]
        cold_blue = list(all_blue_numbers - appeared_blue)[:5] if blue_counter else []
        
        # 温号：中等频率的号码
        warm_red = [num for num, count in red_counter.items() 
                    if count > len(recent_data) * 0.05 and count < len(recent_data) * 0.15][:10]
        
        return {
            'recent_periods': recent_periods,
            'hot_red': hot_red,
            'hot_blue': hot_blue,
            'cold_red': cold_red,
            'cold_blue': cold_blue,
            'warm_red': warm_red,
            'red_frequency': dict(red_counter),
            'blue_frequency': dict(blue_counter),
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于冷热号预测

        :param analysis_result: 分析结果
        :param params: 参数（可选：strategy='hot'/'cold'/'mix'）
        """
        if not params:
            params = {}
        
        strategy = params.get('strategy', 'mix')
        red_count = params.get('red_count', 6)
        blue_count = params.get('blue_count', 1)
        
        if strategy == 'hot':
            # 选择热号
            red_numbers = analysis_result.get('hot_red', [])[:red_count]
            blue_numbers = analysis_result.get('hot_blue', [])[:blue_count]
        elif strategy == 'cold':
            # 选择冷号
            red_numbers = analysis_result.get('cold_red', [])[:red_count]
            blue_numbers = analysis_result.get('cold_blue', [])[:blue_count]
        else:
            # 混合策略：热号+冷号
            hot_red = analysis_result.get('hot_red', [])
            cold_red = analysis_result.get('cold_red', [])
            red_numbers = (hot_red[:red_count//2] + cold_red[:red_count - red_count//2])[:red_count]
            
            hot_blue = analysis_result.get('hot_blue', [])
            cold_blue = analysis_result.get('cold_blue', [])
            blue_numbers = (hot_blue[:blue_count] if hot_blue else cold_blue[:blue_count])
        
        return {
            'red_balls': red_numbers,
            'blue_balls': blue_numbers if blue_numbers else None,
            'method': 'hot_cold',
            'strategy': strategy,
            'confidence': 0.65,
        }

