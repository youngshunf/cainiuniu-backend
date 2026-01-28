---
name: creator-flow-dev
description: CreatorFlow 云端项目开发工作流指南。当用户需要开发新功能模块、创建数据库表、生成 CRUD 代码时使用此技能。
metadata:
  author: CreatorFlow Team
  version: "1.0"
  short-description: CreatorFlow 全栈开发工作流
---

# CreatorFlow 开发工作流

本技能指导 Agent 在 CreatorFlow 云端项目中进行规范化开发。

## 项目结构

```
creator-flow/
├── clound-backend/      # FastAPI 后端
│   ├── backend/
│   │   ├── app/         # 业务模块
│   │   ├── plugin/      # 插件（含代码生成器）
│   │   └── sql/generated/  # 生成的 SQL 文件
│   └── pyproject.toml
└── clound-frontend/     # Vue3 前端 (Vben Admin)
    └── apps/web-antd/src/
        ├── api/         # API 接口
        └── views/       # 页面组件
```

## 开发工作流程

### 第一步：设计数据库表

在 `clound-backend/backend/sql/tables/` 创建 SQL 文件。

#### 数据库表设计规范

**表结构模板（PostgreSQL）：**

```sql
-- 表注释（放在最前面）
CREATE TABLE "public"."user_subscription" (
  -- 主键：必须使用 bigserial
  "id" bigserial PRIMARY KEY,
  
  -- 外键字段：使用 int8，以 _id 结尾
  "user_id" int8 NOT NULL,
  
  -- 字符串字段：使用 varchar，指定长度
  "tier" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'free',
  "status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'active',
  
  -- 数值字段：金额/积分使用 numeric(15, 2)
  "monthly_credits" numeric(15, 2) NOT NULL DEFAULT 0,
  "current_credits" numeric(15, 2) NOT NULL DEFAULT 0,
  
  -- 布尔字段：以 is_/has_/auto_ 开头，类型 bool
  "auto_renew" bool NOT NULL DEFAULT true,
  
  -- JSON 字段：使用 jsonb，避免使用保留字 metadata
  "features" jsonb NOT NULL DEFAULT '{}',
  "extra_data" jsonb,  -- 不要用 metadata
  
  -- 时间字段：使用 timestamptz(6)，必须同时有 created_time 和 updated_time
  "billing_cycle_start" timestamptz(6) NOT NULL,
  "billing_cycle_end" timestamptz(6) NOT NULL,
  "created_time" timestamptz(6) NOT NULL DEFAULT NOW(),
  "updated_time" timestamptz(6)  -- 可为 NULL，更新时自动填充
);
```

**字段类型规范：**

| 场景 | PostgreSQL 类型 | 说明 |
|------|----------------|------|
| 主键 | `bigserial` | 自增大整数 |
| 外键 | `int8` | 64位整数 |
| 短字符串 | `varchar(N)` | N 根据实际需要设置 |
| 长文本 | `text` | 无限制长度 |
| 金额/积分 | `numeric(15,2)` | 精确小数 |
| 布尔 | `bool` | true/false |
| JSON | `jsonb` | 二进制 JSON |
| 时间戳 | `timestamptz(6)` | 带时区 |
| 整数 | `int4` | 普通整数 |

**保留字/禁止使用的字段名：**

| 禁止使用 | 替代方案 | 原因 |
|----------|----------|------|
| `metadata` | `extra_data` | SQLAlchemy ORM 保留字 |
| `registry` | `registry_data` | SQLAlchemy ORM 保留字 |
| `query` | `query_data` | SQLAlchemy ORM 保留字 |

**必须包含的字段：**

每个表必须包含以下字段（代码生成器依赖 Base 模型的 DateTimeMixin）：

```sql
"created_time" timestamptz(6) NOT NULL DEFAULT NOW(),
"updated_time" timestamptz(6)
```

**注释规范（重要）：**

```sql
-- 表注释：会作为菜单标题和文档说明
COMMENT ON TABLE "public"."user_subscription" IS '用户订阅表';

-- 列注释：会作为前端字段标签
-- 格式 1：简单标签
COMMENT ON COLUMN "public"."user_subscription"."user_id" IS '用户 ID';

-- 格式 2：标签 + 字典枚举值（自动生成字典 SQL）
COMMENT ON COLUMN "public"."user_subscription"."status" IS '订阅状态 (active:激活/expired:已过期/cancelled:已取消)';

-- 格式 3：标签 + 字典枚举值 + 颜色
COMMENT ON COLUMN "public"."user_subscription"."tier" IS '订阅等级 (free:免费版:blue/basic:基础版:green/pro:专业版:orange/enterprise:企业版:purple)';
```

### 字典字段命名规范

以下字段名会被自动识别为字典字段，并生成对应的字典 SQL：

- `status` / `*_status` - 状态字典
- `state` / `*_state` - 状态字典  
- `type` / `*_type` - 类型字典
- `category` - 分类字典
- `level` / `*_level` - 等级字典
- `tier` / `*_tier` - 层级字典

生成的字典代码格式为：`{app}_{field_name}`，如 `user_tier_status`

### 字典枚举值格式说明

在字段注释中定义枚举值，代码生成器会自动解析并生成字典 SQL：

```
格式：标签 (value1:显示名1/value2:显示名2/...)
带颜色：标签 (value1:显示名1:颜色/value2:显示名2:颜色/...)
```

**参数说明：**
- `value` - 存储在数据库中的值（英文/数字）
- `显示名` - 前端显示的中文标签
- `颜色` - 可选，支持：blue/green/orange/red/purple/cyan/pink/yellow

**支持的括号：**
- 英文括号 `( )`
- 中文括号 `（ ）`

### 第二步：导入表到代码生成器

```bash
cd clound-backend

# 将表结构导入到 gen_business/gen_column 表
uv run fba codegen import --table user_subscription --app llm
```

### 第三步：一键生成代码

```bash
# 生成完整代码（前端 + 后端 + 菜单SQL + 字典SQL）
uv run fba codegen generate --table user_subscription --app llm

# 强制覆盖已有文件
uv run fba codegen generate --table user_subscription --app llm --force
```

生成的文件包括：

**后端（已有则跳过）：**
- `backend/app/{app}/model/{table}.py` - SQLAlchemy 模型
- `backend/app/{app}/schema/{table}.py` - Pydantic Schema
- `backend/app/{app}/crud/crud_{table}.py` - CRUD 操作
- `backend/app/{app}/service/{table}_service.py` - 业务服务
- `backend/app/{app}/api/v1/{table}.py` - API 路由

**前端：**
- `apps/web-antd/src/views/{app}/{table}/index.vue` - 页面组件
- `apps/web-antd/src/views/{app}/{table}/data.ts` - 表格/表单配置
- `apps/web-antd/src/api/{app}/{table}.ts` - API 接口

**SQL：**
- `backend/sql/generated/{table}_menu.sql` - 菜单初始化
- `backend/sql/generated/{table}_dict.sql` - 字典初始化

### 第四步：执行生成的 SQL

```bash
# 菜单 SQL（自动执行或手动）
uv run fba --sql backend/sql/generated/user_subscription_menu.sql

# 字典 SQL
uv run fba --sql backend/sql/generated/user_subscription_dict.sql
```

**注意**：菜单和字典 SQL 都是幂等的，可以重复执行。

### 第五步：注册路由（如果是新模块）

编辑 `backend/app/{app}/api/router.py`：

```python
from backend.app.{app}.api.v1.{table} import router as {table}_router

v1.include_router({table}_router, prefix='/{table/path}s')
```

路由路径规范：`user_subscription` → `/user/subscriptions`（下划线转斜杠，复数）

### 第六步：业务开发

基础 CRUD 已生成，现在可以：

1. **扩展后端服务** - 在 `service/{table}_service.py` 添加业务逻辑
2. **扩展前端页面** - 在 `views/{app}/{table}/` 添加自定义功能
3. **添加权限控制** - 使用生成的权限标识 `{table}:add/edit/del/get`

## 前端字典使用

生成的代码会自动使用字典组件：

```typescript
// data.ts 中的字典字段会自动使用 getDictOptions
import { getDictOptions } from '#/utils/dict';

// 查询表单
{
  component: 'Select',
  fieldName: 'status',
  label: '状态',
  componentProps: {
    options: getDictOptions('llm_status'),
  },
}

// 表格列
{
  field: 'status',
  title: '状态',
  cellRender: {
    name: 'CellTag',
    options: getDictOptions('llm_status'),
  },
}
```

## 常用命令速查

```bash
# 代码生成
uv run fba codegen generate --table TABLE --app APP [--force]

# 导入表
uv run fba codegen import --table TABLE --app APP

# 执行 SQL
uv run fba --sql path/to/file.sql

# 启动后端
uv run fba run

# 启动前端
cd ../clound-frontend && pnpm dev
```

## 注意事项

1. **字段注释很重要** - 会影响前端显示的标签
2. **遵循命名规范** - 字典字段命名会触发自动字典生成
3. **先导入再生成** - 确保表已导入到 gen_business
4. **SQL 幂等** - 菜单/字典 SQL 可重复执行
5. **路由注册** - 新模块需要手动注册路由
