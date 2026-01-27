-- =====================================================
-- 项目私有选题 菜单初始化 SQL (MySQL)
-- 自动生成于: 2026-01-27 18:38:40.956658+08:00
-- =====================================================

-- 父级菜单
INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
('项目私有选题', 'ProjectTopics', '/projects', 1, 'lucide:list', 1, '#/views/projects/index.vue', NULL, 1, 1, 1, '', '项目私有选题管理', NULL, NOW(), NULL);

-- 获取刚插入的父菜单 ID
SET @parent_menu_id = LAST_INSERT_ID();

-- 新增按钮
INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
('新增', 'AddProjectTopics', NULL, 1, NULL, 2, NULL, 'project:topics:add', 1, 0, 1, '', NULL, @parent_menu_id, NOW(), NULL);

-- 编辑按钮
INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
('编辑', 'EditProjectTopics', NULL, 2, NULL, 2, NULL, 'project:topics:edit', 1, 0, 1, '', NULL, @parent_menu_id, NOW(), NULL);

-- 删除按钮
INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
('删除', 'DeleteProjectTopics', NULL, 3, NULL, 2, NULL, 'project:topics:del', 1, 0, 1, '', NULL, @parent_menu_id, NOW(), NULL);

-- 查看按钮
INSERT INTO sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
VALUES
('查看', 'ViewProjectTopics', NULL, 4, NULL, 2, NULL, 'project:topics:get', 1, 0, 1, '', NULL, @parent_menu_id, NOW(), NULL);

-- =====================================================
-- 菜单生成完成
-- =====================================================
