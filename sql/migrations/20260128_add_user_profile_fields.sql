-- Migration: 添加用户扩展资料字段
-- Date: 2026-01-28
-- Description: 为 sys_user 表添加性别、生日、省市区、行业、简介等扩展字段

-- 添加性别字段
ALTER TABLE sys_user ADD COLUMN IF NOT EXISTS gender VARCHAR(10) DEFAULT NULL;
COMMENT ON COLUMN sys_user.gender IS '性别(male/female/other)';

-- 添加生日字段
ALTER TABLE sys_user ADD COLUMN IF NOT EXISTS birthday VARCHAR(10) DEFAULT NULL;
COMMENT ON COLUMN sys_user.birthday IS '生日(YYYY-MM-DD)';

-- 添加省份字段
ALTER TABLE sys_user ADD COLUMN IF NOT EXISTS province VARCHAR(64) DEFAULT NULL;
COMMENT ON COLUMN sys_user.province IS '省份';

-- 添加城市字段
ALTER TABLE sys_user ADD COLUMN IF NOT EXISTS city VARCHAR(64) DEFAULT NULL;
COMMENT ON COLUMN sys_user.city IS '城市';

-- 添加区字段
ALTER TABLE sys_user ADD COLUMN IF NOT EXISTS district VARCHAR(64) DEFAULT NULL;
COMMENT ON COLUMN sys_user.district IS '区';

-- 添加行业字段
ALTER TABLE sys_user ADD COLUMN IF NOT EXISTS industry VARCHAR(128) DEFAULT NULL;
COMMENT ON COLUMN sys_user.industry IS '行业';

-- 添加个人简介字段
ALTER TABLE sys_user ADD COLUMN IF NOT EXISTS bio TEXT DEFAULT NULL;
COMMENT ON COLUMN sys_user.bio IS '个人简介';

-- 回滚脚本 (如需回滚，执行以下语句):
-- ALTER TABLE sys_user DROP COLUMN IF EXISTS gender;
-- ALTER TABLE sys_user DROP COLUMN IF EXISTS birthday;
-- ALTER TABLE sys_user DROP COLUMN IF EXISTS province;
-- ALTER TABLE sys_user DROP COLUMN IF EXISTS city;
-- ALTER TABLE sys_user DROP COLUMN IF EXISTS district;
-- ALTER TABLE sys_user DROP COLUMN IF EXISTS industry;
-- ALTER TABLE sys_user DROP COLUMN IF EXISTS bio;
