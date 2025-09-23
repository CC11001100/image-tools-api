#!/usr/bin/env python3
"""
生成艺术滤镜页面的OSS示例图片
修复重复路径问题，生成正确的OSS示例图片
"""

import sys
import os
import requests
import io
from PIL import Image
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.oss_client import oss_client
from app.services.filters.artistic_filters import ArtisticFilters

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"art-filter/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{file_key}"

def process_art_filter_image(image_bytes: bytes, filter_type: str, intensity: float = 1.0) -> bytes:
    """使用ArtisticFilters处理图片"""
    print(f"处理图片: {filter_type}, intensity={intensity}")
    
    return ArtisticFilters.apply_filter(
        image_bytes=image_bytes,
        filter_type=filter_type,
        intensity=intensity
    )

def main():
    """生成art-filter示例图片"""
    print("开始生成art-filter示例图片...")
    
    # 定义示例配置
    examples = [
        {
            "title": "油画效果",
            "name": "oil_painting",
            "filter_type": "oil_painting",
            "intensity": 0.8,
            "seed": "art1"
        },
        {
            "title": "轻度油画",
            "name": "oil_painting_light", 
            "filter_type": "oil_painting",
            "intensity": 0.5,
            "seed": "art2"
        },
        {
            "title": "铅笔素描",
            "name": "pencil_sketch",
            "filter_type": "pencil_sketch", 
            "intensity": 1.0,
            "seed": "art3"
        },
        {
            "title": "重度油画",
            "name": "oil_painting_heavy",
            "filter_type": "oil_painting",
            "intensity": 1.2,
            "seed": "art4"
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            print(f"下载图片: https://picsum.photos/seed/{example['seed']}/800/800")
            image_bytes = download_image(f"https://picsum.photos/seed/{example['seed']}/800/800")
            
            # 上传原图
            original_url = upload_to_oss(image_bytes, f"original-{example['name']}.jpg")
            
            # 处理艺术滤镜
            print(f"处理图片: {example['filter_type']} 滤镜")
            processed_bytes = process_art_filter_image(image_bytes, example['filter_type'], example['intensity'])
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"art-filter-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出配置更新信息
    print("\n请更新 frontend/src/config/examples/artFilterExamples.ts 中的URL:")
    for example in examples:
        original_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/original-{example['name']}.jpg"
        processed_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-filter-{example['name']}.jpg"
        print(f"  {example['title']}:")
        print(f"    originalImage: \"{original_url}\"")
        print(f"    processedImage: \"{processed_url}\"")

if __name__ == "__main__":
    main()
