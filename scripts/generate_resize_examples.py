#!/usr/bin/env python3
"""
生成resize页面示例图片脚本
为resize页面生成6个高质量示例图片并上传到OSS
"""

import os
import sys
import requests
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.resize_service import ResizeService
from app.services.oss_client import oss_client

def download_random_image(seed: str, width: int = 1080, height: int = 1920) -> bytes:
    """下载随机图片"""
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    print(f"📥 下载图片: {url}")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.content


def process_resize_image(image_bytes: bytes, **params) -> bytes:
    """处理resize图片"""
    print(f"🎨 处理resize效果: {params}")

    try:
        result = ResizeService.resize_image(image_bytes, **params)
        print("✅ resize处理完成")
        return result
    except Exception as e:
        print(f"❌ resize处理失败: {e}")
        return None


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

def main():
    """主函数"""
    print("🚀 开始生成resize示例图片...")

    # 定义示例配置
    examples = [
        {
            'name': 'resize-800px',
            'description': '等比缩放 - 800px宽度',
            'seed': 'resize-800-001',
            'params': {
                'width': 800,
                'maintain_ratio': True,
                'quality': 90
            }
        },
        {
            'name': 'resize-600px',
            'description': '等比缩放 - 600px宽度',
            'seed': 'resize-600-002',
            'params': {
                'width': 600,
                'maintain_ratio': True,
                'quality': 90
            }
        },
        {
            'name': 'resize-400px',
            'description': '等比缩放 - 400px宽度',
            'seed': 'resize-400-003',
            'params': {
                'width': 400,
                'maintain_ratio': True,
                'quality': 90
            }
        },
        {
            'name': 'resize-fixed-400x300',
            'description': '固定尺寸 - 400x300',
            'seed': 'resize-fixed-004',
            'params': {
                'width': 400,
                'height': 300,
                'maintain_ratio': False,
                'quality': 90
            }
        },
        {
            'name': 'resize-1000px',
            'description': '等比缩放 - 1000px宽度',
            'seed': 'resize-1000-005',
            'params': {
                'width': 1000,
                'maintain_ratio': True,
                'quality': 90
            }
        },
        {
            'name': 'resize-hq-600px',
            'description': '高质量缩放 - 600px宽度',
            'seed': 'resize-hq-006',
            'params': {
                'width': 600,
                'maintain_ratio': True,
                'quality': 100
            }
        }
    ]

    # 处理每个示例
    for example in examples:
        print(f"\n📋 处理示例: {example['description']}")

        # 下载原图
        original_image_bytes = download_random_image(example['seed'])

        # 上传原图到OSS
        original_key = f"resize/resize-original-{example['name']}.jpg"
        original_oss_url = upload_to_oss(original_image_bytes, original_key)

        if not original_oss_url:
            print(f"❌ 原图上传失败，跳过: {example['name']}")
            continue

        # 处理图片
        processed_image_bytes = process_resize_image(original_image_bytes, **example['params'])

        if not processed_image_bytes:
            print(f"❌ 图片处理失败，跳过: {example['name']}")
            continue

        # 上传处理后的图片到OSS
        processed_key = f"resize/{example['name']}.jpg"
        processed_oss_url = upload_to_oss(processed_image_bytes, processed_key)

        if processed_oss_url:
            print(f"✅ 示例完成: {example['description']}")
            print(f"   原图: {original_oss_url}")
            print(f"   效果图: {processed_oss_url}")
        else:
            print(f"❌ 效果图上传失败: {example['name']}")

    print("\n🎉 所有resize示例生成完成！")

if __name__ == "__main__":
    main()
