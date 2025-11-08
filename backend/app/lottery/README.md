# 彩票分析预测系统 - 后端模块

## 项目概述

基于 FastAPI Best Architecture 开发的完整彩票分析预测系统后端，支持8种主流彩票的数据同步、分析和预测。

## 支持的彩种

- 双色球 (ssq)
- 大乐透 (dlt)
- 福彩3D (3d)
- 排列三 (pls)
- 排列五 (plw)
- 七乐彩 (qlc)
- 快乐8 (kl8)
- 七星彩 (qxc)

## 核心功能

### 1. 数据同步模块

- **自动同步**: 每天21:30自动同步最新开奖数据
- **手动同步**: 支持通过API手动触发同步
- **多数据源**: 
  - 体彩官方API
  - 福彩官方API
  - 网页备用方案
- **数据验证**: 自动验证数据完整性
- **期号计算**: 自动计算下期期号

### 2. 分析算法（19种传统方法）

#### 基础分析 (5种)
1. **频率分析**: 统计号码出现频次和概率
2. **冷热号分析**: 识别近期热门和冷门号码
3. **大小号分布**: 分析大小号码的平衡性
4. **和值分析**: 计算号码和值的分布规律
5. **间隔分析**: 研究号码间距的统计特征

#### 高级分析 (14种)
6. **奇偶分析**: 统计奇偶号码的分布
7. **质合分析**: 质数和合数的出现规律
8. **012路分析**: 除3余数分类分析
9. **AC值分析**: 算术复杂性指标
10. **跨度分析**: 最大号码与最小号码的差值
11. **连号分析**: 连续号码的出现频率
12. **重号分析**: 上期号码重复出现的规律
13. **邻号分析**: 相邻号码的关联性
14. **同尾号分析**: 相同尾数号码的分布
15. **区间分析**: 号码池分区间分布
16. **遗漏值分析**: 号码遗漏期数统计
17. **尾数和值分析**: 号码尾数和值分布
18. **号码和分布**: 两两号码之和分布
19. **三分区分析**: 前中后三区出号规律

### 3. 机器学习模型（可选）

- **LSTM**: 时间序列预测
- **聚类分析**: K-means/DBSCAN模式识别
- **关联规则**: Apriori算法
- 更多模型可扩展...

### 4. 组合分析引擎

- **多方法组合**: 支持任意组合19种分析方法
- **权重配置**: 每个方法可设置权重
- **智能推荐**: 自动选择最优号码组合
- **文章生成**: 自动生成分析文章
- **格式化输出**: 根据彩种生成不同格式号码

### 5. 预测系统

- **自定义预测**: 用户可自由配置分析方法和参数
- **组合管理**: 保存和复用分析组合
- **历史验证**: 自动验证预测结果
- **准确率统计**: 记录并计算组合准确率
- **定时推荐**: 每日自动推荐下期号码

### 6. 会员体系

#### 套餐等级
- **免费版**: 
  - 基础分析方法（5种）
  - 每日5次预测
  - 查看30天历史数据
  
- **专业版** (¥99/月):
  - 全部传统分析方法（19种）
  - 每日50次预测
  - 自定义10个组合
  - 查看365天历史数据
  - 数据导出
  
- **旗舰版** (¥299/月):
  - 包含专业版所有功能
  - 机器学习方法
  - 统计学方法
  - 组合优化算法
  - 每日1000次预测
  - 无限自定义组合
  - API调用（1000次/天）
  - 自动预测推荐

- **企业版** (¥999/月):
  - 包含旗舰版所有功能
  - 无限预测次数
  - API调用（10000次/天）
  - 白标支持
  - 自定义算法
  - 优先技术支持

#### 权限控制
- 预测次数限制
- 方法使用权限
- API调用配额
- 每日配额自动重置

## API接口文档

### 彩种管理
```
GET  /api/v1/lottery/lottery-type/list      # 获取彩种列表
GET  /api/v1/lottery/lottery-type/{id}      # 获取彩种详情
```

### 开奖数据
```
GET  /api/v1/lottery/draw/list              # 获取开奖列表
GET  /api/v1/lottery/draw/{code}/{period}   # 获取单期开奖
GET  /api/v1/lottery/draw/{code}/latest     # 获取最新开奖
GET  /api/v1/lottery/draw/{code}/history    # 获取历史开奖
POST /api/v1/lottery/draw/sync/{code}       # 手动同步数据
POST /api/v1/lottery/draw/sync/{code}/history  # 全量同步历史
GET  /api/v1/lottery/draw/{code}/next-period   # 获取下期期号
```

### 分析方法
```
GET  /api/v1/lottery/analysis/methods       # 获取分析方法列表
POST /api/v1/lottery/analysis/analyze       # 单个方法分析
```

### 预测管理
```
POST /api/v1/lottery/prediction/create      # 创建预测
POST /api/v1/lottery/prediction/{id}/verify # 验证预测结果
```

### 组合管理
```
GET  /api/v1/lottery/combination/list       # 获取组合列表
POST /api/v1/lottery/combination/create     # 创建组合
PUT  /api/v1/lottery/combination/{id}       # 更新组合
DELETE /api/v1/lottery/combination/{id}     # 删除组合
```

## 数据库表结构

### 核心表
- `lottery_type`: 彩票类型表
- `draw_result`: 开奖结果表
- `analysis_method`: 分析方法表
- `analysis_combination`: 分析组合表
- `prediction_result`: 预测结果表
- `membership_plan`: 会员套餐表
- `user_membership`: 用户会员表
- `api_usage`: API使用记录表

## 定时任务

### Celery Beat 调度
```python
# 每日21:30同步最新开奖数据
'每日同步最新开奖': {
    'task': 'lottery.sync_latest_draw',
    'schedule': TzAwareCrontab('30', '21'),
}

# 每日00:00重置会员配额（待添加）
# 每日22:00验证预测结果（待添加）
# 每周日02:00重训练ML模型（待添加）
```

## 安装与配置

### 1. 安装依赖

基础依赖（必需）:
```bash
cd cainiuniu-backend
uv sync
```

机器学习依赖（可选）:
```bash
uv pip install tensorflow>=2.15.0 scikit-learn>=1.4.0
```

### 2. 配置环境变量

编辑 `backend/.env`:
```ini
# 数据库配置
DATABASE_TYPE=postgresql
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_SCHEMA=lottery_db

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_DATABASE=0

# Celery配置
CELERY_BROKER=redis
CELERY_BROKER_REDIS_DATABASE=1
```

### 3. 初始化数据库

```bash
# 生成迁移脚本
cd backend
uv run alembic revision --autogenerate -m "init_lottery_tables"

# 执行迁移
uv run alembic upgrade head

# 初始化彩票类型数据
psql -U postgres -d lottery_db -f app/lottery/sql/init_lottery_types.sql

# 初始化分析方法数据
psql -U postgres -d lottery_db -f app/lottery/sql/init_analysis_methods.sql

# 初始化会员套餐数据
psql -U postgres -d lottery_db -f app/lottery/sql/init_membership_plans.sql
```

### 4. 启动服务

```bash
# 启动FastAPI服务
uv run python backend/run.py

# 启动Celery Worker
uv run celery -A backend.app.task.celery worker --loglevel=info -P gevent

# 启动Celery Beat
uv run celery -A backend.app.task.celery beat --loglevel=info
```

### 5. 首次同步数据

```bash
# 使用API同步（推荐）
curl -X POST "http://localhost:8000/api/v1/lottery/draw/sync/ssq/history"

# 或使用Celery任务
uv run celery -A backend.app.task.celery call lottery.sync_all_history --args='["ssq"]'
```

## 开发指南

### 添加新的分析方法

1. 在 `algorithm/traditional/` 创建新文件
2. 继承 `BaseAnalyzer` 类
3. 实现 `analyze()` 和 `predict()` 方法
4. 在 `combiner.py` 中注册

示例:
```python
from backend.app.lottery.algorithm.base_analyzer import BaseAnalyzer

class MyAnalyzer(BaseAnalyzer):
    async def analyze(self, history_data: list, params: dict | None = None) -> dict:
        # 实现分析逻辑
        return {'analysis_result': ...}
    
    async def predict(self, analysis_result: dict, params: dict | None = None) -> list:
        # 实现预测逻辑
        return {'red_balls': [...], 'blue_balls': [...]}
```

### 扩展机器学习模型

1. 在 `algorithm/machine_learning/` 创建新文件
2. 继承 `BaseMLAnalyzer` 类
3. 实现训练、预测、保存、加载方法
4. 在 `combiner.py` 中注册（可选依赖）

## 性能优化

### Redis缓存
- 彩票类型信息缓存
- 最新开奖结果缓存
- 分析方法元数据缓存
- 用户会员信息缓存

### 数据库索引
- `draw_result` 表: (lottery_code, period) 唯一索引
- `draw_result` 表: draw_date 索引
- `prediction_result` 表: (lottery_code, target_period) 索引

### 异步处理
- 所有数据库操作使用异步
- 历史数据同步使用Celery后台任务
- 复杂分析计算可异步执行

## 常见问题

### Q: 如何添加新的彩种？
A: 在数据库中添加 `lottery_type` 记录，配置API地址和号码规则即可。

### Q: 机器学习模型如何训练？
A: 首次使用时自动训练，或通过API手动触发训练任务。

### Q: 如何提高预测准确率？
A: 
1. 增加历史数据量
2. 组合多种分析方法
3. 调整方法权重
4. 定期回测验证

### Q: 数据同步失败怎么办？
A: 系统会自动尝试网页备用方案，如仍失败请检查网络和API地址。

## 技术栈

- **框架**: FastAPI 0.120+
- **数据库**: PostgreSQL 16+ / MySQL 8+
- **缓存**: Redis 7+
- **任务队列**: Celery + RabbitMQ/Redis
- **ORM**: SQLAlchemy 2.0
- **数据验证**: Pydantic V2
- **异步**: asyncio + aiohttp
- **机器学习**: TensorFlow 2.15+ (可选)
- **数据分析**: scikit-learn, pandas, numpy

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- 项目地址: https://github.com/your-repo/lottery-analysis
- 文档地址: https://docs.your-domain.com

---

**注意**: 本系统仅供技术研究和学习使用，预测结果仅供参考。彩票具有随机性，请理性投注。

