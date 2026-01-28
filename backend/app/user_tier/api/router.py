from fastapi import APIRouter

from backend.app.user_tier.api.v1.model_credit_rate import router as model_credit_rate_router
from backend.app.user_tier.api.v1.subscription_tier import router as subscription_tier_router
from backend.app.user_tier.api.v1.user_subscription import router as user_subscription_router
from backend.app.user_tier.api.v1.credit_package import router as credit_package_router
from backend.app.user_tier.api.v1.credit_transaction import router as credit_transaction_router
from backend.core.conf import settings

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/user_tier', tags=['模型积分费率'])

v1.include_router(credit_transaction_router, prefix='/credit/transactions')
v1.include_router(credit_package_router, prefix='/credit/packages')
v1.include_router(user_subscription_router, prefix='/user/subscriptions')
v1.include_router(subscription_tier_router, prefix='/subscription/tiers')
v1.include_router(model_credit_rate_router, prefix='/model/credit/rates')
