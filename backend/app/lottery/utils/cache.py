"""
彩票系统缓存工具模块

提供统一的缓存管理接口，支持Redis缓存。
"""

import json
from functools import wraps
from typing import Any, Callable

from backend.core.conf import settings
from backend.database.db_redis import redis_client


class CacheManager:
    """缓存管理器"""

    def __init__(self):
        self.redis = redis_client
        self.prefix = 'lottery:'

    def _get_key(self, key: str) -> str:
        """获取完整的缓存键"""
        return f'{self.prefix}{key}'

    async def get(self, key: str) -> Any | None:
        """
        获取缓存

        Args:
            key: 缓存键

        Returns:
            缓存值，不存在返回None
        """
        full_key = self._get_key(key)
        value = await self.redis.get(full_key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        设置缓存

        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），默认1小时

        Returns:
            是否成功
        """
        full_key = self._get_key(key)
        try:
            serialized_value = json.dumps(value, ensure_ascii=False)
            await self.redis.setex(full_key, ttl, serialized_value)
            return True
        except Exception as e:
            print(f'设置缓存失败: {e}')
            return False

    async def delete(self, key: str) -> bool:
        """
        删除缓存

        Args:
            key: 缓存键

        Returns:
            是否成功
        """
        full_key = self._get_key(key)
        try:
            await self.redis.delete(full_key)
            return True
        except Exception as e:
            print(f'删除缓存失败: {e}')
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """
        批量删除匹配的缓存

        Args:
            pattern: 匹配模式（支持通配符 *）

        Returns:
            删除的键数量
        """
        full_pattern = self._get_key(pattern)
        try:
            keys = await self.redis.keys(full_pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            print(f'批量删除缓存失败: {e}')
            return 0

    async def exists(self, key: str) -> bool:
        """
        检查缓存是否存在

        Args:
            key: 缓存键

        Returns:
            是否存在
        """
        full_key = self._get_key(key)
        return await self.redis.exists(full_key) > 0


# 全局缓存管理器实例
cache_manager = CacheManager()


def cache(key_pattern: str, ttl: int = 3600):
    """
    缓存装饰器

    Args:
        key_pattern: 缓存键模式，支持占位符 {0}, {1} 等
        ttl: 过期时间（秒）

    Example:
        @cache('lottery_type:list:{0}', ttl=3600)
        async def get_lottery_type_list(category: str):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = key_pattern.format(*args, **kwargs)

            # 尝试从缓存获取
            cached_value = await cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value

            # 执行函数
            result = await func(*args, **kwargs)

            # 设置缓存
            if result is not None:
                await cache_manager.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator


# 常用缓存键定义
class CacheKeys:
    """缓存键常量"""

    # 彩种相关
    LOTTERY_TYPE_LIST = 'lottery_type:list'
    LOTTERY_TYPE_DETAIL = 'lottery_type:detail:{}'  # lottery_type_id
    LOTTERY_TYPE_BY_CODE = 'lottery_type:code:{}'  # lottery_code

    # 开奖数据相关
    DRAW_LATEST = 'draw:latest:{}'  # lottery_code
    DRAW_DETAIL = 'draw:detail:{}:{}'  # lottery_code, period
    DRAW_HISTORY = 'draw:history:{}:{}'  # lottery_code, limit

    # 分析方法相关
    ANALYSIS_METHODS = 'analysis:methods'
    ANALYSIS_METHOD_DETAIL = 'analysis:method:{}'  # method_id

    # 预测相关
    PREDICTION_DETAIL = 'prediction:detail:{}'  # prediction_id

    # 组合相关
    COMBINATION_DETAIL = 'combination:detail:{}'  # combination_id


# 缓存 TTL 配置（秒）
class CacheTTL:
    """缓存过期时间配置"""

    # 彩种数据（1小时）
    LOTTERY_TYPE = 3600

    # 最新开奖（5分钟）
    DRAW_LATEST = 300

    # 历史开奖（30分钟）
    DRAW_HISTORY = 1800

    # 开奖详情（1小时）
    DRAW_DETAIL = 3600

    # 分析方法（1小时）
    ANALYSIS_METHOD = 3600

    # 预测结果（10分钟）
    PREDICTION = 600

    # 组合配置（30分钟）
    COMBINATION = 1800

