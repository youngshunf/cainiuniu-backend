"""代理 API - OpenAI/Anthropic 兼容"""

from fastapi import APIRouter, Header, Request
from fastapi.responses import StreamingResponse

from backend.app.llm.schema.proxy import (
    AnthropicMessageRequest,
    AnthropicMessageResponse,
    ChatCompletionRequest,
    ChatCompletionResponse,
)
from backend.app.llm.service.gateway_service import gateway_service
from backend.database.db import CurrentSession

router = APIRouter()


def _get_client_ip(request: Request) -> str | None:
    """获取客户端 IP"""
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.client.host if request.client else None


def _extract_api_key(authorization: str) -> str:
    """从 Authorization 头提取 API Key"""
    if authorization.startswith('Bearer '):
        return authorization[7:]
    return authorization


@router.post(
    '/v1/chat/completions',
    summary='OpenAI 兼容聊天补全',
    description='兼容 OpenAI Chat Completions API 格式',
    response_model=ChatCompletionResponse,
    response_model_exclude_none=True,
)
async def chat_completions(
    request: Request,
    db: CurrentSession,
    body: ChatCompletionRequest,
    authorization: str = Header(..., description='Bearer sk-xxx'),
) -> ChatCompletionResponse | StreamingResponse:
    api_key = _extract_api_key(authorization)
    ip_address = _get_client_ip(request)

    if body.stream:
        return StreamingResponse(
            gateway_service.chat_completion_stream(
                db,
                api_key=api_key,
                request=body,
                ip_address=ip_address,
            ),
            media_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no',
            },
        )

    return await gateway_service.chat_completion(
        db,
        api_key=api_key,
        request=body,
        ip_address=ip_address,
    )


@router.post(
    '/v1/messages',
    summary='Anthropic 兼容消息',
    description='兼容 Anthropic Messages API 格式',
    response_model=AnthropicMessageResponse,
    response_model_exclude_none=True,
)
async def anthropic_messages(
    request: Request,
    db: CurrentSession,
    body: AnthropicMessageRequest,
    x_api_key: str = Header(..., alias='x-api-key', description='API Key'),
) -> AnthropicMessageResponse | StreamingResponse:
    ip_address = _get_client_ip(request)

    if body.stream:
        return StreamingResponse(
            gateway_service.anthropic_messages_stream(
                db,
                api_key=x_api_key,
                request=body,
                ip_address=ip_address,
            ),
            media_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no',
            },
        )

    return await gateway_service.anthropic_messages(
        db,
        api_key=x_api_key,
        request=body,
        ip_address=ip_address,
    )
