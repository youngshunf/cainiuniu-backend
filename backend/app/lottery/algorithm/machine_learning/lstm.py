"""LSTM时间序列预测算法

注意：此模块需要安装 TensorFlow 依赖
pip install tensorflow>=2.15.0
"""

import json
import os

import numpy as np

from backend.app.lottery.algorithm.machine_learning.base_ml_analyzer import BaseMLAnalyzer
from backend.common.log import log

# 延迟导入TensorFlow，避免未安装时影响其他功能
try:
    import tensorflow as tf
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.models import Sequential, load_model
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    log.warning('TensorFlow未安装，LSTM模型功能不可用')


class LSTMAnalyzer(BaseMLAnalyzer):
    """LSTM神经网络分析器"""

    def __init__(self, lottery_code: str):
        super().__init__(lottery_code)
        self.sequence_length = 10  # 序列长度
        self.feature_dim = 0  # 特征维度
        
        if not TENSORFLOW_AVAILABLE:
            log.error('TensorFlow未安装，无法使用LSTM分析器')

    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        """
        使用LSTM分析历史数据
        
        :param history_data: 历史开奖数据
        :param params: 参数
        :return: 分析结果
        """
        if not TENSORFLOW_AVAILABLE:
            return {'error': 'TensorFlow未安装，无法进行LSTM分析'}
        
        if not params:
            params = {}
        
        # 检查是否需要训练模型
        if not self.model or params.get('retrain', False):
            train_result = await self.train_model(history_data, params)
            if 'error' in train_result:
                return train_result
        
        # 提取最近的序列数据
        recent_sequence = history_data[:self.sequence_length]
        X = self._prepare_sequence(recent_sequence)
        
        if X is None:
            return {'error': '数据预处理失败'}
        
        # 预测
        try:
            predictions = self.model.predict(X, verbose=0)
            
            return {
                'model_type': 'LSTM',
                'sequence_length': self.sequence_length,
                'predictions': predictions.tolist(),
                'recent_sequence': recent_sequence,
            }
        except Exception as e:
            log.error(f'LSTM预测失败: {e}')
            return {'error': f'预测失败: {str(e)}'}

    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        """
        基于LSTM分析结果预测号码
        
        :param analysis_result: 分析结果
        :param params: 参数
        :return: 推荐号码
        """
        if 'error' in analysis_result:
            return {'error': analysis_result['error']}
        
        if not params:
            params = {}
        
        predictions = analysis_result.get('predictions', [])
        if not predictions:
            return {'error': '无预测结果'}
        
        # 将预测结果转换为号码
        # 这里需要根据具体的预测输出格式进行转换
        # 示例：取预测概率最高的号码
        red_count = params.get('red_count', 6)
        blue_count = params.get('blue_count', 1)
        
        # 简化处理：从预测中选择top号码
        pred_array = np.array(predictions[0])
        top_indices = np.argsort(pred_array)[-red_count:]
        recommended_red = [str(i+1).zfill(2) for i in top_indices]
        
        return {
            'red_balls': recommended_red,
            'blue_balls': None,  # LSTM蓝球预测需要单独训练
            'method': 'lstm',
            'confidence': 0.75,
        }

    async def train_model(self, history_data: list, params: dict | None = None) -> dict:
        """
        训练LSTM模型
        
        :param history_data: 历史数据
        :param params: 训练参数
        :return: 训练结果
        """
        if not TENSORFLOW_AVAILABLE:
            return {'error': 'TensorFlow未安装'}
        
        if not params:
            params = {}
        
        try:
            # 数据预处理
            X, y = self.preprocess_data(history_data)
            
            if X is None or y is None:
                return {'error': '数据预处理失败'}
            
            # 构建模型
            epochs = params.get('epochs', 50)
            batch_size = params.get('batch_size', 32)
            units = params.get('units', 64)
            
            self.model = Sequential([
                LSTM(units, return_sequences=True, input_shape=(self.sequence_length, self.feature_dim)),
                Dropout(0.2),
                LSTM(units//2, return_sequences=False),
                Dropout(0.2),
                Dense(units//4, activation='relu'),
                Dense(self.feature_dim, activation='softmax'),
            ])
            
            self.model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            # 训练模型
            history = self.model.fit(
                X, y,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2,
                verbose=0
            )
            
            return {
                'success': True,
                'epochs': epochs,
                'final_loss': float(history.history['loss'][-1]),
                'final_accuracy': float(history.history['accuracy'][-1]),
            }
            
        except Exception as e:
            log.error(f'LSTM训练失败: {e}')
            return {'error': f'训练失败: {str(e)}'}

    async def load_model(self, model_path: str) -> None:
        """加载模型"""
        if not TENSORFLOW_AVAILABLE:
            raise ImportError('TensorFlow未安装')
        
        if os.path.exists(model_path):
            self.model = load_model(model_path)
            self.model_path = model_path
            log.info(f'LSTM模型加载成功: {model_path}')
        else:
            raise FileNotFoundError(f'模型文件不存在: {model_path}')

    async def save_model(self, model_path: str) -> None:
        """保存模型"""
        if not TENSORFLOW_AVAILABLE:
            raise ImportError('TensorFlow未安装')
        
        if self.model:
            self.model.save(model_path)
            self.model_path = model_path
            log.info(f'LSTM模型保存成功: {model_path}')
        else:
            raise ValueError('模型未训练')

    def preprocess_data(self, history_data: list) -> tuple:
        """
        数据预处理
        
        :param history_data: 历史数据
        :return: (X, y) 特征和标签
        """
        try:
            # 提取号码序列
            sequences = []
            for draw in history_data:
                red_balls = self.get_red_balls(draw)
                # 转换为one-hot编码或数值编码
                encoded = self._encode_numbers(red_balls)
                sequences.append(encoded)
            
            # 构建时间序列数据
            X, y = [], []
            for i in range(len(sequences) - self.sequence_length):
                X.append(sequences[i:i + self.sequence_length])
                y.append(sequences[i + self.sequence_length])
            
            X = np.array(X)
            y = np.array(y)
            
            self.feature_dim = X.shape[2]
            
            return X, y
            
        except Exception as e:
            log.error(f'数据预处理失败: {e}')
            return None, None

    def _encode_numbers(self, numbers: list[str]) -> list:
        """
        编码号码
        
        :param numbers: 号码列表
        :return: 编码后的向量
        """
        # 简化实现：one-hot编码
        max_number = 33  # 根据彩种调整
        encoded = [0] * max_number
        for num in numbers:
            idx = int(num) - 1
            if 0 <= idx < max_number:
                encoded[idx] = 1
        return encoded

    def _prepare_sequence(self, recent_data: list) -> np.ndarray | None:
        """
        准备预测序列
        
        :param recent_data: 最近的数据
        :return: 序列数组
        """
        try:
            sequence = []
            for draw in recent_data:
                red_balls = self.get_red_balls(draw)
                encoded = self._encode_numbers(red_balls)
                sequence.append(encoded)
            
            # 确保序列长度正确
            if len(sequence) < self.sequence_length:
                return None
            
            X = np.array([sequence[:self.sequence_length]])
            return X
            
        except Exception as e:
            log.error(f'序列准备失败: {e}')
            return None

