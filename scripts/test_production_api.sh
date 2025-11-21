#!/bin/bash

# 生产环境API测试脚本
# 测试部署在生产服务器上的图片工具箱API

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/production_config.env"

# 加载配置文件
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
    echo "✅ 已加载配置文件: $CONFIG_FILE"
else
    echo "⚠️  配置文件不存在: $CONFIG_FILE"
    echo "使用默认配置..."
fi

# 默认配置 - 如果配置文件中没有设置，则使用这些默认值
PROD_HOST="${PROD_HOST:-your-production-host.com}"
PROD_PORT="${PROD_PORT:-80}"
PROD_PROTOCOL="${PROD_PROTOCOL:-http}"
TEST_TOKEN="${TEST_TOKEN:-aigc-hub-1f9562c6a18247aa82050bb78ffc479c}"
CONNECT_TIMEOUT="${CONNECT_TIMEOUT:-10}"
REQUEST_TIMEOUT="${REQUEST_TIMEOUT:-30}"

# 构建完整的生产环境URL
PROD_BASE_URL="${PROD_PROTOCOL}://${PROD_HOST}:${PROD_PORT}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 打印函数
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

# 检查配置
check_config() {
    if [ "$PROD_HOST" = "your-production-host.com" ]; then
        print_error "请先配置生产环境地址！"
        echo "请修改脚本中的以下变量："
        echo "  PROD_HOST=\"your-production-host.com\"  # 改为实际的服务器地址"
        echo "  PROD_PORT=\"80\"                        # 改为实际的端口号"
        echo "  PROD_PROTOCOL=\"http\"                  # 如果使用HTTPS，改为https"
        exit 1
    fi
    
    print_info "生产环境配置:"
    echo "  服务器地址: $PROD_HOST"
    echo "  端口: $PROD_PORT"
    echo "  协议: $PROD_PROTOCOL"
    echo "  完整URL: $PROD_BASE_URL"
    echo ""
}

# 测试网络连通性
test_connectivity() {
    print_info "测试网络连通性: $PROD_HOST:$PROD_PORT"
    
    if command -v nc &> /dev/null; then
        if nc -z -w5 "$PROD_HOST" "$PROD_PORT" 2>/dev/null; then
            print_success "网络连通性正常"
            return 0
        else
            print_error "无法连接到 $PROD_HOST:$PROD_PORT"
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
    
    print_info "测试 $description: $PROD_BASE_URL$endpoint"
    
    local curl_cmd="curl -s -w \"HTTPSTATUS:%{http_code}\" --connect-timeout $CONNECT_TIMEOUT --max-time $REQUEST_TIMEOUT"
    
    if [ "$method" = "POST" ]; then
        curl_cmd="$curl_cmd -X POST -H \"Authorization: Bearer $TEST_TOKEN\" -H \"Content-Type: application/json\" -d '{\"test_data\": \"production_test\"}'"
    else
        curl_cmd="$curl_cmd -H \"Authorization: Bearer $TEST_TOKEN\""
    fi
    
    curl_cmd="$curl_cmd \"$PROD_BASE_URL$endpoint\""
    
    local response
    response=$(eval "$curl_cmd" 2>/dev/null || echo "HTTPSTATUS:000")
    
    local http_code
    http_code=$(echo "$response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    local body
    body=$(echo "$response" | sed 's/HTTPSTATUS:[0-9]*$//')
    
    if [ "$http_code" = "200" ]; then
        print_success "$description 测试通过 (HTTP $http_code)"
        
        # 检查响应格式
        if echo "$body" | grep -q '"code":200'; then
            print_success "响应格式正确 (统一JSON格式)"
        else
            print_warning "响应格式可能不符合规范"
        fi
        
        # 显示响应摘要
        if echo "$body" | grep -q '"message"'; then
            local message
            message=$(echo "$body" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
            echo "  消息: $message"
        fi
        
        return 0
    else
        print_error "$description 测试失败 (HTTP $http_code)"
        echo "  响应内容: ${body:0:200}..."
        return 1
    fi
}

# 主测试函数
main() {
    print_header "🚀 生产环境API测试"
    
    # 检查配置
    check_config
    
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
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/health" "GET" "健康检查接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    echo ""
    
    # 2. 用户信息
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/v1/auth-example/user-info" "GET" "用户信息接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    echo ""
    
    # 3. 计费示例
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/v1/auth-example/billing-example" "POST" "计费示例接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    echo ""
    
    # 4. 过滤器列表
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/v1/filter/list" "GET" "过滤器列表接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    echo ""
    
    # 5. AI样式列表
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/api/v1/ai-text-to-image/styles" "GET" "AI样式列表接口"; then
        passed_tests=$((passed_tests + 1))
    fi
    
    # 测试结果总结
    echo ""
    print_header "📊 测试结果总结"
    
    local success_rate
    success_rate=$(echo "scale=1; $passed_tests * 100 / $total_tests" | bc 2>/dev/null || echo "N/A")
    
    echo "总测试数: $total_tests"
    echo "通过测试: $passed_tests"
    echo "成功率: $success_rate%"
    
    if [ "$passed_tests" -eq "$total_tests" ]; then
        print_success "🎉 所有测试通过！生产环境部署成功！"
        echo ""
        print_info "生产环境访问地址:"
        echo "  API文档: $PROD_BASE_URL/docs"
        echo "  健康检查: $PROD_BASE_URL/api/health"
        exit 0
    else
        print_error "❌ 部分测试失败，请检查生产环境配置"
        echo ""
        print_info "故障排查建议:"
        echo "  1. 检查服务器是否正常运行"
        echo "  2. 检查防火墙和端口配置"
        echo "  3. 检查Docker容器状态"
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
