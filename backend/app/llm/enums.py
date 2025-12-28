"""LLM 模块枚举定义"""

from enum import StrEnum


class ModelType(StrEnum):
    """模型类型"""

    TEXT = 'TEXT'
    REASONING = 'REASONING'
    VISION = 'VISION'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    EMBEDDING = 'EMBEDDING'
    TTS = 'TTS'
    STT = 'STT'


class ApiKeyStatus(StrEnum):
    """API Key 状态"""

    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'
    EXPIRED = 'EXPIRED'
    REVOKED = 'REVOKED'


class UsageLogStatus(StrEnum):
    """用量日志状态"""

    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


class CircuitState(StrEnum):
    """熔断器状态"""

    CLOSED = 'CLOSED'
    OPEN = 'OPEN'
    HALF_OPEN = 'HALF_OPEN'
