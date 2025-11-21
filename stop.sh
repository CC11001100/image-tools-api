#!/bin/bash

echo "=== Image Tools API 停止脚本 ==="
echo "时间: $(date)"
echo

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 停止后端服务
echo -e "${BLUE}🛑 停止后端服务...${NC}"
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        sleep 2
        if kill -0 $BACKEND_PID 2>/dev/null; then
            echo -e "${YELLOW}⚠️  后端服务未响应，强制停止...${NC}"
            kill -9 $BACKEND_PID 2>/dev/null
        fi
        echo -e "${GREEN}✅ 后端服务已停止 (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠️  后端服务已经停止${NC}"
    fi
    rm -f .backend.pid
else
    echo -e "${YELLOW}⚠️  未找到后端PID文件，尝试按端口停止...${NC}"
    if lsof -i :58888 > /dev/null 2>&1; then
        lsof -ti :58888 | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✅ 后端服务已停止${NC}"
    else
        echo -e "${GREEN}✅ 后端服务未运行${NC}"
    fi
fi

echo

# 停止前端服务
echo -e "${BLUE}🛑 停止前端服务...${NC}"
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        sleep 2
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            echo -e "${YELLOW}⚠️  前端服务未响应，强制停止...${NC}"
            kill -9 $FRONTEND_PID 2>/dev/null
        fi
        echo -e "${GREEN}✅ 前端服务已停止 (PID: $FRONTEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠️  前端服务已经停止${NC}"
    fi
    rm -f .frontend.pid
else
    echo -e "${YELLOW}⚠️  未找到前端PID文件，尝试按端口停止...${NC}"
    if lsof -i :58889 > /dev/null 2>&1; then
        lsof -ti :58889 | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✅ 前端服务已停止${NC}"
    else
        echo -e "${GREEN}✅ 前端服务未运行${NC}"
    fi
fi

echo

# 检查端口状态
echo -e "${BLUE}🔍 检查端口状态...${NC}"
PORTS_TO_CHECK="58888 58889"
PORTS_STILL_IN_USE=""

for port in $PORTS_TO_CHECK; do
    if lsof -i :$port > /dev/null 2>&1; then
        PORTS_STILL_IN_USE="$PORTS_STILL_IN_USE $port"
        echo -e "${YELLOW}⚠️  端口 $port 仍被占用${NC}"
    else
        echo -e "${GREEN}✅ 端口 $port 已释放${NC}"
    fi
done

# 如果还有端口被占用，自动强制清理
if [ ! -z "$PORTS_STILL_IN_USE" ]; then
    echo
    echo -e "${BLUE}🔧 自动强制清理端口...${NC}"
    for port in $PORTS_STILL_IN_USE; do
        echo "强制清理端口 $port..."
        lsof -ti :$port | xargs kill -9 2>/dev/null || true
    done
    sleep 2
    echo -e "${GREEN}✅ 端口清理完成${NC}"
fi

echo
echo -e "${GREEN}=== 停止完成! ===${NC}"
echo -e "${BLUE}提示:${NC}"
echo "- 使用 ${BLUE}./start.sh${NC} 重新启动服务"
echo "- 使用 ${BLUE}./status.sh${NC} 检查服务状态" 