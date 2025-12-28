"""模型组 CRUD"""

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.llm.model.model_group import ModelGroup
from backend.app.llm.schema.model_group import CreateModelGroupParam, UpdateModelGroupParam


class CRUDModelGroup(CRUDPlus[ModelGroup]):
    """模型组数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> ModelGroup | None:
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> ModelGroup | None:
        return await self.select_model_by_column(db, name=name)

    async def get_list(
        self,
        *,
        name: str | None = None,
        model_type: str | None = None,
        enabled: bool | None = None,
    ) -> Select:
        filters = {}
        if name is not None:
            filters['name__like'] = f'%{name}%'
        if model_type is not None:
            filters['model_type'] = model_type
        if enabled is not None:
            filters['enabled'] = enabled
        return await self.select_order('id', 'desc', **filters)

    async def get_all_enabled(self, db: AsyncSession) -> list[ModelGroup]:
        stmt = await self.select_order('id', 'asc', enabled=True)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_type(self, db: AsyncSession, model_type: str) -> ModelGroup | None:
        return await self.select_model_by_column(db, model_type=model_type, enabled=True)

    async def create(self, db: AsyncSession, obj: CreateModelGroupParam) -> None:
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateModelGroupParam) -> int:
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        return await self.delete_model(db, pk)


model_group_dao: CRUDModelGroup = CRUDModelGroup(ModelGroup)
