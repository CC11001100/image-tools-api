#!/bin/bash

# Docker部署测试脚本
# 测试使用Harbor镜像部署的图片工具箱服务

set -e

# 配置
HARBOR_REGISTRY="docker.zhaixingren.cn"
HARBOR_PROJECT="aigchub"
BACKEND_IMAGE="image-tools-api-backend"
FRONTEND_IMAGE="image-tools-api-frontend"
CONTAINER_NAME_BACKEND="image-tools-api-backend-test"
CONTAINER_NAME_FRONTEND="image-tools-api-frontend-test"
TEST_PORT_BACKEND="58889"
TEST_PORT_FRONTEND="58890"
TEST_TOKEN="aigc-hub-1f9562c6a18247aa82050bb78ffc479c"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}$1${NC}"
    echo "=================================================="
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}🔍 $1${NC}"
}

# 清理函数
cleanup() {
    print_info "清理测试容器..."
    docker stop "$CONTAINER_NAME_BACKEND" 2>/dev/null || true
    docker rm "$CONTAINER_NAME_BACKEND" 2>/dev/null || true
    docker stop "$CONTAINER_NAME_FRONTEND" 2>/dev/null || true
    docker rm "$CONTAINER_NAME_FRONTEND" 2>/dev/null || true
}

# 设置清理陷阱
trap cleanup EXIT

# 检查Docker镜像
check_images() {
    print_info "检查Harbor镜像..."
    
    local backend_image="$HARBOR_REGISTRY/$HARBOR_PROJECT/$BACKEND_IMAGE:latest"
    local frontend_image="$HARBOR_REGISTRY/$HARBOR_PROJECT/$FRONTEND_IMAGE:latest"
    
    if docker images | grep -q "$HARBOR_REGISTRY/$HARBOR_PROJECT/$BACKEND_IMAGE"; then
        print_success "后端镜像存在: $backend_image"
    else
        print_error "后端镜像不存在: $backend_image"
        print_info "请先运行部署脚本构建和推送镜像"
        exit 1
    fi
    
    if docker images | grep -q "$HARBOR_REGISTRY/$HARBOR_PROJECT/$FRONTEND_IMAGE"; then
        print_success "前端镜像存在: $frontend_image"
    else
        print_error "前端镜像不存在: $frontend_image"
        print_info "请先运行部署脚本构建和推送镜像"
        exit 1
    fi
}

# 启动后端容器
start_backend() {
    print_info "启动后端测试容器..."
    
    local backend_image="$HARBOR_REGISTRY/$HARBOR_PROJECT/$BACKEND_IMAGE:latest"
    
    docker run -d \
        --name "$CONTAINER_NAME_BACKEND" \
        -p "$TEST_PORT_BACKEND:8000" \
        -e DEVELOPMENT_MODE=true \
        -e ENVIRONMENT=development \
        "$backend_image"
    
    print_success "后端容器已启动: $CONTAINER_NAME_BACKEND"
    print_info "端口映射: $TEST_PORT_BACKEND:8000"
}

# 启动前端容器
start_frontend() {
    print_info "启动前端测试容器..."
    
    local frontend_image="$HARBOR_REGISTRY/$HARBOR_PROJECT/$FRONTEND_IMAGE:latest"
    
    docker run -d \
        --name "$CONTAINER_NAME_FRONTEND" \
        -p "$TEST_PORT_FRONTEND:80" \
        "$frontend_image"
    
    print_success "前端容器已启动: $CONTAINER_NAME_FRONTEND"
    print_info "端口映射: $TEST_PORT_FRONTEND:80"
}

# 等待服务启动
wait_for_service() {
    local port=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_info "等待 $service_name 服务启动..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "http://localhost:$port/api/health" >/dev/null 2>&1; then
            print_success "$service_name 服务已启动"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name 服务启动超时"
    return 1
}

# 测试API端点
test_api() {
    local port=$1
    local service_name=$2
    
    print_info "测试 $service_name API..."
    
    local base_url="http://localhost:$port"
    local success_count=0
    local total_tests=5
    
    # 1. 健康检查
    if curl -s "$base_url/api/health" | grep -q '"status":"running"'; then
        print_success "健康检查通过"
        success_count=$((success_count + 1))
    else
        print_error "健康检查失败"
    fi
    
    # 2. 用户信息
    if curl -s -H "Authorization: Bearer $TEST_TOKEN" "$base_url/api/v1/auth-example/user-info" | grep -q '"code":200'; then
        print_success "用户信息接口通过"
        success_count=$((success_count + 1))
    else
        print_error "用户信息接口失败"
    fi
    
    # 3. 过滤器列表
    if curl -s -H "Authorization: Bearer $TEST_TOKEN" "$base_url/api/v1/filter/list" | grep -q '"total":50'; then
        print_success "过滤器列表接口通过"
        success_count=$((success_count + 1))
    else
        print_error "过滤器列表接口失败"
    fi
    
    # 4. AI样式列表
    if curl -s -H "Authorization: Bearer $TEST_TOKEN" "$base_url/api/v1/ai-text-to-image/styles" | grep -q '"code":200'; then
        print_success "AI样式列表接口通过"
        success_count=$((success_count + 1))
    else
        print_error "AI样式列表接口失败"
    fi
    
    # 5. 计费示例
    if curl -s -X POST -H "Authorization: Bearer $TEST_TOKEN" -H "Content-Type: application/json" -d '{"test_data":"docker_test"}' "$base_url/api/v1/auth-example/billing-example" | grep -q '"call_id"'; then
        print_success "计费示例接口通过"
        success_count=$((success_count + 1))
    else
        print_error "计费示例接口失败"
    fi
    
    local success_rate
    success_rate=$(echo "scale=1; $success_count * 100 / $total_tests" | bc 2>/dev/null || echo "N/A")
    
    echo ""
    print_info "$service_name 测试结果: $success_count/$total_tests ($success_rate%)"
    
    return $success_count
}

# 主函数
main() {
    print_header "🐳 Docker部署测试"
    
    # 清理之前的测试容器
    cleanup
    
    # 检查镜像
    check_images
    
    echo ""
    print_header "🚀 启动测试容器"
    
    # 启动后端容器
    start_backend
    
    # 等待后端服务启动
    if ! wait_for_service "$TEST_PORT_BACKEND" "后端"; then
        print_error "后端服务启动失败"
        exit 1
    fi
    
    echo ""
    print_header "🧪 测试后端API"
    
    # 测试后端API
    backend_success=$(test_api "$TEST_PORT_BACKEND" "后端")
    
    echo ""
    print_header "📊 测试结果总结"
    
    echo "后端服务测试: $backend_success/5"
    
    if [ "$backend_success" -eq 5 ]; then
        print_success "🎉 Docker部署测试完全成功！"
        echo ""
        print_info "测试环境访问地址:"
        echo "  后端API文档: http://localhost:$TEST_PORT_BACKEND/docs"
        echo "  健康检查: http://localhost:$TEST_PORT_BACKEND/api/health"
        echo ""
        print_info "Harbor镜像验证成功:"
        echo "  后端镜像: $HARBOR_REGISTRY/$HARBOR_PROJECT/$BACKEND_IMAGE:latest"
        echo "  前端镜像: $HARBOR_REGISTRY/$HARBOR_PROJECT/$FRONTEND_IMAGE:latest"
        exit 0
    else
        print_error "❌ Docker部署测试部分失败"
        exit 1
    fi
}

# 检查依赖
if ! command -v docker &> /dev/null; then
    print_error "Docker 未安装或不可用"
    exit 1
fi

if ! command -v curl &> /dev/null; then
    print_error "curl 命令未找到"
    exit 1
fi

if ! command -v bc &> /dev/null; then
    print_warning "bc 命令未找到，成功率计算可能不准确"
fi

# 运行主函数
main "$@"
