-- =====================================================
-- 测试用户 菜单初始化 SQL (PostgreSQL)
-- 自动生成于: 2026-01-28 11:37:24.452557+08:00
-- =====================================================

-- 父级菜单
INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
('测试用户', 'TestUser', '/admin', 1, 'lucide:list', 1, '#/views/admin/index.vue', NULL, 1, 1, 1, '', '测试用户管理', NULL, NOW(), NULL)
RETURNING id AS parent_menu_id;

-- 获取刚插入的父菜单 ID（存储到变量中用于后续按钮菜单）
DO $$
DECLARE
    v_parent_menu_id INTEGER;
BEGIN
    -- 获取刚插入的父菜单 ID
    SELECT id INTO v_parent_menu_id FROM sys_menu 
    WHERE name = 'TestUser' AND path = '/admin'
    ORDER BY id DESC LIMIT 1;

    -- 新增按钮
    INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
    VALUES
    ('新增', 'AddTestUser', NULL, 1, NULL, 2, NULL, 'test:user:add', 1, 0, 1, '', NULL, v_parent_menu_id, NOW(), NULL);

    -- 编辑按钮
    INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
    VALUES
    ('编辑', 'EditTestUser', NULL, 2, NULL, 2, NULL, 'test:user:edit', 1, 0, 1, '', NULL, v_parent_menu_id, NOW(), NULL);

    -- 删除按钮
    INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
    VALUES
    ('删除', 'DeleteTestUser', NULL, 3, NULL, 2, NULL, 'test:user:del', 1, 0, 1, '', NULL, v_parent_menu_id, NOW(), NULL);

    -- 查看按钮
    INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
    VALUES
    ('查看', 'ViewTestUser', NULL, 4, NULL, 2, NULL, 'test:user:get', 1, 0, 1, '', NULL, v_parent_menu_id, NOW(), NULL);
END $$;

-- =====================================================
-- 菜单生成完成
-- =====================================================
