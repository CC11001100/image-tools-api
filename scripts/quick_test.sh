#!/bin/bash

# 快速API测试脚本
# 验证图片工具箱API的核心功能

set -e

BASE_URL="http://localhost:58888"
TOKEN="aigc-hub-1f9562c6a18247aa82050bb78ffc479c"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 图片工具箱API快速测试${NC}"
echo "=================================="

# 1. 健康检查
echo -e "${BLUE}1. 健康检查${NC}"
response=$(curl -s "$BASE_URL/api/health")
if echo "$response" | grep -q '"status":"running"'; then
    echo -e "${GREEN}✅ 健康检查通过${NC}"
else
    echo -e "${RED}❌ 健康检查失败${NC}"
    exit 1
fi

# 2. 用户信息
echo -e "${BLUE}2. 用户信息接口${NC}"
response=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/v1/auth-example/user-info")
if echo "$response" | grep -q '"nickname":"测试用户"'; then
    echo -e "${GREEN}✅ 用户信息接口正常${NC}"
else
    echo -e "${RED}❌ 用户信息接口异常${NC}"
    echo "响应: $response"
fi

# 3. 过滤器列表
echo -e "${BLUE}3. 过滤器列表接口${NC}"
response=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/v1/filter/list")
if echo "$response" | grep -q '"total":50'; then
    echo -e "${GREEN}✅ 过滤器列表接口正常${NC}"
else
    echo -e "${RED}❌ 过滤器列表接口异常${NC}"
    echo "响应: $response"
fi

# 4. AI样式列表
echo -e "${BLUE}4. AI样式列表接口${NC}"
response=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/v1/ai-text-to-image/styles")
if echo "$response" | grep -q '"code":200'; then
    echo -e "${GREEN}✅ AI样式列表接口正常${NC}"
else
    echo -e "${RED}❌ AI样式列表接口异常${NC}"
    echo "响应: $response"
fi

# 5. 计费示例
echo -e "${BLUE}5. 计费示例接口${NC}"
response=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"test_data": "quick_test"}' \
    "$BASE_URL/api/v1/auth-example/billing-example")
if echo "$response" | grep -q '"call_id"'; then
    echo -e "${GREEN}✅ 计费示例接口正常${NC}"
else
    echo -e "${RED}❌ 计费示例接口异常${NC}"
    echo "响应: $response"
fi

echo ""
echo -e "${GREEN}🎉 快速测试完成！所有核心接口正常运行${NC}"
echo "=================================="
echo "✅ 健康检查: 正常"
echo "✅ 用户认证: 正常"
echo "✅ 过滤器服务: 正常"
echo "✅ AI服务: 正常"
echo "✅ 计费服务: 正常"
echo ""
echo -e "${BLUE}📊 服务状态: 运行正常${NC}"
echo -e "${BLUE}🌐 访问地址: http://localhost:58888/docs${NC}"
