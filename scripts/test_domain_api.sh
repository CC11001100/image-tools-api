#!/bin/bash

# 域名API测试脚本
# 测试部署在 image-tools.aigchub.vip 上的图片工具箱API

set -e

# 域名配置
DOMAIN="image-tools.aigchub.vip"
PROTOCOL="https"
BASE_URL="${PROTOCOL}://${DOMAIN}"
TEST_TOKEN="aigc-hub-1f9562c6a18247aa82050bb78ffc479c"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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
    echo -e "${CYAN}🔍 $1${NC}"
}

# 测试DNS解析
test_dns_resolution() {
    print_info "测试DNS解析: $DOMAIN"
    
    if command -v nslookup &> /dev/null; then
        local ip_address
        ip_address=$(nslookup "$DOMAIN" | grep -A1 "Name:" | grep "Address:" | awk '{print $2}' | head -1)
        if [ -n "$ip_address" ]; then
            print_success "DNS解析成功: $DOMAIN → $ip_address"
            return 0
        else
            print_error "DNS解析失败"
            return 1
        fi
    else
        print_warning "nslookup命令不可用，跳过DNS解析测试"
        return 0
    fi
}

# 测试SSL证书
test_ssl_certificate() {
    if [ "$PROTOCOL" = "https" ]; then
        print_info "测试SSL证书: $DOMAIN"
        
        if command -v openssl &> /dev/null; then
            local ssl_info
            ssl_info=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)
            if [ $? -eq 0 ]; then
                print_success "SSL证书有效"
                echo "  证书信息: $ssl_info"
                return 0
            else
                print_warning "SSL证书检查失败"
                return 1
            fi
        else
            print_warning "openssl命令不可用，跳过SSL证书测试"
            return 0
        fi
    else
        print_info "使用HTTP协议，跳过SSL证书测试"
        return 0
    fi
}

# 测试API端点
test_api_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local description=$3
    local data=${4:-}
    
    print_info "测试 $description: $BASE_URL$endpoint"
    
    local curl_cmd="curl -s -w \"HTTPSTATUS:%{http_code}\" --connect-timeout 15 --max-time 45"
    
    # 添加SSL选项（如果是HTTPS）
    if [ "$PROTOCOL" = "https" ]; then
        curl_cmd="$curl_cmd --insecure"  # 忽略SSL证书验证问题
    fi
    
    if [ "$method" = "POST" ]; then
        if [ -n "$data" ]; then
            curl_cmd="$curl_cmd -X POST -H \"Authorization: Bearer $TEST_TOKEN\" -H \"Content-Type: application/json\" -d '$data'"
        else
            curl_cmd="$curl_cmd -X POST -H \"Authorization: Bearer $TEST_TOKEN\" -H \"Content-Type: application/json\" -d '{\"test_data\": \"domain_test\"}'"
        fi
    else
        if [ "$endpoint" != "/health" ] && [ "$endpoint" != "/api/health" ]; then
            curl_cmd="$curl_cmd -H \"Authorization: Bearer $TEST_TOKEN\""
        fi
    fi
    
    curl_cmd="$curl_cmd \"$BASE_URL$endpoint\""
    
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
    elif [ "$http_code" = "301" ] || [ "$http_code" = "302" ]; then
        print_warning "$description 重定向 (HTTP $http_code)"
        echo "  可能需要检查URL或协议"
        return 1
    elif [ "$http_code" = "403" ]; then
        print_error "$description 访问被拒绝 (HTTP $http_code)"
        echo "  可能是IP白名单限制"
        return 1
    elif [ "$http_code" = "000" ]; then
        print_error "$description 连接失败"
        echo "  网络连接或DNS解析问题"
        return 1
    else
        print_error "$description 测试失败 (HTTP $http_code)"
        echo "  响应内容: ${body:0:200}..."
        return 1
    fi
}

# 主测试函数
main() {
    print_header "🌐 域名API测试"
    echo "域名: $DOMAIN"
    echo "协议: $PROTOCOL"
    echo "完整URL: $BASE_URL"
    echo ""
    
    # 测试DNS解析
    if ! test_dns_resolution; then
        print_warning "DNS解析失败，但继续测试..."
    fi
    
    echo ""
    
    # 测试SSL证书
    if ! test_ssl_certificate; then
        print_warning "SSL证书测试失败，但继续测试..."
    fi
    
    echo ""
    print_header "📍 开始API功能测试"
    
    # 测试计数器
    local total_tests=0
    local passed_tests=0
    
    # 1. 健康检查（两种路径都测试）
    echo ""
    total_tests=$((total_tests + 1))
    if test_api_endpoint "/health" "GET" "健康检查接口(Nginx)"; then
        passed_tests=$((passed_tests + 1))
    else
        # 如果/health失败，尝试/api/health
        if test_api_endpoint "/api/health" "GET" "健康检查接口(API)"; then
            passed_tests=$((passed_tests + 1))
        fi
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
    
    # 6. 前端页面访问测试
    echo ""
    total_tests=$((total_tests + 1))
    print_info "测试前端页面访问: $BASE_URL/"
    if curl -s --connect-timeout 15 --max-time 30 ${PROTOCOL:+--insecure} "$BASE_URL/" | grep -q -E "(React|Image Tools|图片工具|图像处理工具|<!DOCTYPE html>|<title>)"; then
        print_success "前端页面可访问"
        passed_tests=$((passed_tests + 1))
    else
        print_error "前端页面访问失败"
    fi
    
    # 测试结果总结
    echo ""
    print_header "📊 测试结果总结"
    
    local success_rate
    success_rate=$(echo "scale=1; $passed_tests * 100 / $total_tests" | bc 2>/dev/null || echo "N/A")
    
    echo "域名: $DOMAIN"
    echo "协议: $PROTOCOL"
    echo "总测试数: $total_tests"
    echo "通过测试: $passed_tests"
    echo "成功率: $success_rate%"
    
    if [ "$passed_tests" -eq "$total_tests" ]; then
        print_success "🎉 所有测试通过！域名服务部署成功！"
        echo ""
        print_info "域名服务访问地址:"
        echo "  前端页面: $BASE_URL/"
        echo "  API文档: $BASE_URL/docs"
        echo "  健康检查: $BASE_URL/health"
        echo "  Swagger UI: $BASE_URL/redoc"
        exit 0
    elif [ "$passed_tests" -gt 0 ]; then
        print_warning "部分测试通过，服务基本可用但可能存在问题"
        echo ""
        print_info "故障排查建议:"
        echo "  1. 检查失败的接口日志"
        echo "  2. 验证IP白名单配置"
        echo "  3. 检查Nginx反向代理配置"
        echo "  4. 验证SSL证书状态"
        exit 1
    else
        print_error "❌ 所有测试失败，域名服务可能未正常运行"
        echo ""
        print_info "故障排查建议:"
        echo "  1. 检查DNS解析是否正确"
        echo "  2. 验证服务器是否正常运行"
        echo "  3. 检查防火墙和端口配置"
        echo "  4. 验证Nginx配置"
        echo "  5. 检查Docker容器状态"
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
