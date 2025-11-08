-- 彩票系统菜单初始化SQL
-- 参照系统菜单结构，生成彩票管理模块的完整菜单

-- 说明：
-- type: 0=目录, 1=菜单页面, 2=按钮权限, 3=外链, 4=内链iframe
-- status: 1=启用, 0=停用
-- display: 1=显示, 0=隐藏
-- cache: 1=缓存, 0=不缓存

-- ========== 一级菜单：彩票管理 ==========
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (100, '彩票管理', 'Lottery', '/lottery', 3, 'lucide:trophy', 0, null, null, 1, 1, 1, '', '彩票分析预测系统', null, now(), null);

-- ========== 二级菜单 ==========

-- 1. 数据总览
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (101, '数据总览', 'LotteryDashboard', '/lottery/dashboard', 0, 'lucide:layout-dashboard', 1, '/lottery/dashboard/index', null, 1, 1, 1, '', '彩票数据统计概览', 100, now(), null);

-- 2. 彩种管理
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (102, '彩种管理', 'LotteryType', '/lottery/lottery-type', 1, 'lucide:list', 1, '/lottery/lottery-type/index', null, 1, 1, 1, '', '彩票类型管理', 100, now(), null);

-- 彩种管理按钮权限
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values 
(103, '新增', 'AddLotteryType', null, 0, null, 2, null, 'lottery:type:add', 1, 0, 1, '', null, 102, now(), null),
(104, '修改', 'EditLotteryType', null, 0, null, 2, null, 'lottery:type:edit', 1, 0, 1, '', null, 102, now(), null),
(105, '删除', 'DeleteLotteryType', null, 0, null, 2, null, 'lottery:type:del', 1, 0, 1, '', null, 102, now(), null),
(106, '查看', 'ViewLotteryType', null, 0, null, 2, null, 'lottery:type:view', 1, 0, 1, '', null, 102, now(), null);

-- 3. 开奖数据
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (107, '开奖数据', 'DrawResult', '/lottery/draw-result', 2, 'lucide:calendar-check', 1, '/lottery/draw-result/index', null, 1, 1, 1, '', '开奖结果管理', 100, now(), null);

-- 开奖数据按钮权限
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values 
(108, '查看', 'ViewDrawResult', null, 0, null, 2, null, 'lottery:draw:view', 1, 0, 1, '', null, 107, now(), null),
(109, '同步数据', 'SyncDrawResult', null, 0, null, 2, null, 'lottery:draw:sync', 1, 0, 1, '', null, 107, now(), null),
(110, '全量同步', 'SyncDrawHistory', null, 0, null, 2, null, 'lottery:draw:sync:history', 1, 0, 1, '', null, 107, now(), null),
(111, '删除', 'DeleteDrawResult', null, 0, null, 2, null, 'lottery:draw:del', 1, 0, 1, '', null, 107, now(), null);

-- 4. 分析方法
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (112, '分析方法', 'AnalysisMethod', '/lottery/analysis-method', 3, 'lucide:brain', 1, '/lottery/analysis-method/index', null, 1, 1, 1, '', '分析方法配置', 100, now(), null);

-- 分析方法按钮权限
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values 
(113, '查看', 'ViewAnalysisMethod', null, 0, null, 2, null, 'lottery:method:view', 1, 0, 1, '', null, 112, now(), null),
(114, '新增', 'AddAnalysisMethod', null, 0, null, 2, null, 'lottery:method:add', 1, 0, 1, '', null, 112, now(), null),
(115, '修改', 'EditAnalysisMethod', null, 0, null, 2, null, 'lottery:method:edit', 1, 0, 1, '', null, 112, now(), null),
(116, '删除', 'DeleteAnalysisMethod', null, 0, null, 2, null, 'lottery:method:del', 1, 0, 1, '', null, 112, now(), null);

-- 5. 组合管理
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (117, '组合管理', 'Combination', '/lottery/combination', 4, 'lucide:layers', 1, '/lottery/combination/index', null, 1, 1, 1, '', '分析组合管理', 100, now(), null);

-- 组合管理按钮权限
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values 
(118, '新增', 'AddCombination', null, 0, null, 2, null, 'lottery:combination:add', 1, 0, 1, '', null, 117, now(), null),
(119, '修改', 'EditCombination', null, 0, null, 2, null, 'lottery:combination:edit', 1, 0, 1, '', null, 117, now(), null),
(120, '删除', 'DeleteCombination', null, 0, null, 2, null, 'lottery:combination:del', 1, 0, 1, '', null, 117, now(), null),
(121, '查看', 'ViewCombination', null, 0, null, 2, null, 'lottery:combination:view', 1, 0, 1, '', null, 117, now(), null),
(122, '启用自动预测', 'EnableAutoPrediction', null, 0, null, 2, null, 'lottery:combination:auto', 1, 0, 1, '', null, 117, now(), null);

-- 6. 预测管理
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (123, '预测管理', 'Prediction', '/lottery/prediction', 5, 'lucide:sparkles', 1, '/lottery/prediction/index', null, 1, 1, 1, '', '预测结果管理', 100, now(), null);

-- 预测管理按钮权限
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values 
(124, '创建预测', 'CreatePrediction', null, 0, null, 2, null, 'lottery:prediction:create', 1, 0, 1, '', null, 123, now(), null),
(125, '查看分析', 'ViewPredictionArticle', null, 0, null, 2, null, 'lottery:prediction:view', 1, 0, 1, '', null, 123, now(), null),
(126, '验证结果', 'VerifyPrediction', null, 0, null, 2, null, 'lottery:prediction:verify', 1, 0, 1, '', null, 123, now(), null),
(127, '删除', 'DeletePrediction', null, 0, null, 2, null, 'lottery:prediction:del', 1, 0, 1, '', null, 123, now(), null),
(128, '导出', 'ExportPrediction', null, 0, null, 2, null, 'lottery:prediction:export', 1, 0, 1, '', null, 123, now(), null);

-- 7. 会员管理
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (129, '会员管理', 'Membership', '/lottery/membership', 6, 'lucide:crown', 1, '/lottery/membership/index', null, 1, 1, 1, '', '会员套餐管理', 100, now(), null);

-- 会员管理按钮权限
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values 
(130, '新增套餐', 'AddMembershipPlan', null, 0, null, 2, null, 'lottery:membership:add', 1, 0, 1, '', null, 129, now(), null),
(131, '修改套餐', 'EditMembershipPlan', null, 0, null, 2, null, 'lottery:membership:edit', 1, 0, 1, '', null, 129, now(), null),
(132, '删除套餐', 'DeleteMembershipPlan', null, 0, null, 2, null, 'lottery:membership:del', 1, 0, 1, '', null, 129, now(), null),
(133, '查看用户', 'ViewUserMembership', null, 0, null, 2, null, 'lottery:membership:user:view', 1, 0, 1, '', null, 129, now(), null),
(134, '激活会员', 'ActivateUserMembership', null, 0, null, 2, null, 'lottery:membership:user:activate', 1, 0, 1, '', null, 129, now(), null);

-- 8. 统计报表（扩展功能）
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values (135, '统计报表', 'LotteryStatistics', '/lottery/statistics', 7, 'lucide:bar-chart', 1, '/lottery/statistics/index', null, 1, 1, 1, '', '数据统计与分析', 100, now(), null);

-- 统计报表按钮权限
insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values 
(136, '查看统计', 'ViewStatistics', null, 0, null, 2, null, 'lottery:statistics:view', 1, 0, 1, '', null, 135, now(), null),
(137, '导出报表', 'ExportStatistics', null, 0, null, 2, null, 'lottery:statistics:export', 1, 0, 1, '', null, 135, now(), null);

-- ========== 为测试角色分配彩票菜单权限 ==========
-- 假设测试角色ID为1，为其分配所有彩票相关菜单

insert into sys_role_menu (role_id, menu_id)
select 1, id from sys_menu where id between 100 and 137;

-- ========== 设置序列值（PostgreSQL） ==========
-- 确保下次插入菜单时ID不会冲突
select setval(pg_get_serial_sequence('sys_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_menu;
select setval(pg_get_serial_sequence('sys_role_menu', 'id'), coalesce(max(id), 0) + 1, true) from sys_role_menu;

-- ========== 菜单说明 ==========
-- 菜单ID范围: 100-137 (彩票模块专用)
-- 
-- 菜单树结构:
-- 100. 彩票管理 (一级目录)
--   ├── 101. 数据总览
--   ├── 102. 彩种管理
--   │     ├── 103. 新增
--   │     ├── 104. 修改
--   │     ├── 105. 删除
--   │     └── 106. 查看
--   ├── 107. 开奖数据
--   │     ├── 108. 查看
--   │     ├── 109. 同步数据
--   │     ├── 110. 全量同步
--   │     └── 111. 删除
--   ├── 112. 分析方法
--   │     ├── 113. 查看
--   │     ├── 114. 新增
--   │     ├── 115. 修改
--   │     └── 116. 删除
--   ├── 117. 组合管理
--   │     ├── 118. 新增
--   │     ├── 119. 修改
--   │     ├── 120. 删除
--   │     ├── 121. 查看
--   │     └── 122. 启用自动预测
--   ├── 123. 预测管理
--   │     ├── 124. 创建预测
--   │     ├── 125. 查看分析
--   │     ├── 126. 验证结果
--   │     ├── 127. 删除
--   │     └── 128. 导出
--   ├── 129. 会员管理
--   │     ├── 130. 新增套餐
--   │     ├── 131. 修改套餐
--   │     ├── 132. 删除套餐
--   │     ├── 133. 查看用户
--   │     └── 134. 激活会员
--   └── 135. 统计报表
--         ├── 136. 查看统计
--         └── 137. 导出报表

