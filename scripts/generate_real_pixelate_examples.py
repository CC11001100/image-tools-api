#!/usr/bin/env python3
"""
生成真实的像素化效果示例图片
使用PixelateService生成实际的像素化效果
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
from app.services.pixelate_service import PixelateService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"pixelate/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{file_key}"

def process_pixelate_image(image_bytes: bytes, pixel_size: int) -> bytes:
    """使用PixelateService处理图片"""
    print(f"处理图片: 像素大小={pixel_size}")
    
    return PixelateService.pixelate_full(
        image_bytes=image_bytes,
        pixel_size=pixel_size,
        quality=90
    )

def main():
    """生成真实的像素化示例图片"""
    print("开始生成真实的像素化示例图片...")
    
    # 定义示例配置
    examples = [
        {
            "title": "轻度像素化",
            "name": "light",
            "pixel_size": 8,
            "seed": "pixelate1",
        },
        {
            "title": "中度像素化",
            "name": "medium", 
            "pixel_size": 16,
            "seed": "pixelate2",
        },
        {
            "title": "重度像素化",
            "name": "heavy",
            "pixel_size": 32,
            "seed": "pixelate3",
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
            
            # 处理像素化效果
            print(f"处理图片: {example['pixel_size']}像素 像素化")
            processed_bytes = process_pixelate_image(
                image_bytes, 
                example['pixel_size']
            )
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"pixelate-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出配置更新信息
    print("\n请更新 frontend/src/config/examples/pixelateExamples.ts 中的URL:")
    for example in examples:
        original_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/original-{example['name']}.jpg"
        processed_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/pixelate-{example['name']}.jpg"
        print(f"  {example['title']}:")
        print(f"    originalImage: \"{original_url}\"")
        print(f"    processedImage: \"{processed_url}\"")

if __name__ == "__main__":
    main()
