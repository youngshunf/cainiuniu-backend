from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.lottery.model import PredictionResult
from backend.app.lottery.schema.prediction import AddPredictionParam, UpdatePredictionParam


class CRUDPredictionResult(CRUDPlus[PredictionResult]):
    """预测结果数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> PredictionResult | None:
        """获取预测结果详情"""
        return await self.select_model(db, pk)

    async def add(self, db: AsyncSession, obj: AddPredictionParam, user_id: int | None = None) -> None:
        """添加预测结果"""
        dict_obj = obj.model_dump()
        dict_obj['user_id'] = user_id
        new_prediction = self.model(**dict_obj)
        db.add(new_prediction)

    async def update(self, db: AsyncSession, pk: int, obj: UpdatePredictionParam) -> int:
        """更新预测结果"""
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """删除预测结果"""
        return await self.delete_model(db, pk)

    async def get_select(
        self,
        user_id: int | None,
        lottery_code: str | None,
        target_period: str | None,
        is_verified: bool | None,
    ) -> Select:
        """获取预测结果列表查询"""
        filters = {}
        if user_id is not None:
            filters['user_id'] = user_id
        if lottery_code:
            filters['lottery_code'] = lottery_code
        if target_period:
            filters['target_period'] = target_period
        if is_verified is not None:
            filters['is_verified'] = is_verified
        return await self.select_order('created_time', 'desc', **filters)


prediction_dao: CRUDPredictionResult = CRUDPredictionResult(PredictionResult)

