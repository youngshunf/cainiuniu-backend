-- =====================================================
-- 测试用户表 字典数据初始化 SQL
-- 自动生成于: 2026-01-28 11:37:24.570438
-- =====================================================

-- 状态 字典类型
INSERT INTO sys_dict_type (name, code, status, remark, created_time, updated_time)
VALUES
('状态', 'admin_status', 1, '测试用户表模块-状态', NOW(), NULL)
ON CONFLICT (code) DO NOTHING;

-- 状态 字典数据
DO $$
DECLARE
    v_dict_type_id INTEGER;
BEGIN
    SELECT id INTO v_dict_type_id FROM sys_dict_type
    WHERE code = 'admin_status' ORDER BY id DESC LIMIT 1;

    INSERT INTO sys_dict_data (label, value, sort, status, color_type, type_id, remark, created_time, updated_time)
    VALUES
    ('启用', '1', 1, 1, 'green', v_dict_type_id, '', NOW(), NULL);
    INSERT INTO sys_dict_data (label, value, sort, status, color_type, type_id, remark, created_time, updated_time)
    VALUES
    ('禁用', '0', 2, 1, 'red', v_dict_type_id, '', NOW(), NULL);
END $$;

-- 用户类型 字典类型
INSERT INTO sys_dict_type (name, code, status, remark, created_time, updated_time)
VALUES
('用户类型', 'admin_user_type', 1, '测试用户表模块-用户类型', NOW(), NULL)
ON CONFLICT (code) DO NOTHING;

-- 用户类型 字典数据
DO $$
DECLARE
    v_dict_type_id INTEGER;
BEGIN
    SELECT id INTO v_dict_type_id FROM sys_dict_type
    WHERE code = 'admin_user_type' ORDER BY id DESC LIMIT 1;

    INSERT INTO sys_dict_data (label, value, sort, status, color_type, type_id, remark, created_time, updated_time)
    VALUES
    ('类型1', '1', 1, 1, 'blue', v_dict_type_id, '', NOW(), NULL);
    INSERT INTO sys_dict_data (label, value, sort, status, color_type, type_id, remark, created_time, updated_time)
    VALUES
    ('类型2', '2', 2, 1, 'orange', v_dict_type_id, '', NOW(), NULL);
END $$;

-- =====================================================
-- 字典数据生成完成
-- =====================================================