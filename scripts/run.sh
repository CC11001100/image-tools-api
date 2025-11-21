#!/bin/bash

# 图片工具箱项目运行脚本
# 支持运行前端、后端、完整服务和测试

set -e

# 颜色输出
print_green() {
    echo -e "\033[32m$1\033[0m"
}

print_red() {
    echo -e "\033[31m$1\033[0m"
}

print_yellow() {
    echo -e "\033[33m$1\033[0m"
}

print_blue() {
    echo -e "\033[34m$1\033[0m"
}

# 显示帮助信息
show_help() {
    print_blue "图片工具箱项目运行脚本"
    print_blue "========================"
    echo ""
    print_green "用法: $0 [命令]"
    echo ""
    print_green "可用命令:"
    echo "  backend    - 运行后端服务 (FastAPI)"
    echo "  frontend   - 运行前端服务 (React开发服务器)"
    echo "  all        - 运行完整服务 (前端+后端)"
    echo "  docker     - 使用Docker运行服务"
    echo "  test       - 运行API测试"
    echo "  stop       - 停止所有服务"
    echo "  status     - 查看服务状态"
    echo "  logs       - 查看服务日志"
    echo "  help       - 显示此帮助信息"
    echo ""
    print_green "示例:"
    echo "  $0 backend     # 只运行后端"
    echo "  $0 frontend    # 只运行前端"
    echo "  $0 all         # 运行前后端"
    echo "  $0 test        # 运行测试"
}

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # 端口被占用
    else
        return 1  # 端口空闲
    fi
}

# 运行后端服务
run_backend() {
    print_green "🚀 启动后端服务..."
    
    # 检查端口
    if check_port 58888; then
        print_yellow "⚠️ 端口58888已被占用，请先停止现有服务"
        print_yellow "运行 '$0 stop' 停止服务"
        exit 1
    fi
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        print_red "❌ Python虚拟环境不存在，请先运行构建脚本"
        print_red "运行: ./scripts/build.sh"
        exit 1
    fi
    
    # 激活虚拟环境并启动服务
    print_green "激活Python虚拟环境..."
    source venv/bin/activate
    
    print_green "启动FastAPI服务..."
    print_blue "后端服务地址: http://localhost:58888"
    print_blue "API文档地址: http://localhost:58888/docs"
    
    # 设置环境变量
    export DEVELOPMENT_MODE=true
    export ENVIRONMENT=development
    
    # 启动服务
    python start_backend.py
}

# 运行前端服务
run_frontend() {
    print_green "🚀 启动前端服务..."
    
    if [ ! -d "frontend" ]; then
        print_red "❌ 前端目录不存在"
        exit 1
    fi
    
    cd frontend
    
    # 检查依赖
    if [ ! -d "node_modules" ]; then
        print_red "❌ 前端依赖未安装，请先运行构建脚本"
        print_red "运行: ./scripts/build.sh"
        exit 1
    fi
    
    # 检查端口
    if check_port 3000; then
        print_yellow "⚠️ 端口3000已被占用，React将尝试使用其他端口"
    fi
    
    print_green "启动React开发服务器..."
    print_blue "前端服务地址: http://localhost:3000"
    
    # 启动开发服务器
    npm start
}

# 运行完整服务
run_all() {
    print_green "🚀 启动完整服务 (前端+后端)..."
    
    # 检查端口
    if check_port 58888; then
        print_yellow "⚠️ 后端端口58888已被占用"
        exit 1
    fi
    
    if check_port 3000; then
        print_yellow "⚠️ 前端端口3000已被占用"
    fi
    
    # 在后台启动后端
    print_green "启动后端服务..."
    nohup bash -c "source venv/bin/activate && export DEVELOPMENT_MODE=true && export ENVIRONMENT=development && python start_backend.py" > logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > logs/backend.pid
    
    # 等待后端启动
    print_green "等待后端服务启动..."
    sleep 5
    
    # 检查后端是否启动成功
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_red "❌ 后端服务启动失败"
        cat logs/backend.log
        exit 1
    fi
    
    # 测试后端健康状态
    for i in {1..10}; do
        if curl -s http://localhost:58888/api/health >/dev/null 2>&1; then
            print_green "✅ 后端服务启动成功"
            break
        fi
        if [ $i -eq 10 ]; then
            print_red "❌ 后端服务健康检查失败"
            exit 1
        fi
        sleep 2
    done
    
    # 启动前端
    print_green "启动前端服务..."
    cd frontend
    
    print_blue "服务地址:"
    print_blue "  前端: http://localhost:3000"
    print_blue "  后端: http://localhost:58888"
    print_blue "  API文档: http://localhost:58888/docs"
    
    # 启动前端（前台运行）
    npm start
}

# 使用Docker运行
run_docker() {
    print_green "🐳 使用Docker运行服务..."
    
    if ! command -v docker &> /dev/null; then
        print_red "❌ Docker未安装"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_red "❌ docker-compose未安装"
        exit 1
    fi
    
    # 检查镜像是否存在
    if ! docker images | grep -q "image-tools-api-frontend"; then
        print_red "❌ 前端Docker镜像不存在，请先运行构建脚本"
        exit 1
    fi
    
    if ! docker images | grep -q "image-tools-api-backend"; then
        print_red "❌ 后端Docker镜像不存在，请先运行构建脚本"
        exit 1
    fi
    
    # 启动服务
    print_green "启动Docker服务..."
    docker-compose up -d
    
    print_green "等待服务启动..."
    sleep 10
    
    # 检查服务状态
    docker-compose ps
    
    print_blue "服务地址:"
    print_blue "  前端: http://localhost:58889"
    print_blue "  后端: http://localhost:58888"
    print_blue "  API文档: http://localhost:58888/docs"
}

# 运行测试
run_test() {
    print_green "🧪 运行API测试..."
    
    # 检查后端是否运行
    if ! curl -s http://localhost:58888/api/health >/dev/null 2>&1; then
        print_red "❌ 后端服务未运行，请先启动后端服务"
        print_red "运行: $0 backend"
        exit 1
    fi
    
    # 运行测试脚本
    if [ -f "scripts/test_all_apis.py" ]; then
        python3 scripts/test_all_apis.py
    else
        print_red "❌ 测试脚本不存在"
        exit 1
    fi
}

# 停止服务
stop_services() {
    print_green "🛑 停止所有服务..."
    
    # 停止Docker服务
    if command -v docker-compose &> /dev/null; then
        docker-compose down 2>/dev/null || true
    fi
    
    # 停止后端进程
    if [ -f "logs/backend.pid" ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            print_green "停止后端服务 (PID: $BACKEND_PID)"
            kill $BACKEND_PID
        fi
        rm -f logs/backend.pid
    fi
    
    # 停止占用端口的进程
    for port in 58888 3000 58889; do
        PID=$(lsof -ti:$port 2>/dev/null || true)
        if [ -n "$PID" ]; then
            print_green "停止端口 $port 上的进程 (PID: $PID)"
            kill $PID 2>/dev/null || true
        fi
    done
    
    print_green "✅ 所有服务已停止"
}

# 查看服务状态
show_status() {
    print_green "📊 服务状态检查..."
    
    # 检查端口状态
    for port in 58888 3000 58889; do
        if check_port $port; then
            PID=$(lsof -ti:$port 2>/dev/null || echo "未知")
            print_green "✅ 端口 $port: 运行中 (PID: $PID)"
        else
            print_yellow "❌ 端口 $port: 未运行"
        fi
    done
    
    # 检查Docker服务
    if command -v docker-compose &> /dev/null; then
        print_green "\n🐳 Docker服务状态:"
        docker-compose ps 2>/dev/null || print_yellow "Docker服务未运行"
    fi
    
    # 检查后端健康状态
    print_green "\n🏥 后端健康检查:"
    if curl -s http://localhost:58888/api/health >/dev/null 2>&1; then
        HEALTH_RESPONSE=$(curl -s http://localhost:58888/api/health)
        print_green "✅ 后端服务健康: $HEALTH_RESPONSE"
    else
        print_yellow "❌ 后端服务不可访问"
    fi
}

# 查看日志
show_logs() {
    print_green "📋 查看服务日志..."
    
    if [ -f "logs/backend.log" ]; then
        print_green "\n📄 后端日志 (最近20行):"
        tail -20 logs/backend.log
    else
        print_yellow "后端日志文件不存在"
    fi
    
    if command -v docker-compose &> /dev/null; then
        print_green "\n🐳 Docker日志:"
        docker-compose logs --tail=20 2>/dev/null || print_yellow "Docker服务未运行"
    fi
}

# 创建日志目录
mkdir -p logs

# 主函数
case "${1:-help}" in
    "backend")
        run_backend
        ;;
    "frontend")
        run_frontend
        ;;
    "all")
        run_all
        ;;
    "docker")
        run_docker
        ;;
    "test")
        run_test
        ;;
    "stop")
        stop_services
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "help"|*)
        show_help
        ;;
esac
