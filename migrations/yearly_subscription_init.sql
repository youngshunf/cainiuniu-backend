-- =====================================================
-- 年度订阅功能数据库迁移脚本
-- 执行方式: psql -h localhost -U postgres -d creator_flow -f migrations/yearly_subscription_init.sql
-- =====================================================

-- 1. 添加订阅等级表的年费字段
-- =====================================================
ALTER TABLE subscription_tier 
ADD COLUMN IF NOT EXISTS yearly_price NUMERIC;

ALTER TABLE subscription_tier 
ADD COLUMN IF NOT EXISTS yearly_discount NUMERIC;

COMMENT ON COLUMN subscription_tier.yearly_price IS '年费价格';
COMMENT ON COLUMN subscription_tier.yearly_discount IS '年费折扣 (如 0.8 表示8折)';


-- 2. 添加用户订阅表的新字段
-- =====================================================
ALTER TABLE user_subscription 
ADD COLUMN IF NOT EXISTS subscription_type VARCHAR(16) DEFAULT 'monthly';

ALTER TABLE user_subscription 
ADD COLUMN IF NOT EXISTS subscription_start_date TIMESTAMPTZ;

ALTER TABLE user_subscription 
ADD COLUMN IF NOT EXISTS subscription_end_date TIMESTAMPTZ;

ALTER TABLE user_subscription 
ADD COLUMN IF NOT EXISTS next_grant_date TIMESTAMPTZ;

COMMENT ON COLUMN user_subscription.subscription_type IS '订阅类型 (monthly:月度/yearly:年度)';
COMMENT ON COLUMN user_subscription.subscription_start_date IS '订阅开始时间';
COMMENT ON COLUMN user_subscription.subscription_end_date IS '订阅结束时间';
COMMENT ON COLUMN user_subscription.next_grant_date IS '下次赠送积分时间 (年度订阅专用)';


-- 3. 配置订阅等级的年费价格
-- =====================================================
-- 免费版不需要年费
UPDATE subscription_tier 
SET yearly_price = NULL, yearly_discount = NULL 
WHERE tier_name = 'free';

-- Pro 专业版: 月费 29 元，年费 8 折 = 29 * 12 * 0.8 = 278.4 ≈ 279 元
UPDATE subscription_tier 
SET yearly_price = 279, yearly_discount = 0.80 
WHERE tier_name = 'pro';

-- Max 旗舰版: 月费 99 元，年费 8 折 = 99 * 12 * 0.8 = 950.4 ≈ 950 元
UPDATE subscription_tier 
SET yearly_price = 950, yearly_discount = 0.80 
WHERE tier_name = 'max';

-- Ultra 至尊版: 月费 199 元，年费 75 折 = 199 * 12 * 0.75 = 1791 元
UPDATE subscription_tier 
SET yearly_price = 1791, yearly_discount = 0.75 
WHERE tier_name = 'ultra';


-- 4. 如果有其他等级，使用通用规则设置年费 (8折)
-- =====================================================
UPDATE subscription_tier 
SET 
    yearly_price = ROUND(monthly_price * 12 * 0.8),
    yearly_discount = 0.80
WHERE tier_name NOT IN ('free', 'pro', 'max', 'ultra')
  AND yearly_price IS NULL
  AND monthly_price > 0;


-- 5. 验证数据
-- =====================================================
SELECT 
    tier_name AS "等级",
    display_name AS "名称",
    monthly_credits AS "月积分",
    monthly_price AS "月费",
    yearly_price AS "年费",
    yearly_discount AS "折扣",
    CASE 
        WHEN yearly_price IS NOT NULL 
        THEN ROUND(yearly_price / 12, 2) 
        ELSE NULL 
    END AS "月均价"
FROM subscription_tier 
ORDER BY sort_order;

-- 完成提示
SELECT '✓ 年度订阅功能数据库迁移完成' AS message;
