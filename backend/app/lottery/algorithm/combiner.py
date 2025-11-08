"""组合分析器 - 多方法组合分析"""

import json
import random
from datetime import datetime

from backend.app.lottery.algorithm.traditional.ac_value import ACValueAnalyzer
from backend.app.lottery.algorithm.traditional.adjacent import AdjacentAnalyzer
from backend.app.lottery.algorithm.traditional.consecutive import ConsecutiveAnalyzer
from backend.app.lottery.algorithm.traditional.frequency import FrequencyAnalyzer
from backend.app.lottery.algorithm.traditional.hot_cold import HotColdAnalyzer
from backend.app.lottery.algorithm.traditional.interval import IntervalAnalyzer
from backend.app.lottery.algorithm.traditional.number_sum import NumberSumAnalyzer
from backend.app.lottery.algorithm.traditional.odd_even import OddEvenAnalyzer
from backend.app.lottery.algorithm.traditional.omission import OmissionAnalyzer
from backend.app.lottery.algorithm.traditional.prime_composite import PrimeCompositeAnalyzer
from backend.app.lottery.algorithm.traditional.repeat import RepeatAnalyzer
from backend.app.lottery.algorithm.traditional.road_012 import Road012Analyzer
from backend.app.lottery.algorithm.traditional.same_tail import SameTailAnalyzer
from backend.app.lottery.algorithm.traditional.size_distribution import SizeDistributionAnalyzer
from backend.app.lottery.algorithm.traditional.span import SpanAnalyzer
from backend.app.lottery.algorithm.traditional.sum_value import SumValueAnalyzer
from backend.app.lottery.algorithm.traditional.tail_sum import TailSumAnalyzer
from backend.app.lottery.algorithm.traditional.three_zone import ThreeZoneAnalyzer
from backend.app.lottery.algorithm.traditional.zone import ZoneAnalyzer
from backend.common.log import log

# 机器学习算法（可选，需要额外依赖）
try:
    from backend.app.lottery.algorithm.machine_learning.clustering import ClusteringAnalyzer
    from backend.app.lottery.algorithm.machine_learning.lstm import LSTMAnalyzer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    log.warning('机器学习模块依赖未安装，ML分析方法不可用')


class CombinationAnalyzer:
    """组合分析器"""

    # 分析方法映射
    ANALYZER_MAP = {
        # 传统分析方法
        'frequency': FrequencyAnalyzer,
        'hot_cold': HotColdAnalyzer,
        'odd_even': OddEvenAnalyzer,
        'prime_composite': PrimeCompositeAnalyzer,
        'road_012': Road012Analyzer,
        'sum_value': SumValueAnalyzer,
        'size_distribution': SizeDistributionAnalyzer,
        'interval': IntervalAnalyzer,
        'ac_value': ACValueAnalyzer,
        'span': SpanAnalyzer,
        'consecutive': ConsecutiveAnalyzer,
        'repeat': RepeatAnalyzer,
        'adjacent': AdjacentAnalyzer,
        'same_tail': SameTailAnalyzer,
        'zone': ZoneAnalyzer,
        'omission': OmissionAnalyzer,
        'tail_sum': TailSumAnalyzer,
        'number_sum': NumberSumAnalyzer,
        'three_zone': ThreeZoneAnalyzer,
    }
    
    # 添加机器学习方法（如果可用）
    if ML_AVAILABLE:
        ANALYZER_MAP.update({
            'lstm': LSTMAnalyzer,
            'clustering': ClusteringAnalyzer,
        })

    def __init__(self, lottery_code: str):
        self.lottery_code = lottery_code

    async def combine_methods(
        self, method_configs: list[dict], history_data: list, history_periods: int
    ) -> dict:
        """
        多方法组合分析

        :param method_configs: 方法配置列表 [{"code": "frequency", "weight": 0.3, "params": {}}]
        :param history_data: 历史开奖数据
        :param history_periods: 历史期数
        :return: 综合分析结果
        """
        # 限制历史数据期数
        history_data = history_data[:history_periods]
        
        analysis_results = {}
        method_predictions = []
        
        # 执行各个分析方法
        for config in method_configs:
            method_code = config.get('code')
            weight = config.get('weight', 1.0)
            params = config.get('params', {})
            
            try:
                # 获取分析器类
                analyzer_class = self.ANALYZER_MAP.get(method_code)
                if not analyzer_class:
                    log.warning(f'未找到分析方法: {method_code}')
                    continue
                
                # 创建分析器实例
                analyzer = analyzer_class(self.lottery_code)
                
                # 执行分析
                analysis_result = await analyzer.analyze(history_data, params)
                analysis_results[method_code] = analysis_result
                
                # 执行预测
                prediction = await analyzer.predict(analysis_result, params)
                prediction['weight'] = weight
                method_predictions.append({
                    'method': method_code,
                    'prediction': prediction,
                    'weight': weight,
                })
                
            except Exception as e:
                log.error(f'分析方法 {method_code} 执行失败: {e}')
                continue
        
        # 综合预测
        combined_prediction = await self._combine_predictions(method_predictions)
        
        return {
            'analysis_results': analysis_results,
            'method_predictions': method_predictions,
            'combined_prediction': combined_prediction,
        }

    async def _combine_predictions(self, method_predictions: list[dict]) -> dict:
        """
        综合多个方法的预测结果

        :param method_predictions: 各方法预测结果
        :return: 综合预测
        """
        # 收集所有推荐的号码
        red_ball_scores = {}
        blue_ball_scores = {}
        
        for pred_data in method_predictions:
            prediction = pred_data['prediction']
            weight = pred_data['weight']
            
            # 处理红球
            red_balls = prediction.get('red_balls', [])
            if red_balls:
                for num in red_balls:
                    if num not in red_ball_scores:
                        red_ball_scores[num] = 0
                    red_ball_scores[num] += weight
            
            # 处理蓝球
            blue_balls = prediction.get('blue_balls', [])
            if blue_balls:
                for num in blue_balls:
                    if num not in blue_ball_scores:
                        blue_ball_scores[num] = 0
                    blue_ball_scores[num] += weight
        
        # 按分数排序选择号码
        sorted_red = sorted(red_ball_scores.items(), key=lambda x: x[1], reverse=True)
        sorted_blue = sorted(blue_ball_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 根据彩种确定需要的号码数量
        red_count, blue_count = self._get_ball_counts()
        
        recommended_red = [num for num, _ in sorted_red[:red_count]]
        recommended_blue = [num for num, _ in sorted_blue[:blue_count]] if blue_count > 0 else None
        
        # 计算综合置信度
        confidence = sum(p['prediction'].get('confidence', 0.5) * p['weight'] 
                        for p in method_predictions) / sum(p['weight'] for p in method_predictions) if method_predictions else 0.5
        
        return {
            'recommended_red_balls': recommended_red,
            'recommended_blue_balls': recommended_blue,
            'confidence': round(confidence, 2),
            'red_ball_scores': dict(sorted_red[:20]),
            'blue_ball_scores': dict(sorted_blue[:10]) if blue_count > 0 else None,
        }

    def _get_ball_counts(self) -> tuple[int, int]:
        """
        获取彩种需要的号码数量

        :return: (红球数量, 蓝球数量)
        """
        counts_map = {
            'ssq': (6, 1),      # 双色球
            'dlt': (5, 2),      # 大乐透
            '3d': (3, 0),       # 福彩3D
            'pls': (3, 0),      # 排列三
            'plw': (5, 0),      # 排列五
            'qlc': (7, 0),      # 七乐彩
            'kl8': (20, 0),     # 快乐8
            'qxc': (7, 0),      # 七星彩
        }
        return counts_map.get(self.lottery_code, (6, 1))

    async def generate_article(
        self, analysis_data: dict, lottery_info: dict, target_period: str
    ) -> str:
        """
        生成分析文章

        :param analysis_data: 分析数据
        :param lottery_info: 彩票信息
        :param target_period: 目标期号
        :return: 富文本文章
        """
        method_predictions = analysis_data.get('method_predictions', [])
        combined_prediction = analysis_data.get('combined_prediction', {})
        
        # 文章标题
        article = f"# {lottery_info.get('name', '')} {target_period}期 综合分析预测\n\n"
        article += f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 分析方法总结
        article += "## 📊 使用的分析方法\n\n"
        for pred_data in method_predictions:
            method = pred_data['method']
            weight = pred_data['weight']
            article += f"- **{method}** (权重: {weight})\n"
        article += "\n"
        
        # 各方法分析结果
        article += "## 🔍 各方法分析详情\n\n"
        for pred_data in method_predictions:
            method = pred_data['method']
            prediction = pred_data['prediction']
            article += f"### {method}\n\n"
            article += f"- 置信度: {prediction.get('confidence', 0.5)}\n"
            article += f"- 推荐号码: {prediction}\n\n"
        
        # 综合预测结果
        article += "## 🎯 综合预测结果\n\n"
        article += f"**综合置信度**: {combined_prediction.get('confidence', 0.5)}\n\n"
        article += f"**推荐红球**: {', '.join(combined_prediction.get('recommended_red_balls', []))}\n\n"
        
        blue_balls = combined_prediction.get('recommended_blue_balls')
        if blue_balls:
            article += f"**推荐蓝球**: {', '.join(blue_balls)}\n\n"
        
        # 风险提示
        article += "## ⚠️ 风险提示\n\n"
        article += "本预测仅供参考，彩票具有随机性，请理性投注。\n\n"
        
        return article

    async def format_numbers(self, lottery_code: str, combined_prediction: dict, periods_config: list[int] = None) -> dict:
        """
        格式化号码输出（生成多注）

        :param lottery_code: 彩种代码
        :param combined_prediction: 综合预测结果
        :param periods_config: 期数配置 [50, 100, 300, 500, 1000]
        :return: 格式化的号码组合
        """
        if not periods_config:
            periods_config = [50, 100, 300, 500, 1000]
        
        formatted_numbers = []
        
        # 根据不同彩种生成不同格式的号码
        if lottery_code in ['ssq', 'dlt']:
            # 双色球、大乐透: 大复式、小复式、单式
            red_balls = combined_prediction.get('recommended_red_balls', [])
            blue_balls = combined_prediction.get('recommended_blue_balls', [])
            
            for i, period_count in enumerate(periods_config):
                if i == 0:
                    # 大复式 15+5
                    formatted_numbers.append({
                        'type': '大复式',
                        'period_count': period_count,
                        'red_balls': red_balls[:15] if len(red_balls) >= 15 else red_balls,
                        'blue_balls': blue_balls[:5] if lottery_code == 'ssq' and len(blue_balls) >= 5 else blue_balls,
                    })
                elif i == 1:
                    # 小复式 9+2
                    formatted_numbers.append({
                        'type': '小复式',
                        'period_count': period_count,
                        'red_balls': red_balls[:9] if len(red_balls) >= 9 else red_balls,
                        'blue_balls': blue_balls[:2] if len(blue_balls) >= 2 else blue_balls,
                    })
                else:
                    # 单式
                    red_count, blue_count = self._get_ball_counts()
                    formatted_numbers.append({
                        'type': '单式',
                        'period_count': period_count,
                        'red_balls': red_balls[:red_count],
                        'blue_balls': blue_balls[:blue_count] if blue_balls else None,
                    })
        
        elif lottery_code in ['3d', 'pls']:
            # 3D、排列三
            red_balls = combined_prediction.get('recommended_red_balls', [])
            for i, period_count in enumerate(periods_config):
                if i == 0:
                    formatted_numbers.append({'type': '七码组选', 'period_count': period_count, 'numbers': red_balls[:7]})
                elif i == 1:
                    formatted_numbers.append({'type': '六码组选', 'period_count': period_count, 'numbers': red_balls[:6]})
                elif i == 2:
                    formatted_numbers.append({'type': '五码组选', 'period_count': period_count, 'numbers': red_balls[:5]})
                else:
                    formatted_numbers.append({'type': '直选', 'period_count': period_count, 'numbers': red_balls[:3]})
        
        elif lottery_code == 'kl8':
            # 快乐8: 1-15码各一注
            red_balls = combined_prediction.get('recommended_red_balls', [])
            for i in range(1, 16):
                formatted_numbers.append({
                    'type': f'{i}码',
                    'numbers': red_balls[:i] if len(red_balls) >= i else red_balls,
                })
        
        else:
            # 其他彩种：五注单式
            red_count, blue_count = self._get_ball_counts()
            red_balls = combined_prediction.get('recommended_red_balls', [])
            for i, period_count in enumerate(periods_config):
                formatted_numbers.append({
                    'type': '单式',
                    'period_count': period_count,
                    'numbers': red_balls[i*red_count:(i+1)*red_count] if len(red_balls) >= (i+1)*red_count else red_balls[:red_count],
                })
        
        return {
            'lottery_code': lottery_code,
            'formatted_numbers': formatted_numbers,
        }


combiner = CombinationAnalyzer

