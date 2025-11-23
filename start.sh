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

# 自动清理旧进程
echo -e "${BLUE}🧹 检查并清理旧进程...${NC}"

# 清理后端进程
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${YELLOW}⚠️  发现旧的后端进程 (PID: $BACKEND_PID)，正在停止...${NC}"
        kill $BACKEND_PID 2>/dev/null || true
        sleep 2
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill -9 $BACKEND_PID 2>/dev/null || true
        fi
        echo -e "${GREEN}✅ 旧的后端进程已停止${NC}"
    fi
    rm -f .backend.pid
fi

# 清理前端进程
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${YELLOW}⚠️  发现旧的前端进程 (PID: $FRONTEND_PID)，正在停止...${NC}"
        kill $FRONTEND_PID 2>/dev/null || true
        sleep 2
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill -9 $FRONTEND_PID 2>/dev/null || true
        fi
        echo -e "${GREEN}✅ 旧的前端进程已停止${NC}"
    fi
    rm -f .frontend.pid
fi

# 检查端口占用（双重保险）
echo -e "${BLUE}🔍 检查端口占用...${NC}"
PORTS_TO_CHECK="58888 58889"
PORTS_IN_USE=""

for port in $PORTS_TO_CHECK; do
    if lsof -i :$port > /dev/null 2>&1; then
        PORTS_IN_USE="$PORTS_IN_USE $port"
        echo -e "${YELLOW}⚠️  端口 $port 仍被占用${NC}"
    else
        echo -e "${GREEN}✅ 端口 $port 可用${NC}"
    fi
done

# 如果有端口被占用，强制清理
if [ ! -z "$PORTS_IN_USE" ]; then
    echo
    echo -e "${BLUE}🔧 强制清理占用端口...${NC}"
    for port in $PORTS_IN_USE; do
        echo "清理端口 $port..."
        lsof -ti :$port | xargs kill -9 2>/dev/null || true
    done
    sleep 2
fi

echo

# 检查Python环境
echo -e "${BLUE}🔍 检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3未安装，请先安装Python 3.11+${NC}"
    exit 1
fi

# 检查并激活虚拟环境
if [ -d "venv" ]; then
    echo -e "${BLUE}🔍 检查虚拟环境...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✅ 虚拟环境已激活${NC}"
    PYTHON_CMD="venv/bin/python3"
else
    echo -e "${YELLOW}⚠️  未找到虚拟环境，使用系统Python${NC}"
    PYTHON_CMD="python3"
fi

PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}✅ Python版本: $PYTHON_VERSION${NC}"

# 检查pip依赖
echo -e "${BLUE}🔍 检查Python依赖...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt文件不存在${NC}"
    exit 1
fi

# 检查并安装Python依赖
if [ -d "venv" ]; then
    echo -e "${BLUE}📦 检查并安装Python依赖...${NC}"
    venv/bin/pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Python依赖安装完成${NC}"
    else
        echo -e "${YELLOW}⚠️  Python依赖安装可能有问题，继续尝试启动...${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  跳过依赖安装（未找到虚拟环境）${NC}"
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

# 创建日志目录
mkdir -p logs

# 启动后端服务（后台运行）
echo -e "${BLUE}🚀 启动后端服务...${NC}"
nohup $PYTHON_CMD start_backend.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✅ 后端服务已启动 (PID: $BACKEND_PID)${NC}"
echo -e "${BLUE}📝 后端日志: logs/backend.log${NC}"

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

# 启动前端服务（后台运行）
echo -e "${BLUE}🚀 启动前端服务...${NC}"
cd frontend
nohup npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}✅ 前端服务已启动 (PID: $FRONTEND_PID)${NC}"
echo -e "${BLUE}📝 前端日志: logs/frontend.log${NC}"

echo

# 保存PID到文件，方便后续停止
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo -e "${GREEN}=== 启动完成! ===${NC}"
echo -e "${BLUE}前端界面:${NC} http://localhost:58889"
echo -e "${BLUE}API文档:${NC}   http://localhost:58888/docs"
echo -e "${BLUE}健康检查:${NC} http://localhost:58888/api/health"
echo
echo -e "${BLUE}📋 服务进程信息:${NC}"
echo "后端PID: $BACKEND_PID (保存在 .backend.pid)"
echo "前端PID: $FRONTEND_PID (保存在 .frontend.pid)"
echo
echo -e "${YELLOW}💡 提示:${NC}"
echo "- 使用 ${BLUE}./stop.sh${NC} 停止服务"
echo "- 使用 ${BLUE}tail -f logs/backend.log${NC} 查看后端日志"
echo "- 使用 ${BLUE}tail -f logs/frontend.log${NC} 查看前端日志"
echo "- 服务已在后台运行，关闭此终端窗口不影响服务"
echo
echo -e "${GREEN}✨ 服务已在后台启动成功！${NC}"
