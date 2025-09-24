# 使用更小的基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（只安装必需的）
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 创建优化的requirements.txt（使用opencv-python-headless）
COPY <<EOF requirements.optimized.txt
fastapi==0.103.1
uvicorn==0.23.2
python-multipart==0.0.6
Pillow>=10.0.0
python-dotenv==1.0.0
opencv-python-headless>=4.8.0
numpy>=1.24.0
scipy>=1.11.0
requests>=2.31.0
httpx>=0.25.0
PyJWT>=2.8.0
oss2>=2.18.0
EOF

# 配置pip使用国内镜像源并安装依赖
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn && \
    pip install --no-cache-dir -r requirements.optimized.txt && \
    pip cache purge

# 复制应用代码
COPY app/ ./app/
COPY start_backend.py .
COPY public/ ./public/

# 创建必要的目录
RUN mkdir -p uploads temp logs

# 暴露端口
EXPOSE 58888

# 启动命令
CMD ["python3", "start_backend.py"]
