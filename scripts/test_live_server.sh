#!/bin/bash

# 线上服务器API测试脚本
# 测试部署在 8.130.35.126 上的图片工具箱API

set -e

# 线上服务器配置
LIVE_HOST="8.130.35.126"
LIVE_PORT="58888"
LIVE_BASE_URL="http://${LIVE_HOST}:${LIVE_PORT}"
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

# 测试网络连通性
test_connectivity() {
    print_info "测试网络连通性: $LIVE_HOST:$LIVE_PORT"
    
    if command -v nc &> /dev/null; then
        if nc -z -w5 "$LIVE_HOST" "$LIVE_PORT" 2>/dev/null; then
            print_success "网络连通性正常"
            return 0
        else
            print_error "无法连接到 $LIVE_HOST:$LIVE_PORT"
            return 1
        fi
    else
        print_warning "nc命令不可用，跳过网络连通性测试"
        return 0
    fi
}

# 测试API端点
test_api_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local description=$3
    local data=${4:-}
    
    print_info "测试 $description: $LIVE_BASE_URL$endpoint"
    
    local curl_cmd="curl -s -w \"HTTPSTATUS:%{http_code}\" --connect-timeout 10 --max-time 30"
    
    if [ "$method" = "POST" ]; then
        if [ -n "$data" ]; then
            curl_cmd="$curl_cmd -X POST -H \"Authorization: Bearer $TEST_TOKEN\" -H \"Content-Type: application/json\" -d '$data'"
        else
            curl_cmd="$curl_cmd -X POST -H \"Authorization: Bearer $TEST_TOKEN\" -H \"Content-Type: application/json\" -d '{\"test_data\": \"live_server_test\"}'"
        fi
    else
        if [ "$endpoint" != "/api/health" ]; then
            curl_cmd="$curl_cmd -H \"Authorization: Bearer $TEST_TOKEN\""
        fi
    fi
    
    curl_cmd="$curl_cmd \"$LIVE_BASE_URL$endpoint\""
    
    local response
    response=$(eval "$curl_cmd" 2>/dev/null || echo "HTTPSTATUS:000")
    
    local http_code
    http_code=$(echo "$response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    local body
    body=$(echo "$response" | sed 's/HTTPSTATUS:[0-9]*$//')
    
    echo "  HTTP状态码: $http_code"
    
    if [ "$http_code" = "200" ]; then
        print_success "$description 测试通过"
        
        # 检查响应格式
        if echo "$body" | grep -q '"code":200'; then
            print_success "响应格式正确 (统一JSON格式)"
        elif echo "$body" | grep -q '"code":[0-9]*'; then
            print_warning "响应格式部分正确 (包含code字段)"
        else
            print_warning "响应格式可能不符合规范"
        fi
        
        # 显示响应摘要
        if echo "$body" | grep -q '"message"'; then
            local message
            message=$(echo "$body" | grep -o '"message":"[^"]*"' | cut -d'"' -f4 | head -1)
            echo "  消息: $message"
        fi
        
        # 显示响应长度
        local body_length=${#body}
        echo "  响应长度: $body_length 字符"
        
        return 0
    else
        print_error "$description 测试失败"
        echo "  响应内容: ${body:0:200}..."
        return 1
    fi
}

# 主测试函数
main() {
    print_header "🌐 线上服务器API测试"
    echo "服务器地址: $LIVE_HOST"
    echo "服务端口: $LIVE_PORT"
    echo "完整URL: $LIVE_BASE_URL"
    echo ""
    
    # 测试网络连通性
    if ! test_connectivity; then
        print_error "网络连通性测试失败，停止测试"
        exit 1
    fi
    
    echo ""
    print_header "📍 开始API功能测试"
    
    # 测试计数器
    local total_tests=0
    local passed_tests=0
    
    # 1. 健康检查
    echo ""
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/health" "GET" "健康检查接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    # 2. 用户信息
    echo ""
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/v1/auth-example/user-info" "GET" "用户信息接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    # 3. 计费示例
    echo ""
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/v1/auth-example/billing-example" "POST" "计费示例接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    # 4. 过滤器列表
    echo ""
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/v1/filter/list" "GET" "过滤器列表接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    # 5. AI样式列表
    echo ""
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/v1/ai-text-to-image/styles" "GET" "AI样式列表接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    # 6. API文档访问测试
    echo ""
    total_tests=$((total_tests + 1))
    print_info "测试API文档访问: $LIVE_BASE_URL/docs"
    if curl -s --connect-timeout 10 --max-time 30 "$LIVE_BASE_URL/docs" | grep -q "Swagger" || curl -s --connect-timeout 10 --max-time 30 "$LIVE_BASE_URL/docs" | grep -q "FastAPI"; then
        print_success "API文档可访问"
        passed_tests=$((passed_tests + 1))
    else
        print_error "API文档访问失败"
    fi
    
    # 测试结果总结
    echo ""
    print_header "📊 测试结果总结"
    
    local success_rate
    success_rate=$(echo "scale=1; $passed_tests * 100 / $total_tests" | bc 2>/dev/null || echo "N/A")
    
    echo "服务器地址: $LIVE_HOST:$LIVE_PORT"
    echo "总测试数: $total_tests"
    echo "通过测试: $passed_tests"
    echo "成功率: $success_rate%"
    
    if [ "$passed_tests" -eq "$total_tests" ]; then
        print_success "🎉 所有测试通过！线上服务部署成功！"
        echo ""
        print_info "线上服务访问地址:"
        echo "  API文档: $LIVE_BASE_URL/docs"
        echo "  健康检查: $LIVE_BASE_URL/api/health"
        echo "  Swagger UI: $LIVE_BASE_URL/redoc"
        exit 0
    elif [ "$passed_tests" -gt 0 ]; then
        print_warning "部分测试通过，服务基本可用但可能存在问题"
        echo ""
        print_info "故障排查建议:"
        echo "  1. 检查失败的接口日志"
        echo "  2. 验证认证配置"
        echo "  3. 检查服务器资源状态"
        exit 1
    else
        print_error "❌ 所有测试失败，线上服务可能未正常运行"
        echo ""
        print_info "故障排查建议:"
        echo "  1. 检查服务器是否正常运行"
        echo "  2. 检查Docker容器状态"
        echo "  3. 检查防火墙和端口配置"
        echo "  4. 检查应用日志"
        exit 1
    fi
}

# 检查依赖
if ! command -v curl &> /dev/null; then
    print_error "curl 命令未找到，请安装 curl"
    exit 1
fi

if ! command -v bc &> /dev/null; then
    print_warning "bc 命令未找到，成功率计算可能不准确"
fi

# 运行主函数
main "$@"
