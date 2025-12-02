# 从云服务器到局域网集群迁移指南

## 迁移背景

原本部署在云服务器 K8s 集群（8.130.35.126），现在迁移到局域网 K8s 集群（192.168.3.42）。
域名仍然从云服务器路由过来，实际服务运行在局域网集群。

## 迁移内容

### 1. 新增文件

#### K8s 配置文件（k8s-local/）
- `k8s-local/backend-deployment.yml` - 后端部署配置
- `k8s-local/frontend-deployment.yml` - 前端部署配置
- `k8s-local/service.yml` - Service 配置
- `k8s-local/ingress.yml` - Ingress 配置
- `k8s-local/README.md` - 局域网配置说明

#### 部署脚本
- `deploy-local.sh` - 局域网集群部署脚本（可执行）

#### 文档
- `DEPLOY.md` - 完整部署指南
- `MIGRATION.md` - 本迁移指南（你正在阅读）

### 2. 关键配置变更

#### 镜像仓库地址

| 环境 | 镜像地址 |
|------|---------|
| 云服务器 | `docker.zhaixingren.cn/aigchub/image-tools-api-*:latest` |
| 局域网 | `192.168.3.42:5000/aigchub/image-tools-api-*:latest` |

#### 部署方式

| 环境 | 部署方式 | 配置目录 | 部署脚本 |
|------|---------|---------|---------|
| 云服务器 | SSH + kubectl | k8s/ | deploy-prod.sh |
| 局域网 | kubectl-local | k8s-local/ | deploy-local.sh |

### 3. 保持不变的配置

以下配置在两套环境中保持一致：

✅ **Network**
- hostNetwork: true
- dnsPolicy: ClusterFirstWithHostNet

✅ **Namespace**
- aigchub-prod

✅ **Ingress**
- Traefik Ingress Controller
- TLS 证书: aigchub-vip-tls
- 域名: origin-image-tools.aigchub.vip, image-tools.aigchub.vip

✅ **资源限制**
- Backend: CPU 5m-50m, Memory 80Mi-128Mi
- Frontend: CPU 2m-20m, Memory 6Mi-16Mi

✅ **健康检查**
- Backend: /api/health (端口 58888)
- Frontend: /health (端口 80)

## 迁移步骤

### 步骤 1: 验证环境

```bash
# 验证 kubectl-local 可用
kubectl-local get nodes

# 验证镜像仓库可访问
docker login 192.168.3.42:5000

# 验证 namespace 存在
kubectl-local get namespace aigchub-prod

# 验证必需的 secrets 存在
kubectl-local get secret harbor-secret -n aigchub-prod
kubectl-local get secret aigchub-vip-tls -n aigchub-prod
```

### 步骤 2: 部署到局域网集群

```bash
# 执行部署脚本
./deploy-local.sh
```

该脚本会自动：
1. 清理旧镜像
2. 构建前端
3. 构建并推送后端镜像到 192.168.3.42:5000
4. 构建并推送前端镜像到 192.168.3.42:5000
5. 使用 kubectl-local 部署到集群
6. 等待服务就绪
7. 显示部署状态

### 步骤 3: 验证部署

```bash
# 检查 Pod 状态
kubectl-local get pods -n aigchub-prod | grep image-tools-api

# 检查 Service
kubectl-local get svc -n aigchub-prod | grep image-tools-api

# 检查 Ingress
kubectl-local get ingress -n aigchub-prod | grep image-tools-api

# 查看日志
kubectl-local logs -n aigchub-prod -l app=image-tools-api-backend --tail=50
kubectl-local logs -n aigchub-prod -l app=image-tools-api-frontend --tail=50
```

### 步骤 4: 测试访问

访问以下地址验证服务正常：
- https://origin-image-tools.aigchub.vip
- https://image-tools.aigchub.vip

## 网络架构

### 原有架构（云服务器）
```
Internet
    ↓
Domain (aigchub.vip)
    ↓
云服务器 K8s Ingress (8.130.35.126)
    ↓
Service → Pods (云服务器)
```

### 新架构（局域网）
```
Internet
    ↓
Domain (aigchub.vip)
    ↓
云服务器 K8s Ingress (路由转发)
    ↓
局域网 K8s Cluster (192.168.3.42)
    ↓
Traefik Ingress
    ↓
Service → Pods (局域网)
```

## 参考服务

局域网集群已有类似部署的服务：

### time-tools-api
- 镜像: `192.168.3.42:5000/aigchub/time-tools-api-*:latest`
- hostNetwork: true
- Traefik Ingress
- 域名: origin-time-tools.aigchub.vip, time-tools.aigchub.vip

### markdown-render
- 镜像: `192.168.3.42:5000/aigchub/markdown-render-*:latest`
- NodePort: 30007
- 域名: markdown-render.aigchub.vip

## 回滚方案

如果需要回滚到云服务器：

```bash
# 使用原有部署脚本
./deploy-prod.sh
```

## 常见问题

### Q: 两套环境可以同时运行吗？
A: 可以。它们使用不同的镜像仓库和 K8s 集群，互不影响。

### Q: 域名如何路由？
A: 域名仍然在云服务器配置，云服务器的 Ingress 会将流量路由到局域网集群。

### Q: 为什么使用 hostNetwork?
A: 某些服务可能需要特定的网络访问权限，如 IP 白名单验证。

### Q: 镜像架构是什么？
A: 统一使用 AMD64 架构（linux/amd64），确保在服务器上正常运行。

### Q: 资源使用情况如何监控？
A: 使用 `kubectl-local top pods -n aigchub-prod | grep image-tools-api`

## 相关命令速查

```bash
# 部署
./deploy-local.sh

# 查看状态
kubectl-local get pods -n aigchub-prod | grep image-tools-api
kubectl-local get svc -n aigchub-prod | grep image-tools-api
kubectl-local get ingress -n aigchub-prod | grep image-tools-api

# 查看日志
kubectl-local logs -n aigchub-prod -l app=image-tools-api-backend --tail=100 -f
kubectl-local logs -n aigchub-prod -l app=image-tools-api-frontend --tail=100 -f

# 查看资源
kubectl-local top pods -n aigchub-prod | grep image-tools-api

# 重启服务
kubectl-local rollout restart deployment/image-tools-api-backend -n aigchub-prod
kubectl-local rollout restart deployment/image-tools-api-frontend -n aigchub-prod

# 删除服务（谨慎操作）
kubectl-local delete -f k8s-local/
```

## 总结

✅ 已创建局域网集群配置（k8s-local/）
✅ 已创建部署脚本（deploy-local.sh）
✅ 已创建详细文档（DEPLOY.md, MIGRATION.md）
✅ 验证环境前置条件满足
✅ 参考现有服务配置（time-tools-api）

现在可以执行 `./deploy-local.sh` 部署到局域网集群了！
