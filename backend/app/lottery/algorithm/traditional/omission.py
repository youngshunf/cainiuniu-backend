"""遗漏值分析算法"""

from collections import defaultdict

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer


class OmissionAnalyzer(BaseAnalyzer):
    """遗漏值分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        分析号码遗漏值

        :param history_data: 历史开奖数据（从新到旧排序）
        :param params: 参数（可选：max_number=33）
        :return: 遗漏值分析结果
        """
        if not params:
            params = {}
        
        max_number = params.get('max_number', 33)
        
        # 记录每个号码的遗漏值
        current_omissions = defaultdict(int)  # 当前遗漏
        max_omissions = defaultdict(int)  # 历史最大遗漏
        all_omissions = defaultdict(list)  # 所有遗漏记录
        
        # 初始化所有号码
        for num in range(1, max_number + 1):
            num_str = str(num).zfill(2)
            current_omissions[num_str] = 0
        
        # 从最新一期开始往前遍历
        for draw in history_data:
            red_balls = set(self.get_red_balls(draw))
            
            # 更新遗漏值
            for num_str in current_omissions:
                if num_str in red_balls:
                    # 出现了，记录遗漏值
                    omission = current_omissions[num_str]
                    all_omissions[num_str].append(omission)
                    
                    # 更新最大遗漏
                    if omission > max_omissions[num_str]:
                        max_omissions[num_str] = omission
                    
                    # 重置遗漏
                    current_omissions[num_str] = 0
                else:
                    # 未出现，遗漏+1
                    current_omissions[num_str] += 1
        
        # 计算平均遗漏
        avg_omissions = {}
        for num_str, omissions in all_omissions.items():
            if omissions:
                avg_omissions[num_str] = round(sum(omissions) / len(omissions), 2)
            else:
                avg_omissions[num_str] = 0
        
        # 找出冷门号（当前遗漏较大的）
        cold_numbers = sorted(current_omissions.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 找出可能回补的号（当前遗漏接近或超过平均遗漏的）
        potential_numbers = []
        for num_str, current_omission in current_omissions.items():
            avg_omission = avg_omissions.get(num_str, 0)
            if avg_omission > 0 and current_omission >= avg_omission * 0.8:
                potential_numbers.append((num_str, current_omission, avg_omission))
        potential_numbers.sort(key=lambda x: x[1] / x[2] if x[2] > 0 else 0, reverse=True)
        
        return {
            'current_omissions': dict(current_omissions),
            'max_omissions': dict(max_omissions),
            'avg_omissions': avg_omissions,
            'cold_numbers': cold_numbers,
            'potential_numbers': [(num, curr, avg) for num, curr, avg in potential_numbers[:10]],
        }

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于遗漏值预测

        :param analysis_result: 分析结果
        :param params: 参数（可选：count=6）
        """
        if not params:
            params = {}
        
        count = params.get('count', 6)
        
        # 推荐可能回补的号码
        potential_numbers = analysis_result.get('potential_numbers', [])
        recommended_numbers = [num for num, _, _ in potential_numbers[:count]]
        
        return {
            'recommended_numbers': recommended_numbers,
            'method': 'omission',
            'confidence': 0.65,
        }

