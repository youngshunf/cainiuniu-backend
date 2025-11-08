from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.lottery.model import MembershipPlan, UserMembership
from backend.app.lottery.schema.membership import (
    AddMembershipPlanParam,
    AddUserMembershipParam,
    UpdateMembershipPlanParam,
)


class CRUDMembershipPlan(CRUDPlus[MembershipPlan]):
    """会员套餐数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> MembershipPlan | None:
        """获取会员套餐详情"""
        return await self.select_model(db, pk)

    async def add(self, db: AsyncSession, obj: AddMembershipPlanParam) -> None:
        """添加会员套餐"""
        dict_obj = obj.model_dump()
        new_plan = self.model(**dict_obj)
        db.add(new_plan)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateMembershipPlanParam) -> int:
        """更新会员套餐"""
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """删除会员套餐"""
        return await self.delete_model(db, pk)

    async def get_select(self, status: int | None) -> Select:
        """获取会员套餐列表查询"""
        filters = {}
        if status is not None:
            filters['status'] = status
        return await self.select_order('sort_order', 'asc', **filters)

    async def get_free_plan(self, db: AsyncSession) -> MembershipPlan | None:
        """获取免费套餐"""
        from sqlalchemy import select
        stmt = select(self.model).where(self.model.price == 0, self.model.status == 1).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


class CRUDUserMembership(CRUDPlus[UserMembership]):
    """用户会员数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> UserMembership | None:
        """获取用户会员详情"""
        return await self.select_model(db, pk)

    async def get_by_user(self, db: AsyncSession, user_id: int) -> UserMembership | None:
        """通过用户ID获取会员信息"""
        return await self.select_model_by_column(db, user_id=user_id)

    async def add(self, db: AsyncSession, obj: AddUserMembershipParam) -> None:
        """添加用户会员"""
        dict_obj = obj.model_dump()
        new_membership = self.model(**dict_obj)
        db.add(new_membership)

    async def update_by_user_id(self, db: AsyncSession, user_id: int, update_data: dict) -> int:
        """通过用户ID更新会员信息"""
        return await self.update_model_by_column(db, update_data, user_id=user_id)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """删除用户会员"""
        return await self.delete_model(db, pk)
    
    async def get_all_active(self, db: AsyncSession) -> list[UserMembership]:
        """获取所有激活的会员"""
        from sqlalchemy import select
        stmt = select(self.model).where(self.model.is_active == True)  # noqa: E712
        result = await db.execute(stmt)
        return list(result.scalars().all())


membership_plan_dao: CRUDMembershipPlan = CRUDMembershipPlan(MembershipPlan)
user_membership_dao: CRUDUserMembership = CRUDUserMembership(UserMembership)

