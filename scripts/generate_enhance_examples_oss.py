#!/usr/bin/env python3
"""
Enhance示例图片生成脚本 - OSS版本
为enhance页面生成示例图片并上传到OSS
"""

import os
import sys
import requests
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.enhance_service import EnhanceService
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

def process_enhance_image(image_bytes, effect_type, **params):
    """处理图片增强效果"""
    try:
        print(f"🎨 处理增强效果: {effect_type}, 参数: {params}")

        # 使用通用的增强方法
        from app.services.enhance.main_enhance import MainEnhance
        result_bytes = MainEnhance.apply_enhance_effect(
            image_bytes=image_bytes,
            effect_type=effect_type,
            **params
        )

        print(f"✅ 增强处理完成")
        return result_bytes
    except Exception as e:
        print(f"❌ 增强处理失败: {e}")
        return None

def generate_enhance_examples():
    """生成enhance页面的所有示例"""
    
    examples = [
        {
            'title': '锐化增强',
            'name': 'sharpen',
            'seed': 'enhance-sharpen-001',
            'effect_type': 'sharpen',
            'params': {
                'intensity': 1.5,
                'quality': 90
            }
        },
        {
            'title': '模糊效果',
            'name': 'blur',
            'seed': 'enhance-blur-002',
            'effect_type': 'blur',
            'params': {
                'intensity': 2.0,
                'quality': 90
            }
        },
        {
            'title': '细节增强',
            'name': 'detail',
            'seed': 'enhance-detail-003',
            'effect_type': 'detail',
            'params': {
                'intensity': 2.0,
                'quality': 90
            }
        },
        {
            'title': '边缘增强',
            'name': 'edge-enhance',
            'seed': 'enhance-edge-004',
            'effect_type': 'edge_enhance',
            'params': {
                'intensity': 1.5,
                'quality': 90
            }
        },
        {
            'title': '平滑处理',
            'name': 'smooth',
            'seed': 'enhance-smooth-005',
            'effect_type': 'smooth',
            'params': {
                'intensity': 2.0,
                'quality': 90
            }
        },
        {
            'title': '浮雕效果',
            'name': 'emboss',
            'seed': 'enhance-emboss-006',
            'effect_type': 'emboss',
            'params': {
                'intensity': 1.0,
                'quality': 90
            }
        }
    ]
    
    print("🚀 开始生成enhance示例图片...")
    
    for example in examples:
        print(f"\n📋 处理示例: {example['title']}")
        
        # 下载原图
        original_image_bytes = download_random_image(seed=example['seed'])
        
        # 上传原图到OSS
        original_key = f"enhance/original-{example['name']}.jpg"
        original_oss_url = upload_to_oss(original_image_bytes, original_key)

        if not original_oss_url:
            print(f"❌ 原图上传失败，跳过: {example['name']}")
            continue

        # 处理图片
        processed_image_bytes = process_enhance_image(
            original_image_bytes, 
            example['effect_type'], 
            **example['params']
        )

        if not processed_image_bytes:
            print(f"❌ 图片处理失败，跳过: {example['name']}")
            continue

        # 上传处理后的图片到OSS
        processed_key = f"enhance/enhance-{example['name']}.jpg"
        processed_oss_url = upload_to_oss(processed_image_bytes, processed_key)

        if processed_oss_url:
            print(f"✅ 示例完成: {example['title']}")
            print(f"   原图: {original_oss_url}")
            print(f"   效果图: {processed_oss_url}")
        else:
            print(f"❌ 效果图上传失败: {example['name']}")

    print("\n🎉 所有enhance示例生成完成！")

if __name__ == "__main__":
    generate_enhance_examples()
