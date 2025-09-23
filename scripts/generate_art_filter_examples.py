#!/usr/bin/env python3
"""
生成艺术滤镜示例图片脚本
为art-filter页面生成OSS示例图片
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

from app.filters.oil_painting import apply_oil_painting
from app.filters.watercolor import apply_watercolor
from app.filters.pencil_sketch import apply_pencil_sketch
from app.filters.colored_pencil import apply_colored_pencil
from app.services.oss_client import oss_client


def download_random_image(seed: int, width: int = 1080, height: int = 1920) -> bytes:
    """下载随机图片"""
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    print(f"下载图片: {url}")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content


def process_art_filter_image(image_bytes: bytes, filter_type: str, intensity: float = 1.0) -> bytes:
    """使用艺术滤镜处理图片"""
    print(f"处理图片: {filter_type}, intensity={intensity}")
    
    if filter_type == "oil_painting":
        return apply_oil_painting(
            image_bytes=image_bytes,
            radius=5,
            intensity=intensity * 10.0  # 转换intensity范围
        )
    elif filter_type == "watercolor":
        return apply_watercolor(
            image_bytes=image_bytes,
            sigma_s=60,
            sigma_r=0.6,
            texture_strength=0.1,
            intensity=intensity
        )
    elif filter_type == "pencil_sketch":
        return apply_pencil_sketch(
            image_bytes=image_bytes,
            sigma_s=60,
            sigma_r=0.07,
            shade_factor=0.1,
            intensity=intensity
        )
    elif filter_type == "colored_pencil":
        return apply_colored_pencil(
            image_bytes=image_bytes,
            line_size=7,
            blur_value=7,
            edge_threshold=50,
            texture_strength=0.1,
            intensity=intensity
        )
    else:
        raise ValueError(f"不支持的滤镜类型: {filter_type}")


def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"image-tools-api/examples/art-filter/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/{file_key}"


def main():
    """生成艺术滤镜示例图片"""
    print("开始生成艺术滤镜示例图片...")
    
    # 定义4个示例（使用稳定的滤镜）
    examples = [
        {
            "name": "oil_painting",
            "filter_type": "oil_painting",
            "intensity": 0.8,
            "seed": 3001,
            "title": "油画效果",
            "description": "将图片转换为油画风格，呈现厚重的笔触和丰富的色彩层次"
        },
        {
            "name": "oil_painting_light",
            "filter_type": "oil_painting",
            "intensity": 0.5,
            "seed": 3002,
            "title": "轻度油画",
            "description": "轻度油画效果，保留更多原图细节的同时增加艺术感"
        },
        {
            "name": "pencil_sketch",
            "filter_type": "pencil_sketch",
            "intensity": 1.0,
            "seed": 3003,
            "title": "铅笔素描",
            "description": "将图片转换为铅笔素描风格，突出线条和明暗对比"
        },
        {
            "name": "oil_painting_heavy",
            "filter_type": "oil_painting",
            "intensity": 1.2,
            "seed": 3004,
            "title": "重度油画",
            "description": "强烈的油画效果，色彩浓郁，笔触明显"
        }
    ]
    
    results = []
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            original_bytes = download_random_image(example['seed'])
            
            # 上传原图
            original_filename = f"original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            # 处理图片
            processed_bytes = process_art_filter_image(
                original_bytes, 
                example['filter_type'],
                example['intensity']
            )
            
            # 上传处理后的图片
            processed_filename = f"art-filter-{example['name']}.jpg"
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
            
            print(f"✅ 成功生成: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败 {example['title']}: {str(e)}")
            continue
    
    # 输出结果
    print(f"\n🎉 艺术滤镜示例生成完成!")
    print(f"成功生成: {len(results)}/{len(examples)} 个示例")
    
    for result in results:
        print(f"\n📸 {result['title']}:")
        print(f"   原图: {result['original_url']}")
        print(f"   效果图: {result['processed_url']}")
    
    return results


if __name__ == "__main__":
    main()
