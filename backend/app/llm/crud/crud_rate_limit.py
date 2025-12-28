"""速率限制配置 CRUD"""

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.llm.model.rate_limit import RateLimitConfig
from backend.app.llm.schema.rate_limit import CreateRateLimitConfigParam, UpdateRateLimitConfigParam


class CRUDRateLimitConfig(CRUDPlus[RateLimitConfig]):
    """速率限制配置数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> RateLimitConfig | None:
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> RateLimitConfig | None:
        return await self.select_model_by_column(db, name=name)

    async def get_list(
        self,
        *,
        name: str | None = None,
        enabled: bool | None = None,
    ) -> Select:
        filters = {}
        if name is not None:
            filters['name__like'] = f'%{name}%'
        if enabled is not None:
            filters['enabled'] = enabled
        return await self.select_order('id', 'desc', **filters)

    async def get_all_enabled(self, db: AsyncSession) -> list[RateLimitConfig]:
        stmt = await self.select_order('id', 'asc', enabled=True)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj: CreateRateLimitConfigParam) -> None:
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateRateLimitConfigParam) -> int:
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        return await self.delete_model(db, pk)


rate_limit_dao: CRUDRateLimitConfig = CRUDRateLimitConfig(RateLimitConfig)
