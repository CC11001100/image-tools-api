# 后端容器 Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    libxrender1 \
    libfontconfig1 \
    libice6 \
    libxinerama1 \
    libxrandr2 \
    libxcursor1 \
    libxtst6 \
    libxi6 \
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

# 复制静态资源（示例文件等）
COPY public/ ./public/

# 创建必要的目录
RUN mkdir -p uploads temp logs

# 暴露端口
EXPOSE 58888

# 启动命令
CMD ["python3", "start_backend.py"]
