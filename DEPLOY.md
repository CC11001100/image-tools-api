# Image Tools API 部署指南

## 部署环境

本项目支持两套部署环境：

### 1. 云服务器 K8s 集群（原有）
- **服务器**: 8.130.35.126
- **镜像仓库**: docker.zhaixingren.cn
- **配置目录**: `k8s/`
- **部署脚本**: `deploy-prod.sh`
- **部署命令**: `kubectl`

### 2. 局域网 K8s 集群（新增）⭐
- **服务器**: 192.168.3.42
- **镜像仓库**: 192.168.3.42:5000
- **配置目录**: `k8s-local/`
- **部署脚本**: `deploy-local.sh`
- **部署命令**: `kubectl-local`

## 部署到局域网集群

### 前置条件

1. 确保 Docker 已安装并登录到局域网镜像仓库：
   ```bash
   docker login 192.168.3.42:5000
   ```

2. 确保 `kubectl-local` 命令已配置并可以访问局域网集群：
   ```bash
   kubectl-local get nodes
   ```

### 部署步骤

执行局域网部署脚本：

```bash
./deploy-local.sh
```

该脚本会自动完成以下操作：
1. 清理旧镜像
2. 构建前端代码
3. 构建后端镜像（AMD64架构）
4. 推送后端镜像到 192.168.3.42:5000
5. 构建前端镜像（AMD64架构）
6. 推送前端镜像到 192.168.3.42:5000
7. 使用 kubectl-local 部署到局域网 K8s 集群
8. 等待服务就绪
9. 显示部署状态

### 访问地址

部署成功后，可以通过以下域名访问（域名由云服务器路由到局域网集群）：

- https://origin-image-tools.aigchub.vip
- https://image-tools.aigchub.vip

## 部署到云服务器集群（原有）

如果需要部署到云服务器集群，使用原有脚本：

```bash
./deploy-prod.sh
```

## 查看日志

### 局域网集群

```bash
# 查看后端日志
kubectl-local logs -n aigchub-prod -l app=image-tools-api-backend --tail=100 -f

# 查看前端日志
kubectl-local logs -n aigchub-prod -l app=image-tools-api-frontend --tail=100 -f
```

### 云服务器集群

```bash
# SSH到服务器后查看后端日志
ssh root@8.130.35.126
kubectl logs -n aigchub-prod -l app=image-tools-api-backend --tail=100 -f
```

## 查看资源使用情况

### 局域网集群

```bash
kubectl-local top pods -n aigchub-prod | grep image-tools-api
```

### 云服务器集群

```bash
ssh root@8.130.35.126 'kubectl top pods -n aigchub-prod | grep image-tools-api'
```

## 配置差异

| 配置项 | 云服务器集群 | 局域网集群 |
|--------|-------------|-----------|
| 镜像仓库 | docker.zhaixingren.cn | 192.168.3.42:5000 |
| K8s配置目录 | k8s/ | k8s-local/ |
| 部署脚本 | deploy-prod.sh | deploy-local.sh |
| kubectl命令 | kubectl (SSH到服务器) | kubectl-local |
| hostNetwork | 是 | 是 |
| Ingress | Traefik + TLS | Traefik + TLS |
| namespace | aigchub-prod | aigchub-prod |

## 架构说明

两套集群的架构是相同的：

```
Internet
    ↓
Domain (aigchub.vip)
    ↓
云服务器 K8s Ingress (路由到局域网)
    ↓
局域网 K8s Cluster (192.168.3.42)
    ↓
Traefik Ingress Controller
    ↓
Service → Pods
```

**域名路由说明**：
- 域名仍然在云服务器的 K8s 集群上配置
- 云服务器的 Ingress 将流量路由到局域网集群
- 实际服务运行在局域网集群上

## 故障排查

### 镜像推送失败

检查是否已登录到镜像仓库：
```bash
docker login 192.168.3.42:5000
```

### kubectl-local 命令不存在

检查 kubectl-local 是否已配置：
```bash
which kubectl-local
```

### 部署超时

检查局域网集群节点状态：
```bash
kubectl-local get nodes
kubectl-local get pods -n aigchub-prod
```

### 服务无法访问

1. 检查 Pod 状态：
   ```bash
   kubectl-local get pods -n aigchub-prod | grep image-tools-api
   ```

2. 检查 Service：
   ```bash
   kubectl-local get svc -n aigchub-prod | grep image-tools-api
   ```

3. 检查 Ingress：
   ```bash
   kubectl-local get ingress -n aigchub-prod | grep image-tools-api
   ```

4. 查看 Pod 日志：
   ```bash
   kubectl-local logs -n aigchub-prod -l app=image-tools-api-backend --tail=50
   ```
