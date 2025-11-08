from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.lottery.model import LotteryType
from backend.app.lottery.schema.lottery_type import AddLotteryTypeParam, UpdateLotteryTypeParam


class CRUDLotteryType(CRUDPlus[LotteryType]):
    """彩票类型数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> LotteryType | None:
        """获取彩票类型详情"""
        return await self.select_model(db, pk)

    async def get_by_code(self, db: AsyncSession, code: str) -> LotteryType | None:
        """通过代码获取彩票类型"""
        return await self.select_model_by_column(db, code=code)

    async def add(self, db: AsyncSession, obj: AddLotteryTypeParam) -> None:
        """添加彩票类型"""
        dict_obj = obj.model_dump()
        new_lottery_type = self.model(**dict_obj)
        db.add(new_lottery_type)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateLotteryTypeParam) -> int:
        """更新彩票类型"""
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """删除彩票类型"""
        return await self.delete_model(db, pk)

    async def get_select(
        self, category: str | None, status: int | None
    ) -> Select:
        """获取彩票类型列表查询"""
        filters = {}
        if category:
            filters['category'] = category
        if status is not None:
            filters['status'] = status
        return await self.select_order(
            'id', 'asc',
            load_strategies={'draw_results': 'noload'},
            **filters
        )

    async def get_all_active(self, db: AsyncSession) -> list[LotteryType]:
        """获取所有启用的彩票类型"""
        stmt = select(self.model).where(self.model.status == 1).order_by(self.model.id)
        result = await db.execute(stmt)
        return list(result.scalars().all())


lottery_type_dao: CRUDLotteryType = CRUDLotteryType(LotteryType)

