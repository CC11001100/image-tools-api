#!/bin/bash

# 图片工具箱项目编译脚本
# 负责前端构建、后端依赖安装和Docker镜像构建

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

# 检查依赖
check_dependencies() {
    print_green "检查依赖..."
    
    # 检查Node.js
    if ! command -v node &> /dev/null; then
        print_red "Node.js 未安装，请先安装 Node.js"
        exit 1
    fi
    print_green "✅ Node.js: $(node --version)"
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        print_red "npm 未安装，请先安装 npm"
        exit 1
    fi
    print_green "✅ npm: $(npm --version)"
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        print_red "Python3 未安装，请先安装 Python3"
        exit 1
    fi
    print_green "✅ Python3: $(python3 --version)"
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        print_red "pip3 未安装，请先安装 pip3"
        exit 1
    fi
    print_green "✅ pip3: $(pip3 --version)"
    
    # 检查Docker（可选）
    if command -v docker &> /dev/null; then
        print_green "✅ Docker: $(docker --version)"
    else
        print_yellow "⚠️ Docker 未安装，将跳过Docker镜像构建"
    fi
}

# 构建前端
build_frontend() {
    print_green "构建前端项目..."
    
    if [ ! -d "frontend" ]; then
        print_red "前端目录不存在，跳过前端构建"
        return
    fi
    
    cd frontend
    
    # 安装依赖
    if [ ! -d "node_modules" ]; then
        print_green "安装前端依赖..."
        npm install
    else
        print_green "前端依赖已存在，跳过安装"
    fi
    
    # 构建项目
    print_green "构建前端项目..."
    npm run build
    
    if [ -d "build" ]; then
        print_green "✅ 前端构建完成"
    else
        print_red "❌ 前端构建失败"
        exit 1
    fi
    
    cd ..
}

# 安装后端依赖
install_backend_deps() {
    print_green "安装后端依赖..."
    
    # 检查requirements.txt
    if [ ! -f "requirements.txt" ]; then
        print_red "requirements.txt 不存在"
        exit 1
    fi
    
    # 创建虚拟环境（如果不存在）
    if [ ! -d "venv" ]; then
        print_green "创建Python虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境并安装依赖
    print_green "激活虚拟环境并安装依赖..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    print_green "✅ 后端依赖安装完成"
}

# 构建Docker镜像
build_docker_images() {
    if ! command -v docker &> /dev/null; then
        print_yellow "Docker 未安装，跳过镜像构建"
        return
    fi
    
    print_green "构建Docker镜像..."
    
    # 构建前端镜像
    if [ -d "frontend" ] && [ -f "frontend/Dockerfile" ]; then
        print_green "构建前端Docker镜像..."
        cd frontend
        docker build -t image-tools-api-frontend:latest .
        cd ..
        print_green "✅ 前端镜像构建完成"
    else
        print_yellow "前端Dockerfile不存在，跳过前端镜像构建"
    fi
    
    # 构建后端镜像
    if [ -f "backend.Dockerfile" ]; then
        print_green "构建后端Docker镜像..."
        docker build -f backend.Dockerfile -t image-tools-api-backend:latest .
        print_green "✅ 后端镜像构建完成"
    else
        print_yellow "backend.Dockerfile不存在，跳过后端镜像构建"
    fi
}

# 验证构建结果
verify_build() {
    print_green "验证构建结果..."
    
    # 检查前端构建
    if [ -d "frontend/build" ]; then
        print_green "✅ 前端构建文件存在"
    else
        print_yellow "⚠️ 前端构建文件不存在"
    fi
    
    # 检查后端依赖
    if [ -d "venv" ]; then
        print_green "✅ Python虚拟环境存在"
    else
        print_yellow "⚠️ Python虚拟环境不存在"
    fi
    
    # 检查Docker镜像
    if command -v docker &> /dev/null; then
        FRONTEND_IMAGE=$(docker images -q image-tools-api-frontend:latest)
        BACKEND_IMAGE=$(docker images -q image-tools-api-backend:latest)
        
        if [ -n "$FRONTEND_IMAGE" ]; then
            print_green "✅ 前端Docker镜像存在"
        else
            print_yellow "⚠️ 前端Docker镜像不存在"
        fi
        
        if [ -n "$BACKEND_IMAGE" ]; then
            print_green "✅ 后端Docker镜像存在"
        else
            print_yellow "⚠️ 后端Docker镜像不存在"
        fi
    fi
}

# 主函数
main() {
    print_green "🚀 开始构建图片工具箱项目..."
    print_green "=" * 50
    
    # 检查依赖
    check_dependencies
    
    # 构建前端
    build_frontend
    
    # 安装后端依赖
    install_backend_deps
    
    # 构建Docker镜像
    build_docker_images
    
    # 验证构建结果
    verify_build
    
    print_green "=" * 50
    print_green "🎉 构建完成！"
    
    print_green "\n📋 下一步操作："
    print_green "1. 运行后端服务: ./scripts/run.sh backend"
    print_green "2. 运行前端服务: ./scripts/run.sh frontend"
    print_green "3. 运行完整服务: ./scripts/run.sh all"
    print_green "4. 运行测试: ./scripts/run.sh test"
}

# 执行主函数
main "$@"
