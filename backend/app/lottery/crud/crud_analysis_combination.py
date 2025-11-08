from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.lottery.model import AnalysisCombination
from backend.app.lottery.schema.analysis_combination import AddCombinationParam, UpdateCombinationParam


class CRUDAnalysisCombination(CRUDPlus[AnalysisCombination]):
    """分析组合数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> AnalysisCombination | None:
        """获取分析组合详情"""
        return await self.select_model(db, pk)

    async def add(self, db: AsyncSession, obj: AddCombinationParam, user_id: int) -> None:
        """添加分析组合"""
        dict_obj = obj.model_dump()
        dict_obj['user_id'] = user_id
        new_combination = self.model(**dict_obj)
        db.add(new_combination)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateCombinationParam) -> int:
        """更新分析组合"""
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """删除分析组合"""
        return await self.delete_model(db, pk)

    async def get_select(
        self, user_id: int | None, lottery_code: str | None, is_auto: bool | None, status: int | None
    ) -> Select:
        """获取分析组合列表查询"""
        filters = {}
        if user_id is not None:
            filters['user_id'] = user_id
        if lottery_code:
            filters['lottery_code'] = lottery_code
        if is_auto is not None:
            filters['is_auto'] = is_auto
        if status is not None:
            filters['status'] = status
        return await self.select_order('created_time', 'desc', **filters)

    async def increment_use_count(self, db: AsyncSession, pk: int) -> int:
        """增加使用次数"""
        combination = await self.get(db, pk)
        if combination:
            return await self.update_model(db, pk, {'use_count': combination.use_count + 1})
        return 0

    async def update_accuracy_rate(self, db: AsyncSession, pk: int, accuracy_rate: float) -> int:
        """更新准确率"""
        return await self.update_model(db, pk, {'accuracy_rate': accuracy_rate})


combination_dao: CRUDAnalysisCombination = CRUDAnalysisCombination(AnalysisCombination)

