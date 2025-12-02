# 云端到局域网代理配置说明

## 问题分析

云端K8s集群（198.18.0.75）无法直接访问局域网K8s集群（192.168.3.42），因为两者之间没有网络连接。

## 当前状态

- ✅ 局域网K8s集群部署完成（192.168.3.42）
  - Frontend: 正常运行
  - Backend: 正常运行
  - 通过局域网IP可以正常访问

- ❌ 云端K8s集群无法代理到局域网
  - 网络不可达（测试显示502 Bad Gateway）
  - 需要额外的网络连接方案

## 解决方案

### 方案1：使用FRP内网穿透（推荐）

在局域网服务器上部署frp客户端，连接到云端的frp服务端，建立反向隧道。

#### 云端部署frp服务端

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: frps-config
  namespace: aigchub-prod
data:
  frps.ini: |
    [common]
    bind_port = 7000
    vhost_http_port = 8080
    vhost_https_port = 8443
    token = YOUR_SECRET_TOKEN

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frps
  namespace: aigchub-prod
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frps
  template:
    metadata:
      labels:
        app: frps
    spec:
      containers:
      - name: frps
        image: snowdreamtech/frps:latest
        ports:
        - containerPort: 7000
        - containerPort: 8080
        - containerPort: 8443
        volumeMounts:
        - name: config
          mountPath: /etc/frp
      volumes:
      - name: config
        configMap:
          name: frps-config

---
apiVersion: v1
kind: Service
metadata:
  name: frps
  namespace: aigchub-prod
spec:
  type: LoadBalancer
  ports:
  - name: control
    port: 7000
    targetPort: 7000
  - name: http
    port: 8080
    targetPort: 8080
  - name: https
    port: 8443
    targetPort: 8443
  selector:
    app: frps
```

#### 局域网部署frp客户端

```bash
# 在局域网K8s集群部署frpc
kubectl --context=k3s-local apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: frpc-config
  namespace: aigchub-prod
data:
  frpc.ini: |
    [common]
    server_addr = 198.18.0.75
    server_port = 7000
    token = YOUR_SECRET_TOKEN
    
    [image-tools-https]
    type = https
    local_ip = 192.168.3.42
    local_port = 443
    custom_domains = origin-image-tools.aigchub.vip,image-tools.aigchub.vip

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frpc
  namespace: aigchub-prod
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frpc
  template:
    metadata:
      labels:
        app: frpc
    spec:
      containers:
      - name: frpc
        image: snowdreamtech/frpc:latest
        volumeMounts:
        - name: config
          mountPath: /etc/frp
      volumes:
      - name: config
        configMap:
          name: frpc-config
EOF
```

### 方案2：使用WireGuard VPN

在云端和局域网之间建立VPN连接，使两个K8s集群可以互相访问。

### 方案3：仅在云端部署Frontend（临时方案）

保持云端的frontend部署，修复nginx配置，让frontend连接到云端的backend（已经在运行）。

```bash
# 重新构建frontend镜像（修复nginx配置）
cd frontend
docker build -t docker.zhaixingren.cn/aigchub/image-tools-api-frontend:latest .
docker push docker.zhaixingren.cn/aigchub/image-tools-api-frontend:latest

# 重启pod
kubectl rollout restart deployment/image-tools-api-frontend -n aigchub-prod
```

### 方案4：修改DNS直接指向局域网

如果局域网有公网IP或者通过路由器端口转发可以从公网访问，直接修改DNS：

```
origin-image-tools.aigchub.vip -> 局域网公网IP
```

## 当前配置文件

- `lan-proxy-service.yml` - Service + Endpoints指向192.168.3.42
- `lan-proxy-ingressroute.yml` - Ingress配置（当前无法工作）

## 建议

根据实际网络情况选择方案：

1. **如果需要保持域名从云端路由**: 使用方案1（FRP）或方案2（WireGuard）
2. **如果可以修改DNS**: 使用方案4，最简单
3. **临时解决方案**: 使用方案3，修复云端frontend
