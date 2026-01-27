"""
平台适配器集成模块

从 agent-core 导入平台适配器，供云端使用。
所有平台配置从 YAML 文件加载，确保云端和桌面端具有相同的平台能力。

@author Ysf
@date 2026-01-22
"""

from typing import Any

# 兼容别名
ContentSpec = dict
ContentConstraints = ContentSpec


def get_supported_platforms() -> list[dict[str, Any]]:
    """
    获取支持的平台列表

    Returns:
        平台信息列表
    """
    return []


def get_platform_spec(platform: str) -> ContentSpec | None:
    """
    获取平台内容规格

    Args:
        platform: 平台名称

    Returns:
        内容规格或 None
    """
    return None


def get_platform_url(platform: str, url_name: str) -> str | None:
    """
    获取平台 URL

    Args:
        platform: 平台名称
        url_name: URL 名称 (home, login, publish, etc.)

    Returns:
        URL 或 None
    """
    return None


def get_platform_selector(platform: str, selector_name: str, default: str = "") -> str:
    """
    获取平台选择器
    """
    return default

def list_platforms() -> list[str]:
    return []

def get_adapter(platform: str) -> Any:
    raise ValueError(f"Platform {platform} not supported (agent_core disabled)")

def adapt_content_for_platform(platform: str, title: str, content: str, **kwargs) -> dict:
    return {"title": title, "content": content}
