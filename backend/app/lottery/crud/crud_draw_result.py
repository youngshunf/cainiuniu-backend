from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.lottery.model import DrawResult
from backend.app.lottery.schema.draw_result import AddDrawResultParam, UpdateDrawResultParam
from backend.utils.timezone import timezone


class CRUDDrawResult(CRUDPlus[DrawResult]):
    """开奖结果数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> DrawResult | None:
        """获取开奖结果详情"""
        return await self.select_model(db, pk)

    async def get_by_lottery_and_period(
        self, db: AsyncSession, lottery_code: str, period: str
    ) -> DrawResult | None:
        """通过彩种和期号获取开奖结果"""
        return await self.select_model_by_column(db, lottery_code=lottery_code, period=period)

    async def add(self, db: AsyncSession, obj: AddDrawResultParam) -> None:
        """添加开奖结果"""
        dict_obj = obj.model_dump()
        dict_obj['sync_time'] = timezone.now()
        new_draw_result = self.model(**dict_obj)
        db.add(new_draw_result)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDrawResultParam) -> int:
        """更新开奖结果"""
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """删除开奖结果"""
        return await self.delete_model(db, pk)

    async def get_select(
        self,
        lottery_code: str | None,
        period: str | None,
        start_date: date | None,
        end_date: date | None,
    ) -> Select:
        """获取开奖结果列表查询"""
        filters = {}
        if lottery_code:
            filters['lottery_code'] = lottery_code
        if period:
            filters['period__like'] = f'%{period}%'
        
        stmt = await self.select_order(
            'draw_date', 'desc',
            load_strategies={'lottery_type': 'noload'},
            **filters
        )
        
        if start_date:
            stmt = stmt.where(self.model.draw_date >= start_date)
        if end_date:
            stmt = stmt.where(self.model.draw_date <= end_date)
        
        return stmt

    async def get_latest_by_lottery(self, db: AsyncSession, lottery_code: str) -> DrawResult | None:
        """获取指定彩种的最新开奖结果"""
        stmt = (
            select(self.model)
            .where(self.model.lottery_code == lottery_code)
            .order_by(self.model.draw_date.desc(), self.model.period.desc())
            .limit(1)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_history_by_lottery(
        self, db: AsyncSession, lottery_code: str, limit: int = 100
    ) -> list[DrawResult]:
        """获取指定彩种的历史开奖记录"""
        stmt = (
            select(self.model)
            .where(self.model.lottery_code == lottery_code)
            .order_by(self.model.draw_date.desc(), self.model.period.desc())
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())


draw_result_dao: CRUDDrawResult = CRUDDrawResult(DrawResult)

