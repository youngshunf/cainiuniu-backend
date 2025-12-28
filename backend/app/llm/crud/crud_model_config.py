"""模型配置 CRUD"""

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.llm.model.model_config import ModelConfig
from backend.app.llm.schema.model_config import CreateModelConfigParam, UpdateModelConfigParam


class CRUDModelConfig(CRUDPlus[ModelConfig]):
    """模型配置数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> ModelConfig | None:
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, model_name: str) -> ModelConfig | None:
        return await self.select_model_by_column(db, model_name=model_name)

    async def get_list(
        self,
        *,
        provider_id: int | None = None,
        model_type: str | None = None,
        model_name: str | None = None,
        enabled: bool | None = None,
    ) -> Select:
        filters = {}
        if provider_id is not None:
            filters['provider_id'] = provider_id
        if model_type is not None:
            filters['model_type'] = model_type
        if model_name is not None:
            filters['model_name__like'] = f'%{model_name}%'
        if enabled is not None:
            filters['enabled'] = enabled
        return await self.select_order('priority', 'desc', **filters)

    async def get_all_enabled(self, db: AsyncSession) -> list[ModelConfig]:
        stmt = await self.select_order('priority', 'desc', enabled=True)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_provider(self, db: AsyncSession, provider_id: int) -> list[ModelConfig]:
        stmt = await self.select_order('priority', 'desc', provider_id=provider_id, enabled=True)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj: CreateModelConfigParam) -> None:
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateModelConfigParam) -> int:
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        return await self.delete_model(db, pk)


model_config_dao: CRUDModelConfig = CRUDModelConfig(ModelConfig)
