#!/bin/bash

# =====================================================
# Image Tools API - 局域网集群部署脚本
# =====================================================

set -e

# 配置
PROJECT_NAME="image-tools-api"
HARBOR_REGISTRY="192.168.3.42:5000"
HARBOR_NAMESPACE="aigchub"
K8S_NAMESPACE="aigchub-prod"
BUILD_DATE=$(date +%Y%m%d_%H%M%S)

# 镜像名称
BACKEND_IMAGE="${HARBOR_REGISTRY}/${HARBOR_NAMESPACE}/${PROJECT_NAME}-backend:latest"
FRONTEND_IMAGE="${HARBOR_REGISTRY}/${HARBOR_NAMESPACE}/${PROJECT_NAME}-frontend:latest"

# 颜色输出
print_green() { echo -e "\033[32m$1\033[0m"; }
print_red() { echo -e "\033[31m$1\033[0m"; }
print_yellow() { echo -e "\033[33m$1\033[0m"; }
print_blue() { echo -e "\033[34m$1\033[0m"; }

# 错误处理
trap 'print_red "部署失败，退出"; exit 1' ERR

print_green "======================================================"
print_green "  Image Tools API - 局域网集群部署"
print_green "======================================================"
print_blue "构建时间: ${BUILD_DATE}"
print_blue "目标集群: 192.168.3.42"
print_green ""

# 0. 清理旧镜像释放空间
print_green "=== [0/6] 清理本地镜像 ==="
print_yellow "删除本地旧镜像..."
docker rmi ${BACKEND_IMAGE} 2>/dev/null || true
docker rmi ${FRONTEND_IMAGE} 2>/dev/null || true
print_yellow "清理悬空镜像..."
docker image prune -f
print_green "✓ 本地镜像清理完成"

# 1. 构建前端
print_green "=== [1/6] 构建前端 ==="
cd frontend
if [ ! -d "node_modules" ]; then
    print_yellow "安装前端依赖..."
    pnpm install
fi
print_yellow "构建前端..."
pnpm build
print_green "✓ 前端构建完成"
cd ..

# 2. 构建后端镜像到本地 (AMD64架构)
print_green "=== [2/6] 构建后端镜像 (AMD64) ==="
print_yellow "构建镜像: ${BACKEND_IMAGE}"
docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  --sbom=false \
  -f backend.Dockerfile \
  -t ${BACKEND_IMAGE} \
  --load .
print_green "✓ 后端镜像构建完成"

# 3. 推送后端镜像并删除本地镜像
print_green "=== [3/6] 推送后端镜像 ==="
print_yellow "推送: ${BACKEND_IMAGE}"
docker push ${BACKEND_IMAGE}
print_green "✓ 后端镜像推送完成"
print_yellow "删除本地镜像..."
docker rmi ${BACKEND_IMAGE}
print_green "✓ 本地后端镜像已删除"

# 4. 构建前端镜像到本地 (AMD64架构)
print_green "=== [4/6] 构建前端镜像 (AMD64) ==="
print_yellow "构建镜像: ${FRONTEND_IMAGE}"
docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  --sbom=false \
  -f frontend/Dockerfile \
  -t ${FRONTEND_IMAGE} \
  --load .
print_green "✓ 前端镜像构建完成"

# 5. 推送前端镜像并删除本地镜像
print_green "=== [5/6] 推送前端镜像 ==="
print_yellow "推送: ${FRONTEND_IMAGE}"
docker push ${FRONTEND_IMAGE}
print_green "✓ 前端镜像推送完成"
print_yellow "删除本地镜像..."
docker rmi ${FRONTEND_IMAGE}
print_green "✓ 本地前端镜像已删除"

# 清理构建缓存
print_yellow "清理Docker构建缓存..."
docker builder prune -f --filter "until=24h"
print_green "✓ 构建缓存清理完成"

# 6. 部署到局域网 K8s 集群
print_green "=== [6/6] 部署到局域网 K8s 集群 ==="
print_yellow "使用 kubectl-local 部署..."

# 应用 K8s 配置
print_yellow "应用 Deployment 配置..."
kubectl --context=k3s-local apply -f k8s-local/backend-deployment.yml
kubectl --context=k3s-local apply -f k8s-local/frontend-deployment.yml

print_yellow "应用 Service 配置..."
kubectl --context=k3s-local apply -f k8s-local/service.yml

print_yellow "应用 Ingress 配置..."
kubectl --context=k3s-local apply -f k8s-local/ingress.yml

print_yellow "等待后端服务就绪..."
kubectl --context=k3s-local rollout status deployment/image-tools-api-backend -n ${K8S_NAMESPACE} --timeout=600s

print_yellow "等待前端服务就绪..."
kubectl --context=k3s-local rollout status deployment/image-tools-api-frontend -n ${K8S_NAMESPACE} --timeout=300s

print_green "✓ K8s 部署完成"

# 显示部署状态
print_yellow "=== 部署状态 ==="
kubectl --context=k3s-local get pods -n ${K8S_NAMESPACE} | grep image-tools-api || true
kubectl --context=k3s-local get svc -n ${K8S_NAMESPACE} | grep image-tools-api || true
kubectl --context=k3s-local get ingress -n ${K8S_NAMESPACE} | grep image-tools-api || true

print_green ""
print_green "======================================================"
print_green "🎉 部署成功！"
print_green "======================================================"
print_green "访问地址:"
print_green "  https://origin-image-tools.aigchub.vip"
print_green "  https://image-tools.aigchub.vip"
print_green ""
print_green "查看日志："
print_green "  kubectl --context=k3s-local logs -n ${K8S_NAMESPACE} -l app=image-tools-api-backend --tail=100 -f"
print_green "  kubectl --context=k3s-local logs -n ${K8S_NAMESPACE} -l app=image-tools-api-frontend --tail=100 -f"
print_green ""
print_green "查看资源使用情况："
print_green "  kubectl --context=k3s-local top pods -n ${K8S_NAMESPACE} | grep image-tools-api"
print_green "======================================================"
