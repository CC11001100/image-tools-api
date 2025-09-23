#!/usr/bin/env python3
"""
生成水印示例图片的脚本
从 https://picsum.photos/1080/1920 下载随机图片，
通过水印接口处理，并保存原图和效果图到 public 目录
"""

import os
import sys
import requests
import json
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.watermark_service import WatermarkService

def download_random_image(width=1080, height=1920, seed=None):
    """从 picsum.photos 下载随机图片"""
    if seed:
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    else:
        url = f"https://picsum.photos/{width}/{height}"
    
    print(f"正在下载图片: {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content

def generate_watermark_example(image_bytes, watermark_config, output_name):
    """生成水印示例"""
    print(f"正在生成水印示例: {output_name}")
    
    # 使用水印服务处理图片
    result_bytes = WatermarkService.add_watermark(
        image_bytes=image_bytes,
        text=watermark_config['text'],
        position=watermark_config.get('position', 'center'),
        opacity=watermark_config.get('opacity', 0.5),
        color=watermark_config.get('color', 'white'),
        font_size=watermark_config.get('font_size', 40),
        angle=watermark_config.get('angle', 0),
        quality=watermark_config.get('quality', 90)
    )
    
    return result_bytes

def save_image(image_bytes, file_path):
    """保存图片到指定路径"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(image_bytes)
    print(f"图片已保存: {file_path}")

def main():
    """主函数"""
    # 定义输出目录
    public_dir = project_root / "frontend" / "public" / "examples"
    watermark_dir = public_dir / "watermark"
    
    # 确保目录存在
    watermark_dir.mkdir(parents=True, exist_ok=True)
    
    # 定义水印配置
    watermark_configs = [
        {
            'name': 'watermark-example-1',
            'seed': 'watermark1',
            'text': '© 2024 Sample',
            'position': 'bottom-right',
            'font_size': 32,
            'color': '#FFFFFF',
            'opacity': 0.8,
            'angle': 0,
            'quality': 90
        },
        {
            'name': 'watermark-example-2',
            'seed': 'watermark2',
            'text': 'SAMPLE',
            'position': 'center',
            'font_size': 72,
            'color': '#FFFFFF',
            'opacity': 0.6,
            'angle': -30,
            'quality': 90
        },
        {
            'name': 'watermark-example-3',
            'seed': 'watermark3',
            'text': 'WATERMARK',
            'position': 'top-left',
            'font_size': 24,
            'color': '#000000',
            'opacity': 0.7,
            'angle': 0,
            'quality': 90
        },
        {
            'name': 'watermark-example-4',
            'seed': 'watermark4',
            'text': 'BRAND',
            'position': 'center',
            'font_size': 80,
            'color': '#FF0000',
            'opacity': 0.3,
            'angle': 0,
            'quality': 90
        },
        {
            'name': 'watermark-example-5',
            'seed': 'watermark5',
            'text': 'www.example.com',
            'position': 'bottom-left',
            'font_size': 20,
            'color': '#FFFFFF',
            'opacity': 0.9,
            'angle': 0,
            'quality': 90
        },
        {
            'name': 'watermark-example-6',
            'seed': 'watermark6',
            'text': '2024-07-04',
            'position': 'top-right',
            'font_size': 18,
            'color': '#000000',
            'opacity': 0.8,
            'angle': 0,
            'quality': 90
        },
        {
            'name': 'watermark-example-7',
            'seed': 'watermark7',
            'text': 'CONFIDENTIAL',
            'position': 'center',
            'font_size': 60,
            'color': '#FF0000',
            'opacity': 0.2,
            'angle': 45,
            'quality': 90
        },
        {
            'name': 'watermark-example-8',
            'seed': 'watermark8',
            'text': '© Photo Studio',
            'position': 'center',
            'font_size': 30,
            'color': '#FFD700',
            'opacity': 0.7,
            'angle': 0,
            'quality': 90
        },
        {
            'name': 'watermark-example-9',
            'seed': 'watermark9',
            'text': 'DRAFT',
            'position': 'top-left',
            'font_size': 48,
            'color': '#FFA500',
            'opacity': 0.6,
            'angle': -15,
            'quality': 90
        },
        {
            'name': 'watermark-example-10',
            'seed': 'watermark10',
            'text': 'PREMIUM',
            'position': 'top-right',
            'font_size': 42,
            'color': '#800080',
            'opacity': 0.4,
            'angle': 90,
            'quality': 90
        }
    ]
    
    # 生成原图
    original_images = [
        {'name': 'original-landscape', 'seed': 'landscape1', 'width': 1920, 'height': 1080},
        {'name': 'original-nature', 'seed': 'nature1', 'width': 1920, 'height': 1080},
        {'name': 'sample-image-1', 'seed': 'sample1', 'width': 1080, 'height': 1920},
        {'name': 'sample-image-2', 'seed': 'sample2', 'width': 1080, 'height': 1920},
        {'name': 'sample-image-3', 'seed': 'sample3', 'width': 1080, 'height': 1920}
    ]
    
    print("开始生成原图...")
    for img_config in original_images:
        try:
            # 下载原图
            image_bytes = download_random_image(
                width=img_config['width'], 
                height=img_config['height'], 
                seed=img_config['seed']
            )
            
            # 保存原图
            original_path = public_dir / f"{img_config['name']}.jpg"
            save_image(image_bytes, original_path)
            
            time.sleep(1)  # 避免请求过于频繁
            
        except Exception as e:
            print(f"生成原图 {img_config['name']} 失败: {e}")
    
    print("\n开始生成水印示例...")
    for config in watermark_configs:
        try:
            # 下载随机图片
            image_bytes = download_random_image(seed=config['seed'])
            
            # 生成水印效果图
            watermarked_bytes = generate_watermark_example(image_bytes, config, config['name'])
            
            # 保存水印效果图
            watermark_path = watermark_dir / f"{config['name']}.jpg"
            save_image(watermarked_bytes, watermark_path)
            
            time.sleep(1)  # 避免请求过于频繁
            
        except Exception as e:
            print(f"生成水印示例 {config['name']} 失败: {e}")
    
    print("\n所有水印示例生成完成！")

if __name__ == "__main__":
    main()
