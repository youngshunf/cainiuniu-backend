-- =====================================================
-- Test User 字典数据初始化 SQL
-- 自动生成于: 2026-01-27 15:32:05.689338
-- =====================================================

-- User Status 字典类型
INSERT INTO sys_dict_type (name, code, status, remark, created_time, updated_time)
VALUES
('User Status', 'test_status', 1, 'Test User模块-User Status', NOW(), NULL)
ON CONFLICT (code) DO NOTHING;

-- User Status 字典数据
DO $$
DECLARE
    v_dict_type_id INTEGER;
BEGIN
    SELECT id INTO v_dict_type_id FROM sys_dict_type
    WHERE code = 'test_status' ORDER BY id DESC LIMIT 1;

    INSERT INTO sys_dict_data (label, value, sort, status, color_type, type_id, remark, created_time, updated_time)
    VALUES
    ('启用', '1', 1, 1, 'green', v_dict_type_id, '', NOW(), NULL);
    INSERT INTO sys_dict_data (label, value, sort, status, color_type, type_id, remark, created_time, updated_time)
    VALUES
    ('禁用', '0', 2, 1, 'red', v_dict_type_id, '', NOW(), NULL);
END $$;

-- =====================================================
-- 字典数据生成完成
-- =====================================================