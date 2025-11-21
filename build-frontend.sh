#!/bin/bash

# 前端构建脚本 - 使用 pnpm
echo "🚀 开始使用 pnpm 构建前端项目..."

# 进入前端目录
cd frontend

# 检查 pnpm 是否安装
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm 未安装，请先安装 pnpm"
    echo "安装命令: npm install -g pnpm"
    exit 1
fi

# 显示 pnpm 版本
echo "📦 pnpm 版本: $(pnpm --version)"

# 安装依赖
echo "📥 安装依赖..."
pnpm install

# 构建项目
echo "🔨 构建项目..."
pnpm run build

# 检查构建结果
if [ -d "build" ]; then
    echo "✅ 构建成功！"
    echo "📁 构建文件位置: frontend/build"
    
    # 显示构建文件大小
    echo "📊 构建文件大小:"
    du -sh build/*
else
    echo "❌ 构建失败！"
    exit 1
fi

echo "🎉 前端构建完成！"

