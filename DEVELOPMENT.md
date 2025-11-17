# Image Tools API 开发指南

## 项目概述

Image Tools API 是一个基于 FastAPI 和 React 的完整图片处理服务，提供从基础图片操作到高级艺术效果的一站式解决方案。

## 技术栈

### 后端
- **FastAPI**: 高性能的 Python Web 框架
- **Pillow**: 图片处理库
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI 服务器
- **httpx**: HTTP 客户端（用于外部服务调用）

### 前端
- **React**: 用户界面库
- **TypeScript**: 类型安全的 JavaScript
- **Ant Design**: UI 组件库
- **Axios**: HTTP 客户端

### 基础设施
- **Docker**: 容器化部署
- **Docker Compose**: 多容器编排
- **Nginx**: 前端服务器

## 项目结构详解

```
image-tools-api/
├── app/                          # 后端应用
│   ├── main.py                  # FastAPI 主应用
│   ├── middleware/              # 中间件
│   │   ├── __init__.py
│   │   ├── auth_middleware.py   # 认证中间件
│   │   └── cors_middleware.py   # CORS 中间件
│   ├── routers/                 # API 路由
│   │   ├── __init__.py
│   │   ├── health.py           # 健康检查
│   │   ├── resize.py           # 图片缩放
│   │   └── watermark.py        # 水印功能
│   ├── schemas/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── common.py           # 通用响应模型
│   │   ├── resize.py           # 缩放相关模型
│   │   └── watermark.py        # 水印相关模型
│   ├── services/                # 业务服务
│   │   ├── __init__.py
│   │   ├── auth_service.py     # 认证服务
│   │   ├── billing_service.py  # 计费服务
│   │   ├── file_upload_service.py # 文件上传服务
│   │   ├── image_service.py    # 图片处理服务
│   │   └── user_service.py     # 用户服务
│   └── utils/                   # 工具函数
│       ├── __init__.py
│       ├── config.py           # 配置管理
│       └── logger.py           # 日志工具
├── frontend/                    # 前端应用
│   ├── public/                 # 静态文件
│   ├── src/                    # 源代码
│   │   ├── components/         # 组件
│   │   ├── pages/             # 页面
│   │   ├── services/          # 服务层
│   │   └── utils/             # 工具函数
│   ├── package.json           # 依赖配置
│   └── tsconfig.json          # TypeScript 配置
├── scripts/                     # 项目脚本
│   ├── start.sh               # 启动脚本
│   ├── stop.sh                # 停止脚本
│   ├── status.sh              # 状态检查脚本
│   ├── test_api.sh            # API 测试脚本
│   └── clean.sh               # 清理脚本
├── docker-compose.yml          # Docker 编排配置
├── backend.Dockerfile          # 后端 Docker 配置
├── frontend.Dockerfile         # 前端 Docker 配置
├── requirements.txt            # Python 依赖
├── README.md                   # 项目说明
└── DEVELOPMENT.md              # 开发指南
```

## 快速开始

### 1. 环境准备

确保系统安装了以下软件：
- Docker Desktop
- Git

### 2. 克隆项目

```bash
git clone <repository-url>
cd image-tools-api
```

### 3. 启动服务

```bash
# 一键启动（推荐）
./start.sh

# 或手动启动
docker-compose up -d --build
```

### 4. 验证服务

```bash
# 检查服务状态
./status.sh

# 测试 API 功能
./test_api.sh
```

## 开发模式

### 环境变量配置

在开发模式下，系统会使用以下配置：

```bash
# 环境模式
ENVIRONMENT=development
DEVELOPMENT_MODE=true

# 用户中心配置（开发模式下会使用模拟认证）
USER_CENTER_BASE_URL=https://usersystem.aigchub.vip
USER_CENTER_INTERNAL_TOKEN=aigc-hub-big-business

# AIGC 网盘配置（开发模式下会返回模拟响应）
AIGC_STORAGE_BASE_URL=https://aigc-network-disk.aigchub.vip
AIGC_STORAGE_DEFAULT_CATEGORY_ID=1
AIGC_STORAGE_DEFAULT_TAGS=图片处理,AI工具
```

### 开发模式特性

1. **认证系统**: 任何以 `aigc-hub-` 开头的 token 都会通过认证
2. **文件上传**: 返回模拟的上传响应，不实际上传到网盘
3. **日志**: 详细的调试日志输出
4. **CORS**: 允许跨域请求

## API 开发

### 添加新的 API 端点

1. **创建数据模型** (`app/schemas/`)
```python
# app/schemas/new_feature.py
from pydantic import BaseModel
from typing import Optional

class NewFeatureRequest(BaseModel):
    param1: str
    param2: Optional[int] = None

class NewFeatureResponse(BaseModel):
    result: str
    processed_at: str
```

2. **实现业务逻辑** (`app/services/`)
```python
# app/services/new_feature_service.py
from app.schemas.new_feature import NewFeatureRequest, NewFeatureResponse
from datetime import datetime

class NewFeatureService:
    @staticmethod
    def process(request: NewFeatureRequest) -> NewFeatureResponse:
        # 实现业务逻辑
        result = f"Processed: {request.param1}"
        return NewFeatureResponse(
            result=result,
            processed_at=datetime.now().isoformat()
        )
```

3. **创建 API 路由** (`app/routers/`)
```python
# app/routers/new_feature.py
from fastapi import APIRouter, Depends
from app.schemas.new_feature import NewFeatureRequest, NewFeatureResponse
from app.services.new_feature_service import NewFeatureService
from app.middleware.auth_middleware import verify_token

router = APIRouter(prefix="/api/v1", tags=["new-feature"])

@router.post("/new-feature", response_model=NewFeatureResponse)
async def process_new_feature(
    request: NewFeatureRequest,
    user_info: dict = Depends(verify_token)
):
    return NewFeatureService.process(request)
```

4. **注册路由** (`app/main.py`)
```python
from app.routers import new_feature

app.include_router(new_feature.router)
```

## 前端开发

### 组件开发规范

1. **使用 TypeScript**: 所有组件必须使用 TypeScript
2. **组件命名**: 使用 PascalCase
3. **文件结构**: 每个功能模块一个文件夹
4. **样式管理**: 使用 Ant Design 的主题系统

### API 调用

```typescript
// src/services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:58888';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`,
  },
});

export const newFeatureApi = {
  process: (data: NewFeatureRequest) => 
    apiClient.post<NewFeatureResponse>('/api/v1/new-feature', data),
};
```

## 测试

### 后端测试

```bash
# 运行 API 测试
./test_api.sh

# 手动测试单个端点
curl -X POST "http://localhost:58888/api/v1/resize" \
  -H "Authorization: Bearer aigc-hub-test-token" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg" \
  -F "width=800" \
  -F "height=600"
```

### 前端测试

```bash
# 进入前端目录
cd frontend

# 运行测试
npm test

# 构建生产版本
npm run build
```

## 部署

### 生产环境部署

1. **环境变量配置**
```bash
# .env.production
ENVIRONMENT=production
DEVELOPMENT_MODE=false
USER_CENTER_BASE_URL=https://usersystem.aigchub.vip
USER_CENTER_INTERNAL_TOKEN=your-production-token
AIGC_STORAGE_BASE_URL=https://aigc-network-disk.aigchub.vip
```

2. **构建和启动**
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### 监控和日志

```bash
# 查看服务状态
./status.sh

# 查看实时日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 查看特定时间段的日志
docker-compose logs --since="2h" backend
```

## 故障排除

### 常见问题

1. **端口占用**
```bash
# 清理端口占用
./clean.sh
```

2. **Docker 镜像问题**
```bash
# 重新构建镜像
docker-compose build --no-cache
```

3. **权限问题**
```bash
# 给脚本添加执行权限
chmod +x *.sh
```

### 调试模式

```bash
# 进入后端容器调试
docker-compose exec backend bash

# 查看详细日志
docker-compose logs -f --tail=100 backend
```

## 性能优化

### 后端优化

1. **图片处理**: 使用适当的图片质量和压缩
2. **缓存**: 实现响应缓存机制
3. **异步处理**: 对于大图片使用后台任务

### 前端优化

1. **代码分割**: 使用 React.lazy 进行组件懒加载
2. **图片优化**: 实现图片预加载和压缩
3. **缓存策略**: 合理使用浏览器缓存

## 贡献指南

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -am 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 提交 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件 