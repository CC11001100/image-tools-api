# 局域网集群配置说明

## 概述

本目录包含用于部署到局域网 K8s 集群 (192.168.3.42) 的配置文件。

## 与云服务器配置的主要区别

### 1. 镜像仓库地址

**云服务器 (k8s/):**
```yaml
image: docker.zhaixingren.cn/aigchub/image-tools-api-backend:latest
```

**局域网集群 (k8s-local/):**
```yaml
image: 192.168.3.42:5000/aigchub/image-tools-api-backend:latest
```

### 2. 部署命令

- **云服务器**: 需要 SSH 到 8.130.35.126，然后使用 `kubectl`
- **局域网集群**: 直接使用 `kubectl-local` 命令

### 3. 架构特点

两套配置都使用以下特性：

✅ **hostNetwork: true**
- 让 Pod 使用宿主机网络
- 适合需要特定网络访问的服务

✅ **Traefik Ingress**
- 使用 Traefik 作为 Ingress Controller
- 支持 TLS/HTTPS
- 自动 HTTP 到 HTTPS 重定向

✅ **相同的命名空间**
- namespace: aigchub-prod
- 保持统一的命名规范

## 配置文件说明

### backend-deployment.yml
后端 Deployment 配置：
- 端口: 58888
- 资源限制: CPU 5m-50m, Memory 80Mi-128Mi
- 健康检查: /api/health
- 挂载卷: uploads, temp, logs

### frontend-deployment.yml
前端 Deployment 配置：
- 端口: 80
- 资源限制: CPU 2m-20m, Memory 6Mi-16Mi
- 健康检查: /health

### service.yml
Service 配置：
- **backend-service**: ClusterIP, 端口映射 80 -> 58888
- **frontend-service**: ClusterIP, 端口映射 80 -> 80

### ingress.yml
Ingress 配置：
- **域名**: 
  - origin-image-tools.aigchub.vip
  - image-tools.aigchub.vip
- **路由规则**:
  - `/api` -> backend-service
  - `/health` -> backend-service
  - `/docs` -> backend-service
  - `/openapi.json` -> backend-service
  - `/` -> frontend-service
- **TLS**: 使用 aigchub-vip-tls secret

## 部署流程

1. **构建镜像**（本地）
   ```bash
   # 构建后端镜像
   docker buildx build --platform linux/amd64 -f backend.Dockerfile -t 192.168.3.42:5000/aigchub/image-tools-api-backend:latest .
   
   # 构建前端镜像
   docker buildx build --platform linux/amd64 -f frontend/Dockerfile -t 192.168.3.42:5000/aigchub/image-tools-api-frontend:latest .
   ```

2. **推送镜像**（本地）
   ```bash
   docker push 192.168.3.42:5000/aigchub/image-tools-api-backend:latest
   docker push 192.168.3.42:5000/aigchub/image-tools-api-frontend:latest
   ```

3. **部署到集群**（本地）
   ```bash
   kubectl-local apply -f k8s-local/backend-deployment.yml
   kubectl-local apply -f k8s-local/frontend-deployment.yml
   kubectl-local apply -f k8s-local/service.yml
   kubectl-local apply -f k8s-local/ingress.yml
   ```

4. **等待就绪**
   ```bash
   kubectl-local rollout status deployment/image-tools-api-backend -n aigchub-prod
   kubectl-local rollout status deployment/image-tools-api-frontend -n aigchub-prod
   ```

## 快速部署

使用提供的部署脚本自动完成上述所有步骤：

```bash
./deploy-local.sh
```

## 验证部署

### 检查 Pod 状态
```bash
kubectl-local get pods -n aigchub-prod | grep image-tools-api
```

### 检查 Service
```bash
kubectl-local get svc -n aigchub-prod | grep image-tools-api
```

### 检查 Ingress
```bash
kubectl-local get ingress -n aigchub-prod | grep image-tools-api
```

### 查看日志
```bash
# 后端日志
kubectl-local logs -n aigchub-prod -l app=image-tools-api-backend --tail=50

# 前端日志
kubectl-local logs -n aigchub-prod -l app=image-tools-api-frontend --tail=50
```

### 查看资源使用
```bash
kubectl-local top pods -n aigchub-prod | grep image-tools-api
```

## 故障排查

### Pod 启动失败
1. 检查镜像是否正确推送
2. 检查 harbor-secret 是否存在
3. 查看 Pod 事件: `kubectl-local describe pod <pod-name> -n aigchub-prod`

### 服务无法访问
1. 检查 Service 是否正确创建
2. 检查 Ingress 是否正确配置
3. 检查 TLS secret 是否存在: `kubectl-local get secret aigchub-vip-tls -n aigchub-prod`

### 健康检查失败
1. 查看 Pod 日志检查应用是否正常启动
2. 确认健康检查路径是否正确
3. 检查端口映射是否正确

## 参考

参考了以下已部署的服务配置：
- time-tools-api: 时间工具 API
- markdown-render: Markdown 渲染服务

这些服务都使用相同的部署模式：
- 镜像仓库: 192.168.3.42:5000
- hostNetwork: true
- Traefik Ingress
- aigchub-prod namespace
