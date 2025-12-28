"""
云端浏览器工具 - 使用浏览器池执行发布操作

@author Ysf
@date 2025-12-28
"""

from typing import Any, Dict, Optional

from agent_core.tools.base import (
    ToolInterface,
    ToolMetadata,
    ToolCapability,
    ToolResult,
)
from agent_core.runtime.interfaces import RuntimeType
from agent_core.runtime.context import RuntimeContext


class CloudBrowserPublishTool(ToolInterface):
    """
    云端浏览器发布工具

    使用云端浏览器池执行发布操作。
    需要用户开启凭证同步功能。
    """

    metadata = ToolMetadata(
        name="browser_publish",
        description="使用云端浏览器池发布内容到社交平台",
        capabilities=[ToolCapability.BROWSER_AUTOMATION],
        supported_runtimes=[RuntimeType.CLOUD],
    )

    async def execute(
        self,
        ctx: RuntimeContext,
        *,
        platform: str,
        account_id: str,
        content: Dict[str, Any],
    ) -> ToolResult:
        """
        执行云端浏览器发布

        Args:
            ctx: 运行时上下文
            platform: 目标平台
            account_id: 账号ID
            content: 发布内容

        Returns:
            ToolResult: 执行结果
        """
        try:
            # 获取浏览器池
            browser_pool = ctx.extra.get("browser_pool")
            if not browser_pool:
                return ToolResult(
                    success=False,
                    data=None,
                    error="浏览器池未配置",
                )

            # 获取用户同步的凭证
            credential = await self._get_synced_credential(
                ctx, platform, account_id
            )
            if not credential:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"未找到同步的凭证: {platform}/{account_id}，请在桌面端开启凭证同步",
                )

            # 从浏览器池获取实例
            browser_context = await browser_pool.acquire(platform, credential)

            try:
                # 执行发布
                result = await browser_context.publish(content)

                return ToolResult(
                    success=True,
                    data={
                        "platform": platform,
                        "account_id": account_id,
                        "result": result,
                    },
                )

            finally:
                # 释放浏览器实例
                await browser_pool.release(browser_context)

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=f"云端发布失败: {str(e)}",
            )

    async def _get_synced_credential(
        self,
        ctx: RuntimeContext,
        platform: str,
        account_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        获取用户同步的凭证

        Args:
            ctx: 运行时上下文
            platform: 平台名称
            account_id: 账号ID

        Returns:
            凭证数据或 None
        """
        db = ctx.extra.get("db")
        if not db:
            return None

        # TODO: 从数据库查询用户同步的凭证
        # 需要实现凭证同步功能后完善
        return None

    def get_schema(self) -> Dict[str, Any]:
        """获取工具参数 Schema"""
        return {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "description": "目标平台",
                    "enum": ["xiaohongshu", "douyin", "weibo", "wechat_mp", "bilibili"],
                },
                "account_id": {
                    "type": "string",
                    "description": "账号ID",
                },
                "content": {
                    "type": "object",
                    "description": "发布内容",
                },
            },
            "required": ["platform", "account_id", "content"],
        }
