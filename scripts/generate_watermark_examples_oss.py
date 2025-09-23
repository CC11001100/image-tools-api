#!/usr/bin/env python3
"""
Watermark示例图片生成脚本 - OSS版本
为watermark页面生成示例图片并上传到OSS
"""

import os
import sys
import requests
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.watermark_service import WatermarkService
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

def process_watermark_image(image_bytes, text, position="center", font_size=40, color="#FFFFFF", opacity=0.8, angle=0, quality=90):
    """处理图片添加水印效果"""
    try:
        print(f"🎨 处理水印效果: {text}, 位置: {position}, 透明度: {opacity}")
        result_bytes = WatermarkService.add_watermark(
            image_bytes=image_bytes,
            text=text,
            position=position,
            opacity=opacity,
            color=color,
            font_size=font_size,
            angle=angle,
            quality=quality
        )
        print(f"✅ 水印处理完成")
        return result_bytes
    except Exception as e:
        print(f"❌ 水印处理失败: {e}")
        return None

def generate_watermark_examples():
    """生成watermark页面的所有示例"""
    
    examples = [
        {
            'title': '中心文字水印',
            'name': 'center-text',
            'seed': 'watermark-center-001',
            'params': {
                'text': 'SAMPLE',
                'position': 'center',
                'font_size': 48,
                'color': '#FFFFFF',
                'opacity': 0.8,
                'angle': 0,
                'quality': 90
            }
        },
        {
            'title': '右下角版权水印',
            'name': 'bottom-right',
            'seed': 'watermark-copyright-002',
            'params': {
                'text': '© 2024',
                'position': 'bottom-right',
                'font_size': 32,
                'color': '#FFFFFF',
                'opacity': 0.7,
                'angle': 0,
                'quality': 90
            }
        },
        {
            'title': '对角线水印',
            'name': 'diagonal',
            'seed': 'watermark-diagonal-003',
            'params': {
                'text': 'WATERMARK',
                'position': 'center',
                'font_size': 60,
                'color': '#FFFFFF',
                'opacity': 0.5,
                'angle': -30,
                'quality': 90
            }
        },
        {
            'title': '左上角标识',
            'name': 'top-left',
            'seed': 'watermark-brand-004',
            'params': {
                'text': 'BRAND',
                'position': 'top-left',
                'font_size': 36,
                'color': '#000000',
                'opacity': 0.9,
                'angle': 0,
                'quality': 90
            }
        },
        {
            'title': '透明水印',
            'name': 'transparent',
            'seed': 'watermark-transparent-005',
            'params': {
                'text': 'CONFIDENTIAL',
                'position': 'center',
                'font_size': 80,
                'color': '#FF0000',
                'opacity': 0.3,
                'angle': 45,
                'quality': 90
            }
        },
        {
            'title': '网站水印',
            'name': 'website',
            'seed': 'watermark-website-006',
            'params': {
                'text': 'www.example.com',
                'position': 'bottom-left',
                'font_size': 28,
                'color': '#FFFFFF',
                'opacity': 0.8,
                'angle': 0,
                'quality': 90
            }
        }
    ]
    
    print("🚀 开始生成watermark示例图片...")
    
    for example in examples:
        print(f"\n📋 处理示例: {example['title']}")
        
        # 下载原图
        original_image_bytes = download_random_image(seed=example['seed'])
        
        # 上传原图到OSS
        original_key = f"watermark/original-{example['name']}.jpg"
        original_oss_url = upload_to_oss(original_image_bytes, original_key)

        if not original_oss_url:
            print(f"❌ 原图上传失败，跳过: {example['name']}")
            continue

        # 处理图片
        processed_image_bytes = process_watermark_image(original_image_bytes, **example['params'])

        if not processed_image_bytes:
            print(f"❌ 图片处理失败，跳过: {example['name']}")
            continue

        # 上传处理后的图片到OSS
        processed_key = f"watermark/watermark-{example['name']}.jpg"
        processed_oss_url = upload_to_oss(processed_image_bytes, processed_key)

        if processed_oss_url:
            print(f"✅ 示例完成: {example['title']}")
            print(f"   原图: {original_oss_url}")
            print(f"   效果图: {processed_oss_url}")
        else:
            print(f"❌ 效果图上传失败: {example['name']}")

    print("\n🎉 所有watermark示例生成完成！")

if __name__ == "__main__":
    generate_watermark_examples()
