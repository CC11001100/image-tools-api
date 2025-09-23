#!/usr/bin/env python3
"""
生成transform页面示例图片脚本
为transform页面生成6个不同变换效果的示例图片并上传到OSS
"""

import os
import sys
import requests
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.transform_service import TransformService
from app.services.oss_client import oss_client


def download_random_image(seed: int, width: int = 1080, height: int = 1920) -> bytes:
    """从picsum.photos下载随机图片"""
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}.jpg"
    print(f"下载图片: {url}")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content


def process_transform_image(image_bytes: bytes, transform_type: str, angle: float = 0) -> bytes:
    """使用TransformService处理图片"""
    print(f"处理图片: {transform_type}, angle={angle}")
    
    return TransformService.transform_image(
        image_bytes=image_bytes,
        transform_type=transform_type,
        angle=angle,
        quality=90
    )


def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"transform/{filename}"
    print(f"上传到OSS: {file_key}")

    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{file_key}"


def main():
    """生成transform示例图片"""
    print("开始生成transform示例图片...")
    
    # 定义6个示例
    examples = [
        {
            "name": "flip-horizontal",
            "transform_type": "flip-horizontal",
            "angle": 0,
            "seed": 1001,
            "title": "水平翻转",
            "description": "将图片水平翻转，创建镜像效果"
        },
        {
            "name": "flip-vertical", 
            "transform_type": "flip-vertical",
            "angle": 0,
            "seed": 1002,
            "title": "垂直翻转",
            "description": "将图片垂直翻转，上下颠倒"
        },
        {
            "name": "rotate-90-cw",
            "transform_type": "rotate-90-cw", 
            "angle": 0,
            "seed": 1003,
            "title": "顺时针旋转90°",
            "description": "将图片顺时针旋转90度"
        },
        {
            "name": "rotate-180",
            "transform_type": "rotate-180",
            "angle": 0, 
            "seed": 1004,
            "title": "旋转180°",
            "description": "将图片旋转180度，完全倒置"
        },
        {
            "name": "rotate-270",
            "transform_type": "rotate-90-ccw",
            "angle": 0,
            "seed": 1005, 
            "title": "逆时针旋转90°",
            "description": "将图片逆时针旋转90度"
        },
        {
            "name": "rotate-45",
            "transform_type": "rotate",
            "angle": 45,
            "seed": 1006,
            "title": "自定义角度旋转 - 45°",
            "description": "将图像旋转45度，创造动感效果"
        }
    ]
    
    results = []
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            original_bytes = download_random_image(example['seed'])
            
            # 上传原图
            original_filename = f"transform-original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            # 处理图片
            processed_bytes = process_transform_image(
                original_bytes, 
                example['transform_type'],
                example['angle']
            )
            
            # 上传处理后的图片
            processed_filename = f"transform-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_filename)
            
            results.append({
                'name': example['name'],
                'title': example['title'],
                'description': example['description'],
                'transform_type': example['transform_type'],
                'angle': example['angle'],
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
    
    print("\n所有transform示例图片生成完成！")
    return results


if __name__ == "__main__":
    main()
