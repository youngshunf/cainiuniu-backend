from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.lottery.model import AnalysisMethod
from backend.app.lottery.schema.analysis_method import AddMethodParam, UpdateMethodParam


class CRUDAnalysisMethod(CRUDPlus[AnalysisMethod]):
    """分析方法数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> AnalysisMethod | None:
        """获取分析方法详情"""
        return await self.select_model(db, pk)

    async def get_by_code(self, db: AsyncSession, code: str) -> AnalysisMethod | None:
        """通过代码获取分析方法"""
        return await self.select_model_by_column(db, code=code)

    async def add(self, db: AsyncSession, obj: AddMethodParam) -> None:
        """添加分析方法"""
        dict_obj = obj.model_dump()
        new_method = self.model(**dict_obj)
        db.add(new_method)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateMethodParam) -> int:
        """更新分析方法"""
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """删除分析方法"""
        return await self.delete_model(db, pk)

    async def get_select(
        self, category: str | None, is_premium: bool | None, status: int | None
    ) -> Select:
        """获取分析方法列表查询"""
        filters = {}
        if category:
            filters['category'] = category
        if is_premium is not None:
            filters['is_premium'] = is_premium
        if status is not None:
            filters['status'] = status
        return await self.select_order('id', 'asc', **filters)

    async def get_by_ids(self, db: AsyncSession, ids: list[int]) -> list[AnalysisMethod]:
        """通过ID列表获取分析方法"""
        stmt = select(self.model).where(self.model.id.in_(ids), self.model.status == 1)
        result = await db.execute(stmt)
        return list(result.scalars().all())


method_dao: CRUDAnalysisMethod = CRUDAnalysisMethod(AnalysisMethod)

