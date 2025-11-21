#!/bin/bash

echo "=== Image Tools API 本地启动脚本 ==="
echo "时间: $(date)"
echo

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查端口占用
echo -e "${BLUE}🔍 检查端口占用...${NC}"
PORTS_TO_CHECK="58888 58889"
PORTS_IN_USE=""

for port in $PORTS_TO_CHECK; do
    if lsof -i :$port > /dev/null 2>&1; then
        PORTS_IN_USE="$PORTS_IN_USE $port"
        echo -e "${YELLOW}⚠️  端口 $port 被占用${NC}"
    else
        echo -e "${GREEN}✅ 端口 $port 可用${NC}"
    fi
done

# 如果有端口被占用，自动清理
if [ ! -z "$PORTS_IN_USE" ]; then
    echo
    echo -e "${BLUE}🔧 自动清理占用端口...${NC}"
    for port in $PORTS_IN_USE; do
        echo "清理端口 $port..."
        lsof -ti :$port | xargs kill -9 2>/dev/null || true
    done
    sleep 2
    echo -e "${GREEN}✅ 端口清理完成${NC}"
fi

echo

# 检查Python环境
echo -e "${BLUE}🔍 检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3未安装，请先安装Python 3.11+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}✅ Python版本: $PYTHON_VERSION${NC}"

# 检查pip依赖
echo -e "${BLUE}🔍 检查Python依赖...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt文件不存在${NC}"
    exit 1
fi

# 检查并安装Python依赖
echo -e "${BLUE}📦 检查并安装Python依赖...${NC}"
pip3 install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python依赖安装完成${NC}"
else
    echo -e "${YELLOW}⚠️  Python依赖安装可能有问题，继续尝试启动...${NC}"
fi

echo

# 检查Node.js环境
echo -e "${BLUE}🔍 检查Node.js环境...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js未安装，请先安装Node.js 18+${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm未安装，请先安装npm${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
NPM_VERSION=$(npm --version)
echo -e "${GREEN}✅ Node.js版本: $NODE_VERSION${NC}"
echo -e "${GREEN}✅ npm版本: $NPM_VERSION${NC}"

# 检查前端依赖
echo -e "${BLUE}📦 检查前端依赖...${NC}"
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  前端依赖未安装，正在安装...${NC}"
    cd frontend
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 前端依赖安装完成${NC}"
    else
        echo -e "${RED}❌ 前端依赖安装失败${NC}"
        exit 1
    fi
    cd ..
else
    echo -e "${GREEN}✅ 前端依赖已安装${NC}"
fi

echo

# 启动后端服务
echo -e "${BLUE}🚀 启动后端服务...${NC}"
python3 start_backend.py &
BACKEND_PID=$!
echo -e "${GREEN}✅ 后端服务已启动 (PID: $BACKEND_PID)${NC}"

# 等待后端启动
echo -e "${BLUE}⏳ 等待后端服务就绪...${NC}"
sleep 5

# 检查后端是否启动成功
if curl -s http://localhost:58888/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 后端服务运行正常${NC}"
else
    echo -e "${YELLOW}⚠️  后端服务可能还在启动中...${NC}"
fi

echo

# 启动前端服务
echo -e "${BLUE}🚀 启动前端服务...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}✅ 前端服务已启动 (PID: $FRONTEND_PID)${NC}"

echo

# 保存PID到文件，方便后续停止
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo -e "${GREEN}=== 启动完成! ===${NC}"
echo -e "${BLUE}前端界面:${NC} http://localhost:58889"
echo -e "${BLUE}API文档:${NC}   http://localhost:58888/docs"
echo -e "${BLUE}健康检查:${NC} http://localhost:58888/api/health"
echo
echo -e "${YELLOW}提示:${NC}"
echo "- 使用 ${BLUE}./stop.sh${NC} 停止服务"
echo "- 使用 ${BLUE}./status.sh${NC} 检查服务状态"
echo "- 使用 ${BLUE}./test_api.sh${NC} 测试API功能"
echo "- 按 ${BLUE}Ctrl+C${NC} 可以停止此脚本，但服务会继续运行"
echo
echo -e "${BLUE}📋 服务进程信息:${NC}"
echo "后端PID: $BACKEND_PID"
echo "前端PID: $FRONTEND_PID"
echo

# 等待用户中断
echo -e "${YELLOW}按Ctrl+C退出监控模式（服务将继续运行）${NC}"
trap 'echo -e "\n${YELLOW}退出监控模式，服务继续运行...${NC}"; exit 0' INT

# 保持脚本运行，显示日志
while true; do
    sleep 30
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}❌ 后端服务已停止${NC}"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}❌ 前端服务已停止${NC}"
        break
    fi
    echo -e "${GREEN}✅ 服务运行正常 $(date)${NC}"
done
