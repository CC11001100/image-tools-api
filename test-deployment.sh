#!/bin/bash

# =====================================================
# Image Tools API - 部署测试脚本
# =====================================================

# 颜色输出
print_green() { echo -e "\033[32m✓ $1\033[0m"; }
print_red() { echo -e "\033[31m✗ $1\033[0m"; }
print_yellow() { echo -e "\033[33m→ $1\033[0m"; }
print_blue() { echo -e "\033[34m$1\033[0m"; }

BASE_URL="https://origin-image-tools.aigchub.vip"

print_blue "======================================================"
print_blue "  Image Tools API - 部署测试"
print_blue "======================================================"
echo ""

# 1. 测试K8s资源状态
print_yellow "1. 检查K8s资源状态..."
kubectl --context=k3s-local get pods -n aigchub-prod | grep image-tools-api
kubectl --context=k3s-local get svc -n aigchub-prod | grep image-tools-api
kubectl --context=k3s-local get ingress -n aigchub-prod | grep image-tools-api
echo ""

# 2. 测试健康检查
print_yellow "2. 测试健康检查..."
HEALTH_STATUS=$(curl -s -k ${BASE_URL}/api/health | jq -r '.data.status')
if [ "$HEALTH_STATUS" == "running" ]; then
    print_green "后端健康检查通过"
else
    print_red "后端健康检查失败"
    exit 1
fi
echo ""

# 3. 测试API文档
print_yellow "3. 测试API文档..."
DOCS_STATUS=$(curl -s -k ${BASE_URL}/docs -o /dev/null -w "%{http_code}")
if [ "$DOCS_STATUS" == "200" ]; then
    print_green "API文档访问正常"
else
    print_red "API文档访问失败: HTTP $DOCS_STATUS"
fi
echo ""

# 4. 测试OpenAPI规范
print_yellow "4. 测试OpenAPI规范..."
OPENAPI_STATUS=$(curl -s -k ${BASE_URL}/openapi.json -o /dev/null -w "%{http_code}")
if [ "$OPENAPI_STATUS" == "200" ]; then
    print_green "OpenAPI规范访问正常"
else
    print_red "OpenAPI规范访问失败: HTTP $OPENAPI_STATUS"
fi
echo ""

# 5. 测试后端服务组件
print_yellow "5. 检查服务组件状态..."
REDIS_STATUS=$(curl -s -k ${BASE_URL}/api/health | jq -r '.data.redis.status')
if [ "$REDIS_STATUS" == "connected" ]; then
    print_green "Redis连接正常"
else
    print_red "Redis连接失败"
fi
echo ""

# 6. 测试认证
print_yellow "6. 测试API认证..."
AUTH_MSG=$(curl -s -k -X POST ${BASE_URL}/api/v1/image/text-to-image \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer aigc-hub-test" \
    -d '{"text":"Test"}' | jq -r '.message')
if [[ "$AUTH_MSG" == *"未授权"* ]] || [[ "$AUTH_MSG" == *"登录"* ]]; then
    print_green "API认证系统工作正常"
else
    print_yellow "API认证响应: $AUTH_MSG"
fi
echo ""

# 7. 测试各个域名
print_yellow "7. 测试域名访问..."
for DOMAIN in "origin-image-tools.aigchub.vip" "image-tools.aigchub.vip"; do
    STATUS=$(curl -s -k https://${DOMAIN}/api/health -o /dev/null -w "%{http_code}")
    if [ "$STATUS" == "200" ]; then
        print_green "$DOMAIN 访问正常"
    else
        print_red "$DOMAIN 访问失败: HTTP $STATUS"
    fi
done
echo ""

# 8. 查看资源使用情况
print_yellow "8. 资源使用情况..."
kubectl --context=k3s-local top pods -n aigchub-prod | grep image-tools-api || print_yellow "metrics-server未安装"
echo ""

# 9. 检查Pod日志
print_yellow "9. 检查最近日志..."
print_blue "后端日志(最后5行):"
kubectl --context=k3s-local logs -n aigchub-prod -l app=image-tools-api-backend --tail=5
echo ""
print_blue "前端日志(最后5行):"
kubectl --context=k3s-local logs -n aigchub-prod -l app=image-tools-api-frontend --tail=5
echo ""

# 总结
print_blue "======================================================"
print_green "🎉 部署测试完成！"
print_blue "======================================================"
print_blue "访问地址:"
print_blue "  https://origin-image-tools.aigchub.vip"
print_blue "  https://image-tools.aigchub.vip"
print_blue "  https://origin-image-tools.aigchub.vip/docs"
print_blue "======================================================"
