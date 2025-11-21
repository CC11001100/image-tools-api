#!/bin/bash

echo "=== Image Tools API 本地环境清理脚本 ==="
echo "时间: $(date)"
echo

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}⚠️  开始清理本地开发环境...${NC}"
echo -e "${YELLOW}包括: 服务进程、PID文件、临时文件、日志等${NC}"
echo

# 停止服务进程
echo -e "${BLUE}🛑 停止运行中的服务...${NC}"
./stop.sh

echo

# 清理PID文件
echo -e "${BLUE}🗑️  清理PID文件...${NC}"
if [ -f ".backend.pid" ]; then
    rm -f .backend.pid
    echo "✅ 删除后端PID文件"
fi
if [ -f ".frontend.pid" ]; then
    rm -f .frontend.pid
    echo "✅ 删除前端PID文件"
fi

# 强制清理端口占用
echo -e "${BLUE}🔧 强制清理端口占用...${NC}"
PORTS_TO_CLEAN="58888 58889"
for port in $PORTS_TO_CLEAN; do
    if lsof -i :$port > /dev/null 2>&1; then
        echo "强制清理端口 $port..."
        lsof -ti :$port | xargs kill -9 2>/dev/null || true
    else
        echo "✅ 端口 $port 未被占用"
    fi
done

# 清理临时文件
echo -e "${BLUE}📁 清理临时文件...${NC}"
if [ -d "uploads" ]; then
    rm -rf uploads/*
    echo "✅ 清理上传文件目录"
fi
if [ -d "temp" ]; then
    rm -rf temp/*
    echo "✅ 清理临时文件目录"
fi
if [ -d "logs" ]; then
    rm -rf logs/*
    echo "✅ 清理日志文件目录"
fi

# 清理前端构建产物（可选）
echo -e "${BLUE}🏗️  清理前端构建产物...${NC}"
if [ -d "frontend/build" ]; then
    rm -rf frontend/build
    echo "✅ 删除前端构建目录"
fi

# 清理Python缓存
echo -e "${BLUE}🐍 清理Python缓存...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
echo "✅ 清理Python缓存文件"

# 清理npm缓存（可选，不删除node_modules）
echo -e "${BLUE}📦 清理npm缓存...${NC}"
cd frontend
npm cache clean --force 2>/dev/null || true
cd ..
echo "✅ 清理npm缓存"

echo
echo -e "${GREEN}=== 清理完成! ===${NC}"
echo -e "${BLUE}提示:${NC}"
echo "- 使用 ${BLUE}./start.sh${NC} 重新启动服务"
echo "- 使用 ${BLUE}./status.sh${NC} 检查服务状态"
echo "- 如需重新安装依赖，删除 ${BLUE}frontend/node_modules${NC} 后运行启动脚本" 