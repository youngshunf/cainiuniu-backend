# 彩票系统API路由文档

## 基础路径

所有彩票API的基础路径为：`/api/v1/lottery`

---

## 🎯 彩种管理 (`/lottery-type`)

### 列表查询
```
GET /api/v1/lottery/lottery-type/list
```
**查询参数:**
- `category`: string (可选) - 类别（福彩/体彩）
- `status`: int (可选) - 状态（0停用/1启用）
- `page`: int (可选) - 页码，默认1
- `size`: int (可选) - 每页数量，默认20

**响应示例:**
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "total": 8,
    "items": [
      {
        "id": 1,
        "code": "ssq",
        "name": "双色球",
        "category": "福彩",
        "red_ball_count": 6,
        "blue_ball_count": 1,
        "status": 1
      }
    ]
  }
}
```

### 获取详情
```
GET /api/v1/lottery/lottery-type/{pk}
```

### 创建彩种
```
POST /api/v1/lottery/lottery-type/create
```

### 更新彩种
```
PUT /api/v1/lottery/lottery-type/{pk}
```

### 删除彩种
```
DELETE /api/v1/lottery/lottery-type/{pk}
```

---

## 📅 开奖数据 (`/draw`)

### 列表查询
```
GET /api/v1/lottery/draw/list
```
**查询参数:**
- `lottery_code`: string (可选) - 彩种代码
- `period`: string (可选) - 期号
- `start_date`: string (可选) - 开始日期 (YYYY-MM-DD)
- `end_date`: string (可选) - 结束日期 (YYYY-MM-DD)
- `page`: int (可选) - 页码
- `size`: int (可选) - 每页数量

### 获取单期开奖
```
GET /api/v1/lottery/draw/{lottery_code}/{period}
```

### 获取最新开奖
```
GET /api/v1/lottery/draw/{lottery_code}/latest
```

### 获取历史开奖
```
GET /api/v1/lottery/draw/{lottery_code}/history?limit=100
```

### 获取下期期号
```
GET /api/v1/lottery/draw/{lottery_code}/next-period
```

### 手动同步数据
```
POST /api/v1/lottery/draw/sync/{lottery_code}?page_size=30
```

### 全量同步历史
```
POST /api/v1/lottery/draw/sync/{lottery_code}/history
```

---

## 🧠 分析方法 (`/analysis`)

### 获取方法列表
```
GET /api/v1/lottery/analysis/methods
```

### 单个方法分析
```
POST /api/v1/lottery/analysis/analyze
```
**查询参数:**
- `lottery_code`: string (必需) - 彩种代码
- `method_code`: string (必需) - 方法代码
- `history_periods`: int (可选) - 历史期数，默认100

**请求体:**
```json
{
  "is_red_ball": true,
  "top_n": 10
}
```

---

## 📦 组合管理 (`/combination`)

### 列表查询
```
GET /api/v1/lottery/combination/list
```
**查询参数:**
- `lottery_code`: string (可选) - 彩种代码
- `is_auto`: boolean (可选) - 是否自动预测
- `page`: int (可选) - 页码
- `size`: int (可选) - 每页数量

### 获取详情
```
GET /api/v1/lottery/combination/{pk}
```

### 创建组合
```
POST /api/v1/lottery/combination/create
```
**请求体:**
```json
{
  "name": "双色球智能组合1",
  "lottery_code": "ssq",
  "method_configs": "[{\"code\":\"frequency\",\"weight\":0.3},{\"code\":\"hot_cold\",\"weight\":0.3}]",
  "history_periods": 100,
  "is_auto": true
}
```

### 更新组合
```
PUT /api/v1/lottery/combination/{pk}
```

### 删除组合
```
DELETE /api/v1/lottery/combination/{pk}
```

---

## ✨ 预测管理 (`/prediction`)

### 列表查询
```
GET /api/v1/lottery/prediction/list
```
**查询参数:**
- `lottery_code`: string (可选) - 彩种代码
- `is_verified`: boolean (可选) - 是否已验证
- `page`: int (可选) - 页码
- `size`: int (可选) - 每页数量

### 获取详情
```
GET /api/v1/lottery/prediction/{pk}
```

### 创建预测
```
POST /api/v1/lottery/prediction/create
```
**查询参数:**
- `lottery_code`: string (必需) - 彩种代码
- `combination_id`: int (可选) - 组合ID
- `history_periods`: int (可选) - 历史期数，默认100

**响应示例:**
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "success": true,
    "lottery_code": "ssq",
    "target_period": "2025002",
    "predicted_numbers": {...},
    "analysis_article": "# 分析文章...",
    "confidence": 0.75
  }
}
```

### 验证预测结果
```
POST /api/v1/lottery/prediction/{prediction_id}/verify
```

---

## 👑 会员管理 (`/membership`)

### 获取套餐列表
```
GET /api/v1/lottery/membership/plans
```

### 获取用户会员信息
```
GET /api/v1/lottery/membership/user/{user_id}
```

### 激活会员
```
POST /api/v1/lottery/membership/activate
```
**请求体:**
```json
{
  "user_id": 1,
  "plan_id": 2,
  "auto_renew": false
}
```

---

## 🔐 认证接口 (`/auth`)

### 登录
```
POST /api/v1/auth/login
```
**请求体:**
```json
{
  "username": "admin",
  "password": "123456",
  "captcha": "1234"
}
```

### 登出
```
POST /api/v1/auth/logout
```

### 刷新Token
```
POST /api/v1/auth/refresh
```

---

## 📝 通用响应格式

### 成功响应
```json
{
  "code": 200,
  "msg": "Success",
  "data": {...}
}
```

### 失败响应
```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

### 分页响应
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "total": 100,
    "items": [...],
    "page": 1,
    "size": 20
  }
}
```

---

## 🔑 请求Headers

### 必需Headers
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

### 可选Headers
```
Accept-Language: zh-CN
X-Request-ID: {request_id}
```

---

## 📊 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（需要登录） |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 422 | 数据验证失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器错误 |

---

## 🚀 使用示例

### 获取彩种列表
```bash
curl -X GET "http://localhost:8000/api/v1/lottery/lottery-type/list?page=1&size=20" \
  -H "Authorization: Bearer {token}"
```

### 同步开奖数据
```bash
curl -X POST "http://localhost:8000/api/v1/lottery/draw/sync/ssq?page_size=30" \
  -H "Authorization: Bearer {token}"
```

### 创建预测
```bash
curl -X POST "http://localhost:8000/api/v1/lottery/prediction/create?lottery_code=ssq&history_periods=100" \
  -H "Authorization: Bearer {token}"
```

### 验证预测
```bash
curl -X POST "http://localhost:8000/api/v1/lottery/prediction/1/verify" \
  -H "Authorization: Bearer {token}"
```

---

## 🔧 前端调用示例（TypeScript）

```typescript
import { lotteryApi } from '@/lib/api';

// 获取彩种列表
const lotteries = await lotteryApi.getLotteryTypes();

// 获取开奖数据
const draws = await lotteryApi.getDrawResults({
  lottery_code: 'ssq',
  page: 1,
  size: 20
});

// 创建预测
const prediction = await lotteryApi.createPrediction({
  lottery_code: 'ssq',
  history_periods: 100
});
```

---

## ⚠️ 注意事项

1. **所有接口都需要JWT认证**（除了登录接口）
2. **分页参数**：page从1开始，size默认20，最大100
3. **日期格式**：YYYY-MM-DD
4. **时间格式**：YYYY-MM-DD HH:MM:SS
5. **布尔值**：true/false（小写）
6. **JSON字符串字段**：需要手动parse（如red_balls, method_configs等）

---

## 📖 更多信息

- 完整API文档：http://localhost:8000/docs
- ReDoc文档：http://localhost:8000/redoc
- OpenAPI JSON：http://localhost:8000/openapi.json

