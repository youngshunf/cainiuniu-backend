"""聚类分析算法

注意：此模块需要安装 scikit-learn 依赖
pip install scikit-learn>=1.4.0
"""

import json

import numpy as np

from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer
from backend.common.log import log

# 延迟导入scikit-learn
try:
    from sklearn.cluster import DBSCAN, KMeans
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    log.warning('scikit-learn未安装，聚类分析功能不可用')


class ClusteringAnalyzer(BaseAnalyzer):
    """聚类分析器"""

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        聚类分析
        
        :param history_data: 历史开奖数据
        :param params: 参数（algorithm='kmeans'/'dbscan', n_clusters=5）
        :return: 聚类结果
        """
        if not SKLEARN_AVAILABLE:
            return {'error': 'scikit-learn未安装，无法进行聚类分析'}
        
        if not params:
            params = {}
        
        algorithm = params.get('algorithm', 'kmeans')
        n_clusters = params.get('n_clusters', 5)
        
        try:
            # 提取特征
            features = self._extract_features(history_data)
            
            if features is None or len(features) == 0:
                return {'error': '特征提取失败'}
            
            # 标准化
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # 选择聚类算法
            if algorithm == 'kmeans':
                model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            elif algorithm == 'dbscan':
                eps = params.get('eps', 0.5)
                min_samples = params.get('min_samples', 5)
                model = DBSCAN(eps=eps, min_samples=min_samples)
            else:
                return {'error': f'未知的聚类算法: {algorithm}'}
            
            # 聚类
            labels = model.fit_predict(features_scaled)
            
            # 分析聚类结果
            cluster_analysis = self._analyze_clusters(history_data, labels, n_clusters)
            
            return {
                'algorithm': algorithm,
                'n_clusters': n_clusters,
                'labels': labels.tolist(),
                'cluster_analysis': cluster_analysis,
            }
            
        except Exception as e:
            log.error(f'聚类分析失败: {e}')
            return {'error': f'聚类分析失败: {str(e)}'}

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于聚类结果预测
        
        :param analysis_result: 分析结果
        :param params: 参数
        :return: 推荐号码
        """
        if 'error' in analysis_result:
            return {'error': analysis_result['error']}
        
        if not params:
            params = {}
        
        cluster_analysis = analysis_result.get('cluster_analysis', {})
        
        # 选择最常出现的聚类中心的号码
        most_common_cluster = cluster_analysis.get('most_common_cluster')
        if most_common_cluster is not None:
            cluster_numbers = cluster_analysis.get('cluster_numbers', {}).get(str(most_common_cluster), [])
            
            red_count = params.get('red_count', 6)
            recommended_red = cluster_numbers[:red_count]
            
            return {
                'red_balls': recommended_red,
                'blue_balls': None,
                'method': 'clustering',
                'cluster': most_common_cluster,
                'confidence': 0.65,
            }
        
        return {'error': '无法生成预测'}

    def _extract_features(self, history_data: list) -> np.ndarray | None:
        """
        提取特征
        
        :param history_data: 历史数据
        :return: 特征矩阵
        """
        try:
            features = []
            for draw in history_data:
                red_balls = self.get_red_balls(draw)
                # 特征：号码值、和值、跨度、奇偶比等
                numbers = [int(num) for num in red_balls]
                feature = [
                    sum(numbers),  # 和值
                    max(numbers) - min(numbers),  # 跨度
                    sum(1 for n in numbers if n % 2 == 1),  # 奇数个数
                    sum(1 for n in numbers if self._is_prime(n)),  # 质数个数
                ] + numbers  # 加上原始号码
                features.append(feature)
            
            return np.array(features)
            
        except Exception as e:
            log.error(f'特征提取失败: {e}')
            return None

    def _analyze_clusters(self, history_data: list, labels: np.ndarray, n_clusters: int) -> dict:
        """
        分析聚类结果
        
        :param history_data: 历史数据
        :param labels: 聚类标签
        :param n_clusters: 聚类数量
        :return: 聚类分析
        """
        from collections import Counter
        
        cluster_counts = Counter(labels)
        most_common_cluster = cluster_counts.most_common(1)[0][0]
        
        # 每个聚类的代表号码
        cluster_numbers = {}
        for cluster_id in range(n_clusters):
            indices = np.where(labels == cluster_id)[0]
            if len(indices) > 0:
                # 取该聚类中最近的一期的号码
                latest_idx = indices[0]
                red_balls = self.get_red_balls(history_data[latest_idx])
                cluster_numbers[str(cluster_id)] = red_balls
        
        return {
            'cluster_counts': dict(cluster_counts),
            'most_common_cluster': int(most_common_cluster),
            'cluster_numbers': cluster_numbers,
        }

    def _is_prime(self, n: int) -> bool:
        """判断是否为质数"""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

