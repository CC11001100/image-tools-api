#!/usr/bin/env python3
"""
Canvas示例图片生成脚本
为canvas页面生成示例图片并上传到OSS
"""

import os
import sys
import requests
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.canvas_service import CanvasService
from app.services.oss_client import oss_client

def download_random_image(width=1080, height=1920, seed=None):
    """从picsum.photos下载指定尺寸的随机图片"""
    if seed:
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    else:
        url = f"https://picsum.photos/{width}/{height}"
    
    print(f"📥 下载图片: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes, file_key):
    """上传图片到OSS"""
    try:
        print(f"📤 上传到OSS: {file_key}")
        oss_url = oss_client.upload_bytes(image_bytes, file_key)
        if oss_url:
            print(f"✅ 上传成功: {oss_url}")
            return oss_url
        else:
            print(f"❌ 上传失败: {file_key}")
            return None
    except Exception as e:
        print(f"❌ 上传失败: {file_key} - {e}")
        return None

def process_canvas_image(image_bytes, canvas_type="border", border_width=2, border_color="#000000", background_color="#FFFFFF", padding=0, quality=90):
    """处理图片添加画布效果"""
    try:
        print(f"🎨 处理画布效果: {canvas_type}, 边框宽度: {border_width}, 颜色: {border_color}")
        result_bytes = CanvasService.process_canvas(
            image_bytes=image_bytes,
            canvas_type=canvas_type,
            border_width=border_width,
            border_color=border_color,
            background_color=background_color,
            padding=padding,
            quality=quality
        )
        print(f"✅ 画布处理完成")
        return result_bytes
    except Exception as e:
        print(f"❌ 画布处理失败: {e}")
        return None

def generate_canvas_examples():
    """生成canvas页面的所有示例"""
    
    # 定义示例配置
    examples = [
        {
            "name": "solid-border",
            "title": "简单实线边框",
            "seed": "canvas-solid-001",
            "params": {
                "canvas_type": "border",
                "border_width": 2,
                "border_color": "#000000",
                "background_color": "#FFFFFF",
                "quality": 90
            }
        },
        {
            "name": "fancy-dashed",
            "title": "花式虚线边框", 
            "seed": "canvas-dashed-002",
            "params": {
                "canvas_type": "border",
                "border_width": 3,
                "border_color": "#FF5733",
                "background_color": "#FFFFFF",
                "quality": 90
            }
        },
        {
            "name": "modern-dotted",
            "title": "现代点线边框",
            "seed": "canvas-dotted-003", 
            "params": {
                "canvas_type": "border",
                "border_width": 2,
                "border_color": "#3498DB",
                "background_color": "#FFFFFF",
                "quality": 90
            }
        },
        {
            "name": "classic-double",
            "title": "经典双线边框",
            "seed": "canvas-double-004",
            "params": {
                "canvas_type": "border", 
                "border_width": 4,
                "border_color": "#2C3E50",
                "background_color": "#FFFFFF",
                "quality": 90
            }
        },
        {
            "name": "padding-expand",
            "title": "画布扩展",
            "seed": "canvas-expand-005",
            "params": {
                "canvas_type": "expand",
                "padding": 20,
                "background_color": "#F8F9FA",
                "quality": 90
            }
        },
        {
            "name": "background-fill",
            "title": "背景填充",
            "seed": "canvas-fill-006",
            "params": {
                "canvas_type": "padding",
                "padding": 15,
                "background_color": "#E8F4FD",
                "quality": 90
            }
        }
    ]
    
    print("🚀 开始生成canvas示例图片...")
    
    for example in examples:
        print(f"\n📋 处理示例: {example['title']}")
        
        # 下载原图
        original_image_bytes = download_random_image(seed=example['seed'])
        
        # 上传原图到OSS
        original_key = f"canvas/canvas-original-{example['name']}.jpg"
        original_oss_url = upload_to_oss(original_image_bytes, original_key)

        if not original_oss_url:
            print(f"❌ 原图上传失败，跳过: {example['name']}")
            continue

        # 处理图片
        processed_image_bytes = process_canvas_image(original_image_bytes, **example['params'])

        if not processed_image_bytes:
            print(f"❌ 图片处理失败，跳过: {example['name']}")
            continue

        # 上传处理后的图片到OSS
        processed_key = f"canvas/{example['name']}.jpg"
        processed_oss_url = upload_to_oss(processed_image_bytes, processed_key)
        
        if processed_oss_url:
            print(f"✅ 示例完成: {example['title']}")
            print(f"   原图: {original_oss_url}")
            print(f"   效果图: {processed_oss_url}")
        else:
            print(f"❌ 效果图上传失败: {example['name']}")
    
    print("\n🎉 所有canvas示例生成完成！")

if __name__ == "__main__":
    generate_canvas_examples()
