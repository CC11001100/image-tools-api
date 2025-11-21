#!/bin/bash

# =====================================================
# Image Tools API - K8s 快速部署脚本
# =====================================================
#
# 功能：应用 K8s 配置并等待服务就绪
# 前提：镜像已经在 Harbor 中
#
# =====================================================

set -e

# 配置
NAMESPACE="aigchub-prod"
K8S_DIR="$(dirname "$0")"

# 颜色输出
print_green() { echo -e "\033[32m$1\033[0m"; }
print_red() { echo -e "\033[31m$1\033[0m"; }
print_yellow() { echo -e "\033[33m$1\033[0m"; }

# 错误处理
trap 'print_red "部署失败"' ERR

print_green "======================================================"
print_green "  Image Tools API - K8s 部署"
print_green "======================================================"

# 1. 检查环境
print_green "=== 检查环境 ==="
if ! kubectl get namespace ${NAMESPACE} >/dev/null 2>&1; then
    print_red "namespace ${NAMESPACE} 不存在"
    exit 1
fi
print_green "✓ K8s 连接正常"

# 2. 应用配置
print_green "=== 应用 K8s 配置 ==="
kubectl apply -f ${K8S_DIR}/backend-deployment.yml
kubectl apply -f ${K8S_DIR}/frontend-deployment.yml
kubectl apply -f ${K8S_DIR}/service.yml
kubectl apply -f ${K8S_DIR}/ingress.yml
print_green "✓ 配置已应用"

# 3. 等待服务就绪
print_green "=== 等待服务就绪 ==="
print_yellow "正在等待后端服务..."
kubectl rollout status deployment/image-tools-backend -n ${NAMESPACE} --timeout=600s
print_green "✓ 后端服务就绪"

print_yellow "正在等待前端服务..."
kubectl rollout status deployment/image-tools-frontend -n ${NAMESPACE} --timeout=300s
print_green "✓ 前端服务就绪"

# 4. 显示状态
print_green "=== 部署状态 ==="
kubectl get pods -n ${NAMESPACE} | grep image-tools
kubectl get svc -n ${NAMESPACE} | grep image-tools
kubectl get ingress -n ${NAMESPACE} | grep image-tools

print_green ""
print_green "======================================================"
print_green "🎉 部署成功！"
print_green "======================================================"
print_green "访问地址:"
print_green "  https://origin-image-tools.aigchub.vip"
print_green "  https://image-tools.aigchub.vip"
print_green ""
print_green "查看日志："
print_green "  kubectl logs -n ${NAMESPACE} -l app=image-tools-backend --tail=100 -f"
print_green "  kubectl logs -n ${NAMESPACE} -l app=image-tools-frontend --tail=100 -f"
print_green "======================================================"
