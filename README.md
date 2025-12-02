# Image Tools API

一个基于FastAPI和React的图片处理工具API，提供多种图片处理功能，包括缩放、水印、滤镜等。

## 功能特性

- 🖼️ **图片缩放**: 支持多种重采样算法的图片大小调整
- 🏷️ **文字水印**: 为图片添加自定义文字水印
- 🎨 **图片滤镜**: 多种艺术滤镜效果
- 🔄 **格式转换**: 支持多种图片格式转换
- 🔐 **用户认证**: 集成用户中心的认证系统
- 💰 **计费系统**: 基于Token的使用计费
- 📤 **文件上传**: 自动上传处理结果到网盘

## 快速开始

### 1. 环境要求

- Python 3.11+
- Node.js 18+
- npm 或 yarn

### 2. 本地开发启动

```bash
# 克隆项目
git clone <repository-url>
cd image-tools-api

# 一键启动（自动安装依赖并启动服务）
./start.sh

# 查看服务状态
./status.sh

# 停止服务
./stop.sh
```

### 3. Docker部署（可选）

```bash
# 使用Docker Compose启动
docker-compose up -d

# 查看Docker服务状态
docker-compose ps
```

### 4. 访问服务

- **前端界面**: http://localhost:58889
- **后端API**: http://localhost:58888
- **API文档**: http://localhost:58888/docs
- **健康检查**: http://localhost:58888/api/health

### 5. 开发工具脚本

| 脚本 | 功能 | 说明 |
|------|------|------|
| `./start.sh` | 启动服务 | 自动安装依赖并启动前后端服务 |
| `./stop.sh` | 停止服务 | 优雅停止所有服务进程 |
| `./status.sh` | 查看状态 | 检查服务运行状态和端口占用 |
| `./clean.sh` | 清理环境 | 清理进程、临时文件和缓存 |

### 6. 测试API

运行测试脚本验证API功能：

```bash
./test_api.sh
```

## API使用示例

### 图片缩放

```bash
curl -X POST "http://localhost:58888/api/v1/resize" \
  -H "Authorization: Bearer aigc-hub-your-token" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-image.jpg" \
  -F "width=800" \
  -F "height=600" \
  -F "resample=LANCZOS"
```

### 文字水印

```bash
curl -X POST "http://localhost:58888/api/v1/watermark" \
  -H "Authorization: Bearer aigc-hub-your-token" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@your-image.jpg" \
  -F "watermark_text=Your Watermark" \
  -F "position=center" \
  -F "font_size=48" \
  -F "opacity=0.5"
```

## 环境模式

项目默认为**生产模式**，如需开发模式，请设置：

```bash
export DEVELOPMENT_MODE=true
```

**生产模式特性**：
- 真实的用户中心认证
- 实际文件上传到AIGC网盘
- 完整的计费系统集成
- 严格的错误处理

**开发模式特性**：
- 模拟的用户认证（以`aigc-hub-`开头的token即可）
- 文件上传返回模拟响应，不实际上传到网盘
- 详细的调试日志输出

## 环境配置

主要环境变量配置：

```bash
# 环境模式（生产环境）
ENVIRONMENT=production
DEVELOPMENT_MODE=false

# 用户中心配置
USER_CENTER_BASE_URL=https://usersystem.aigchub.vip
USER_CENTER_INTERNAL_TOKEN=aigc-hub-big-business

# AIGC网盘配置
AIGC_STORAGE_BASE_URL=https://aigc-network-disk.aigchub.vip
AIGC_STORAGE_DEFAULT_CATEGORY_ID=1
AIGC_STORAGE_DEFAULT_TAGS=图片处理,AI工具
```

## 项目结构

```
image-tools-api/
├── app/                    # 后端应用
│   ├── routers/           # API路由
│   ├── services/          # 业务服务
│   ├── middleware/        # 中间件
│   ├── schemas/           # 数据模型
│   └── utils/             # 工具函数
├── frontend/              # 前端应用
├── docker-compose.yml     # Docker编排配置
├── backend.Dockerfile     # 后端Docker配置
├── frontend.Dockerfile    # 前端Docker配置
└── test_api.sh           # API测试脚本
```

## 支持的功能

### 图片处理功能

- **缩放**: 调整图片尺寸，支持多种重采样算法
- **水印**: 文字水印和图片水印
- **滤镜**: 模糊、锐化、边缘检测等
- **艺术滤镜**: 油画、素描、卡通等艺术效果
- **裁剪**: 智能裁剪和自定义裁剪
- **变换**: 旋转、翻转、透视变换
- **增强**: 亮度、对比度、饱和度调整
- **格式转换**: JPEG、PNG、WebP等格式互转

### 高级功能

- **批量处理**: 支持多图片批量处理
- **GIF处理**: GIF动图编辑
- **文字转图片**: 文本渲染为图片
- **AI文字转图片**: AI生成图片功能
- **图片拼接**: 多图拼接合成

## 开发指南

### 添加新功能

1. 在`app/routers/`目录下创建新的路由文件
2. 在`app/services/`目录下实现业务逻辑
3. 在`app/main.py`中注册新路由
4. 更新API文档和测试用例

### 调试

#### 本地开发调试

```bash
# 查看服务状态
./status.sh

# 手动启动后端（开发模式）
cd backend
python3 start_backend.py

# 手动启动前端（开发模式）
cd frontend
BROWSER=none npm start

# 清理环境重新开始
./clean.sh
./start.sh
```

#### Docker调试（可选）

```bash
# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend

# 进入后端容器
docker-compose exec backend bash
```

## 生产环境部署

项目支持两套部署环境：

### 局域网 K8s 集群部署 ⭐（推荐）

部署到局域网 K8s 集群（192.168.3.42）：

```bash
# 一键部署到局域网集群
./deploy-local.sh
```

**特点**：
- 镜像仓库: 192.168.3.42:5000
- 使用 kubectl-local 命令
- 本地构建和推送，速度快
- 域名从云服务器路由过来

### 云服务器 K8s 集群部署

部署到云服务器 K8s 集群（8.130.35.126）：

```bash
# 部署到云服务器集群
./deploy-prod.sh
```

### 详细部署文档

- 📖 **[完整部署指南](DEPLOY.md)** - 详细的部署步骤和说明
- 🔄 **[迁移指南](MIGRATION.md)** - 从云服务器到局域网集群的迁移
- 📁 **[局域网配置说明](k8s-local/README.md)** - 局域网集群配置细节

### 访问地址

部署成功后可通过以下域名访问：
- https://origin-image-tools.aigchub.vip
- https://image-tools.aigchub.vip

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进项目。 