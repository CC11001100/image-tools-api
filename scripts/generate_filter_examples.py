#!/usr/bin/env python3
"""
生成filter页面示例图片脚本
为filter页面生成6个不同滤镜效果的示例图片并上传到OSS
"""

import os
import sys
import requests
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.filter_service import FilterService
from app.services.oss_client import oss_client


def download_random_image(seed: int, width: int = 1080, height: int = 1920) -> bytes:
    """从picsum.photos下载随机图片"""
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}.jpg"
    print(f"下载图片: {url}")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content


def process_filter_image(image_bytes: bytes, filter_type: str, intensity: float = 1.0) -> bytes:
    """使用FilterService处理图片"""
    print(f"处理图片: {filter_type}, intensity={intensity}")
    
    return FilterService.apply_filter(
        image_bytes=image_bytes,
        filter_type=filter_type,
        intensity=intensity
    )


def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"filter/{filename}"
    print(f"上传到OSS: {file_key}")

    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{file_key}"


def main():
    """生成filter示例图片"""
    print("开始生成filter示例图片...")
    
    # 定义6个示例
    examples = [
        {
            "name": "blur",
            "filter_type": "blur",
            "intensity": 1.5,
            "seed": 2001,
            "title": "模糊效果",
            "description": "为图像添加模糊效果，可用于背景虚化或隐私保护"
        },
        {
            "name": "sharpen", 
            "filter_type": "sharpen",
            "intensity": 1.8,
            "seed": 2002,
            "title": "锐化效果",
            "description": "增强图片的细节和边缘清晰度"
        },
        {
            "name": "emboss",
            "filter_type": "emboss",
            "intensity": 1.2,
            "seed": 2003,
            "title": "浮雕效果",
            "description": "创建立体浮雕效果，突出图像轮廓"
        },
        {
            "name": "grayscale",
            "filter_type": "grayscale",
            "intensity": 1.0,
            "seed": 2004,
            "title": "灰度效果",
            "description": "将彩色图片转换为黑白灰度图"
        },
        {
            "name": "vintage",
            "filter_type": "vintage",
            "intensity": 1.3,
            "seed": 2005,
            "title": "复古效果",
            "description": "添加复古怀旧色调，营造经典氛围"
        },
        {
            "name": "brightness",
            "filter_type": "brightness",
            "intensity": 1.4,
            "seed": 2006,
            "title": "亮度调整",
            "description": "调整图片亮度，增强明暗对比效果"
        }
    ]
    
    results = []
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            original_bytes = download_random_image(example['seed'])
            
            # 上传原图
            original_filename = f"filter-original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            # 处理图片
            processed_bytes = process_filter_image(
                original_bytes, 
                example['filter_type'],
                example['intensity']
            )
            
            # 上传处理后的图片
            processed_filename = f"filter-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_filename)
            
            results.append({
                'name': example['name'],
                'title': example['title'],
                'description': example['description'],
                'filter_type': example['filter_type'],
                'intensity': example['intensity'],
                'original_url': original_url,
                'processed_url': processed_url
            })
            
            print(f"✓ 完成: {example['title']}")
            
        except Exception as e:
            print(f"✗ 处理失败: {example['title']} - {e}")
            continue
    
    # 输出结果
    print(f"\n成功生成 {len(results)} 个示例图片:")
    for result in results:
        print(f"- {result['title']}: {result['processed_url']}")
    
    print("\n所有filter示例图片生成完成！")
    return results


if __name__ == "__main__":
    main()
