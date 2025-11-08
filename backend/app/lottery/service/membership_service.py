"""会员服务"""

import secrets
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.lottery.crud import membership_plan_dao, user_membership_dao
from backend.app.lottery.crud.crud_api_usage import api_usage_dao
from backend.common.exception import errors
from backend.common.log import log
from backend.utils.timezone import timezone


class MembershipService:
    """会员服务"""

    @staticmethod
    async def activate_membership(
        db: AsyncSession, user_id: int, plan_id: int, auto_renew: bool = False
    ) -> dict:
        """
        激活会员
        
        :param db: 数据库会话
        :param user_id: 用户ID
        :param plan_id: 套餐ID
        :param auto_renew: 是否自动续费
        :return: 激活结果
        """
        # 获取套餐信息
        plan = await membership_plan_dao.get(db, plan_id)
        if not plan or plan.status != 1:
            raise errors.NotFoundError(msg='套餐不存在或已停用')
        
        # 检查是否已有会员
        existing = await user_membership_dao.get_by_user(db, user_id)
        
        now = timezone.now()
        start_date = now
        
        if existing and existing.is_active and existing.end_date > now:
            # 如果当前会员还有效，从结束日期开始计算
            start_date = existing.end_date
        
        end_date = start_date + timedelta(days=plan.duration_days)
        
        if existing:
            # 更新现有会员
            await user_membership_dao.update(db, existing.id, {
                'plan_id': plan_id,
                'start_date': start_date,
                'end_date': end_date,
                'is_active': True,
                'auto_renew': auto_renew,
                'remaining_predictions_today': plan.max_predictions_per_day,
                'remaining_api_quota_today': plan.api_quota_per_day,
            })
        else:
            # 创建新会员
            from backend.app.lottery.schema.membership import AddUserMembershipParam
            membership_param = AddUserMembershipParam(
                user_id=user_id,
                plan_id=plan_id,
                start_date=start_date,
                end_date=end_date,
                is_active=True,
                auto_renew=auto_renew,
                remaining_predictions_today=plan.max_predictions_per_day,
                remaining_api_quota_today=plan.api_quota_per_day,
            )
            await user_membership_dao.add(db, membership_param)
        
        await db.commit()
        
        return {
            'success': True,
            'user_id': user_id,
            'plan_name': plan.name,
            'start_date': str(start_date),
            'end_date': str(end_date),
        }

    @staticmethod
    async def check_membership_permission(
        db: AsyncSession, user_id: int, action: str
    ) -> dict:
        """
        检查会员权限
        
        :param db: 数据库会话
        :param user_id: 用户ID
        :param action: 操作类型 (prediction/ml_method/api_call等)
        :return: 权限检查结果
        """
        membership = await user_membership_dao.get_by_user(db, user_id)
        
        # 没有会员记录，分配免费会员
        if not membership:
            return await MembershipService._assign_free_membership(db, user_id)
        
        # 检查会员是否过期
        if not membership.is_active or membership.end_date < timezone.now():
            return {
                'allowed': False,
                'reason': '会员已过期',
                'plan_name': '已过期',
            }
        
        # 获取套餐信息
        plan = await membership_plan_dao.get(db, membership.plan_id)
        if not plan:
            return {
                'allowed': False,
                'reason': '套餐不存在',
            }
        
        # 根据不同操作类型检查权限
        if action == 'prediction':
            # 检查今日预测次数
            if membership.remaining_predictions_today <= 0:
                return {
                    'allowed': False,
                    'reason': '今日预测次数已用完',
                    'plan_name': plan.name,
                }
            return {
                'allowed': True,
                'plan_name': plan.name,
                'remaining_predictions': membership.remaining_predictions_today,
            }
        
        elif action == 'ml_method':
            # 检查是否可使用机器学习方法
            if not plan.can_use_ml_methods:
                return {
                    'allowed': False,
                    'reason': '当前套餐不支持机器学习方法',
                    'plan_name': plan.name,
                }
            return {
                'allowed': True,
                'plan_name': plan.name,
            }
        
        elif action == 'api_call':
            # 检查API调用配额
            if not plan.can_use_api:
                return {
                    'allowed': False,
                    'reason': '当前套餐不支持API调用',
                    'plan_name': plan.name,
                }
            if membership.remaining_api_quota_today <= 0:
                return {
                    'allowed': False,
                    'reason': '今日API配额已用完',
                    'plan_name': plan.name,
                }
            return {
                'allowed': True,
                'plan_name': plan.name,
                'remaining_quota': membership.remaining_api_quota_today,
            }
        
        return {
            'allowed': True,
            'plan_name': plan.name,
        }

    @staticmethod
    async def consume_quota(
        db: AsyncSession, user_id: int, action: str, amount: int = 1
    ) -> None:
        """
        消耗配额
        
        :param db: 数据库会话
        :param user_id: 用户ID
        :param action: 操作类型
        :param amount: 消耗数量
        """
        membership = await user_membership_dao.get_by_user(db, user_id)
        if not membership:
            return
        
        if action == 'prediction':
            await user_membership_dao.update(db, membership.id, {
                'remaining_predictions_today': max(0, membership.remaining_predictions_today - amount),
            })
        elif action == 'api_call':
            await user_membership_dao.update(db, membership.id, {
                'remaining_api_quota_today': max(0, membership.remaining_api_quota_today - amount),
            })
        
        await db.commit()

    @staticmethod
    async def reset_daily_quota(db: AsyncSession) -> dict:
        """
        重置每日配额（定时任务）
        
        :param db: 数据库会话
        :return: 重置结果
        """
        try:
            memberships = await user_membership_dao.get_all_active(db)
            
            reset_count = 0
            for membership in memberships:
                plan = await membership_plan_dao.get(db, membership.plan_id)
                if plan:
                    await user_membership_dao.update(db, membership.id, {
                        'remaining_predictions_today': plan.max_predictions_per_day,
                        'remaining_api_quota_today': plan.api_quota_per_day,
                    })
                    reset_count += 1
            
            await db.commit()
            
            log.info(f'每日配额重置完成，共重置 {reset_count} 个会员')
            return {
                'success': True,
                'reset_count': reset_count,
            }
        except Exception as e:
            log.error(f'每日配额重置失败: {e}')
            return {
                'success': False,
                'error': str(e),
            }

    @staticmethod
    async def generate_api_key(user_id: int) -> str:
        """
        生成API密钥
        
        :param user_id: 用户ID
        :return: API密钥
        """
        # 格式: cnn_{user_id}_{random_string}
        random_str = secrets.token_urlsafe(32)
        api_key = f'cnn_{user_id}_{random_str}'
        return api_key

    @staticmethod
    async def _assign_free_membership(db: AsyncSession, user_id: int) -> dict:
        """
        分配免费会员
        
        :param db: 数据库会话
        :param user_id: 用户ID
        :return: 会员信息
        """
        # 查找免费套餐
        free_plan = await membership_plan_dao.get_free_plan(db)
        if not free_plan:
            return {
                'allowed': False,
                'reason': '系统配置错误：免费套餐不存在',
            }
        
        # 激活免费会员
        await MembershipService.activate_membership(db, user_id, free_plan.id)
        
        return {
            'allowed': True,
            'plan_name': free_plan.name,
            'remaining_predictions': free_plan.max_predictions_per_day,
        }


membership_service = MembershipService()

