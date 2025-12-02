#!/bin/bash

# SSH反向隧道配置脚本
# 将云端服务器的8008/8009端口转发到局域网K8s的30008/30009端口

set -e

echo "配置SSH反向隧道..."
echo "将云端服务器的 8008/8009 端口转发到局域网 192.168.3.42:30008/30009"

# SSH到云端服务器并设置反向隧道
ssh root@zhaixingren.cn << 'EOF'
# 检查是否已有隧道运行
pkill -f "ssh.*8008.*192.168.3.42" || true
pkill -f "ssh.*8009.*192.168.3.42" || true

# 创建systemd服务配置
cat > /etc/systemd/system/image-tools-ssh-tunnel.service << 'SERVICE'
[Unit]
Description=SSH Tunnel for Image Tools API (Local K8s)
After=network.target

[Service]
Type=simple
User=root
# 反向隧道: 云端8008 -> 局域网30008, 云端8009 -> 局域网30009
ExecStart=/usr/bin/ssh -N -T \
  -o ServerAliveInterval=60 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes \
  -R 8008:192.168.3.42:30008 \
  -R 8009:192.168.3.42:30009 \
  root@192.168.3.42

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# 重新加载systemd
systemctl daemon-reload

# 启动并启用服务
systemctl enable image-tools-ssh-tunnel.service
systemctl restart image-tools-ssh-tunnel.service

# 检查状态
systemctl status image-tools-ssh-tunnel.service --no-pager

echo "✓ SSH隧道服务已配置并启动"
echo "  云端 8008 -> 局域网 192.168.3.42:30008 (backend)"
echo "  云端 8009 -> 局域网 192.168.3.42:30009 (frontend)"
EOF

echo "✓ 配置完成！"
echo ""
echo "测试连接："
echo "  curl -I http://172.22.246.76:8008/"
echo "  curl -I http://172.22.246.76:8009/"
