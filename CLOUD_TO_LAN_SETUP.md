# 云端到局域网路由配置方案

## 当前情况

### ✅ 已完成
1. 局域网K8s集群部署成功（192.168.3.42）
   - Frontend: 正常运行
   - Backend: 正常运行
   - Ingress: 正常配置
   - 通过IP可以访问: `https://192.168.3.42/`

2. 云端K8s集群已有资源（198.18.0.75）
   - Backend: 运行中（但是旧版本）
   - Frontend: 运行中（Nginx配置有Bug）

### ❌ 问题
- 云端K8s集群无法直接访问局域网IP（192.168.3.42）
- 测试显示：`502 Bad Gateway`
- 原因：云端服务器和局域网之间没有网络连接

## 解决方案选择

### 方案A：FRP内网穿透（推荐） ⭐

**优点**:
- 无需修改DNS
- 保持域名从云端路由
- 安全可靠
- 易于管理

**步骤**:

1. 在云端部署frps服务端
2. 在局域网部署frpc客户端
3. frpc将局域网的443端口映射到云端
4. 云端Ingress转发到frps

**配置文件**:
```bash
# 1. 云端部署frps
kubectl apply -f k8s-cloud-proxy/frps-deployment.yml

# 2. 局域网部署frpc
kubectl --context=k3s-local apply -f k8s-cloud-proxy/frpc-deployment.yml

# 3. 云端配置Ingress指向frps
kubectl apply -f k8s-cloud-proxy/frps-ingress.yml
```

### 方案B：修改DNS解析（最简单） 🚀

**优点**:
- 最简单
- 不需要任何代理
- 性能最好

**缺点**:
- 需要修改DNS
- 局域网需要有公网可访问的方式

**步骤**:
```bash
# 1. 确认局域网是否可以从公网访问
curl -k https://YOUR_PUBLIC_IP/

# 2. 修改DNS A记录
origin-image-tools.aigchub.vip -> YOUR_PUBLIC_IP
image-tools.aigchub.vip -> YOUR_PUBLIC_IP

# 3. 等待DNS生效（5-30分钟）

# 4. 测试
curl -k https://origin-image-tools.aigchub.vip/
```

### 方案C：端口转发 + Ingress

如果你的局域网路由器支持端口转发：

**步骤**:
1. 在路由器上配置端口转发：`公网IP:443 -> 192.168.3.42:443`
2. 修改DNS指向公网IP
3. 完成！

### 方案D：Cloudflare Tunnel（推荐用于生产）

使用Cloudflare Tunnel连接局域网到云端：

**优点**:
- 无需公网IP
- 免费
- 自动HTTPS
- DDoS防护

**步骤**:
```bash
# 1. 在局域网部署Cloudflare Tunnel
kubectl --context=k3s-local apply -f k8s-cloud-proxy/cloudflared-deployment.yml

# 2. 配置Cloudflare DNS指向tunnel
# 3. 完成！
```

## 临时方案：修复云端Frontend

如果只是想快速让服务可用，可以：

```bash
# 1. 修复云端frontend的Nginx配置
kubectl --context=k3s-local exec -n aigchub-prod image-tools-api-frontend-f58c54d8-6b9zb -- \
  cat /etc/nginx/conf.d/default.conf > /tmp/fixed-nginx.conf

# 编辑修复配置

# 2. 重新构建镜像
cd frontend
docker build -t docker.zhaixingren.cn/aigchub/image-tools-api-frontend:latest .
docker push docker.zhaixingren.cn/aigchub/image-tools-api-frontend:latest

# 3. 云端重启
kubectl rollout restart deployment/image-tools-api-frontend -n aigchub-prod

# 4. 恢复云端Ingress
kubectl apply -f k8s/ingress.yml
```

## 我的建议

根据你的实际情况：

### 如果局域网有公网IP或端口转发
→ **使用方案B（修改DNS）**
- 最简单
- 不需要任何额外配置

### 如果局域网没有公网IP
→ **使用方案A（FRP）或方案D（Cloudflare Tunnel）**
- FRP: 自己控制，更灵活
- Cloudflare: 免费，功能强大

### 如果只是临时测试
→ **使用临时方案**
- 修复云端frontend
- 快速恢复服务

## 下一步操作

请告诉我你的网络情况：

1. **局域网192.168.3.42是否有公网IP？**
2. **路由器是否支持端口转发？**
3. **是否希望使用第三方服务（如Cloudflare）？**

我会根据你的回答提供具体的配置命令。

## 已创建的文件

- `k8s-cloud-proxy/lan-proxy-service.yml` - Service配置（待用）
- `k8s-cloud-proxy/lan-proxy-ingressroute.yml` - Ingress配置（待用）
- `k8s-cloud-proxy/README.md` - 详细说明文档
- `CLOUD_TO_LAN_SETUP.md` - 本文件

## 当前配置状态

### 云端（198.18.0.75）
- ✅ Service: `image-tools-lan-proxy` (指向192.168.3.42:443)
- ✅ ServersTransport: `lan-transport` (跳过SSL验证)
- ❌ Ingress: 已删除（等待网络方案确定）
- ⚠️  Frontend Pod: 运行中但Nginx配置有问题
- ✅ Backend Pod: 运行中

### 局域网（192.168.3.42）
- ✅ Frontend: 完全正常
- ✅ Backend: 完全正常  
- ✅ Ingress: 配置正确
- ✅ 通过IP访问: 成功

## 测试命令

### 测试局域网服务
```bash
# 通过IP直接访问（成功）
curl -k --resolve origin-image-tools.aigchub.vip:443:192.168.3.42 \
  https://origin-image-tools.aigchub.vip/

# 通过域名访问（需要配置后才能成功）
curl -k https://origin-image-tools.aigchub.vip/
```

### 测试云端到局域网连通性
```bash
# 从云端Pod测试
kubectl run test --rm -i --image=curlimages/curl -- \
  curl -k -m 5 https://192.168.3.42/
```

---

**等待你的反馈，我会立即配置对应的方案！** 🚀
