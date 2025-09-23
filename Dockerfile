# 多阶段构建：前端构建阶段
FROM node:18-alpine AS frontend-builder

# 设置前端工作目录
WORKDIR /app/frontend

# 复制前端package文件
COPY frontend/package*.json ./

# 安装前端依赖
RUN npm ci --only=production

# 复制前端源码
COPY frontend/ ./

# 构建前端
RUN npm run build

# 后端构建阶段
FROM docker.zhaixingren.cn/aigchub/admin-backend:latest

# 设置工作目录
WORKDIR /app

# 安装基本系统依赖和OpenCV依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 复制Python依赖文件
COPY requirements.txt .

# 配置pip使用国内镜像源并安装Python依赖
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn && \
    pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY app/ ./app/
COPY start_backend.py .

# 复制静态资源
COPY public/ ./public/

# 从前端构建阶段复制构建产物
COPY --from=frontend-builder /app/frontend/build ./frontend_build

# 创建必要的目录
RUN mkdir -p uploads temp logs

# 复制启动脚本
COPY start_docker.py .

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# 启动命令
CMD ["python3", "start_docker.py"]
