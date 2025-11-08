"""重号分析算法"""

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class RepeatAnalyzer(BaseAnalyzer):
    """重号分析器（上期号码在本期重复出现）"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析重号规律

        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 重号分析结果
        """
        repeat_counts = []
        repeat_numbers_list = []
        has_repeat_count = 0
        
        for i in range(1, len(history_data)):
            prev_draw = history_data[i]
            curr_draw = history_data[i-1]
            
            prev_balls = set(self.get_red_balls(prev_draw))
            curr_balls = set(self.get_red_balls(curr_draw))
            
            # 计算重号
            repeat_numbers = prev_balls & curr_balls
            repeat_count = len(repeat_numbers)
            
            repeat_counts.append(repeat_count)
            repeat_numbers_list.append(list(repeat_numbers))
            
            if repeat_count > 0:
                has_repeat_count += 1
        
        # 统计重号个数频率
        from collections import Counter
        repeat_counter = Counter(repeat_counts)
        
        # 重号出现概率
        repeat_probability = has_repeat_count / len(repeat_counts) if repeat_counts else 0
        avg_repeat_count = sum(repeat_counts) / len(repeat_counts) if repeat_counts else 0
        
        return {
            'repeat_probability': round(repeat_probability, 4),
            'repeat_count_frequency': dict(repeat_counter.most_common()),
            'avg_repeat_count': round(avg_repeat_count, 2),
            'repeat_counts': repeat_counts,
            'repeat_numbers_list': repeat_numbers_list,
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于重号分析预测

        :param analysis_result: 分析结果
        :param params: 参数（需要提供上期号码）
        """
        if not params or 'prev_numbers' not in params:
            return {
                'method': 'repeat',
                'confidence': 0.5,
                'note': '需要提供上期号码',
            }
        
        prev_numbers = params.get('prev_numbers', [])
        avg_repeat_count = int(analysis_result.get('avg_repeat_count', 1))
        
        # 预测可能重复的号码
        return {
            'potential_repeat_numbers': prev_numbers[:avg_repeat_count] if prev_numbers else [],
            'expected_repeat_count': avg_repeat_count,
            'repeat_probability': analysis_result.get('repeat_probability', 0),
            'method': 'repeat',
            'confidence': 0.55,
        }

