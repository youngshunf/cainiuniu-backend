from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.lottery.model import ApiUsage


class CRUDApiUsage(CRUDPlus[ApiUsage]):
    """API使用记录数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> ApiUsage | None:
        """获取API使用记录详情"""
        return await self.select_model(db, pk)

    async def add(
        self,
        db: AsyncSession,
        user_id: int,
        api_key: str,
        endpoint: str,
        request_params: str | None,
        response_status: int,
        quota_used: int,
        ip_address: str,
    ) -> None:
        """添加API使用记录"""
        new_usage = self.model(
            user_id=user_id,
            api_key=api_key,
            endpoint=endpoint,
            request_params=request_params,
            response_status=response_status,
            quota_used=quota_used,
            ip_address=ip_address,
        )
        db.add(new_usage)

    async def get_select(
        self, user_id: int | None, api_key: str | None, endpoint: str | None
    ) -> Select:
        """获取API使用记录列表查询"""
        filters = {}
        if user_id is not None:
            filters['user_id'] = user_id
        if api_key:
            filters['api_key'] = api_key
        if endpoint:
            filters['endpoint__like'] = f'%{endpoint}%'
        return await self.select_order('created_time', 'desc', **filters)


api_usage_dao: CRUDApiUsage = CRUDApiUsage(ApiUsage)

