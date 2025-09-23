#!/usr/bin/env python3
"""
生成图片拼接页面的OSS示例图片
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
from app.services.stitch_service_backup import StitchService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"image-tools-api/examples/stitch/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/{file_key}"

def process_stitch_image(image1_bytes: bytes, image2_bytes: bytes, direction: str) -> bytes:
    """处理图片拼接"""
    return StitchService.stitch_images(
        image_bytes_list=[image1_bytes, image2_bytes],
        direction=direction,
        spacing=10,
        quality=90
    )

def main():
    """主函数"""
    print("开始生成图片拼接示例图片...")
    
    # 定义3个示例
    examples = [
        {
            "name": "horizontal",
            "direction": "horizontal",
            "seed1": 4001,
            "seed2": 4002,
            "title": "水平拼接",
            "description": "将两张图片水平拼接在一起"
        },
        {
            "name": "vertical",
            "direction": "vertical", 
            "seed1": 4003,
            "seed2": 4004,
            "title": "垂直拼接",
            "description": "将两张图片垂直拼接在一起"
        },
        {
            "name": "grid",
            "direction": "grid",
            "seed1": 4005,
            "seed2": 4006,
            "title": "网格拼接",
            "description": "将多张图片按网格方式拼接"
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载两张原图
            print(f"下载图片1: https://picsum.photos/seed/{example['seed1']}/800/600")
            image1_bytes = download_image(f"https://picsum.photos/seed/{example['seed1']}/800/600")
            
            print(f"下载图片2: https://picsum.photos/seed/{example['seed2']}/800/600")
            image2_bytes = download_image(f"https://picsum.photos/seed/{example['seed2']}/800/600")
            
            # 上传原图1
            original1_url = upload_to_oss(image1_bytes, f"original1-{example['name']}.jpg")
            
            # 上传原图2
            original2_url = upload_to_oss(image2_bytes, f"original2-{example['name']}.jpg")
            
            # 处理拼接
            print(f"处理图片: {example['direction']} 拼接")
            processed_bytes = process_stitch_image(image1_bytes, image2_bytes, example['direction'])
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"stitch-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n🎉 图片拼接示例生成完成!")
    print(f"成功生成: {success_count}/{len(examples)} 个示例")
    
    if success_count > 0:
        print(f"\n📸 生成的示例:")
        for i, example in enumerate(examples[:success_count]):
            print(f"📸 {example['title']}:")
            print(f"   原图1: https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-{example['name']}.jpg")
            print(f"   原图2: https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-{example['name']}.jpg")
            print(f"   拼接图: https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-{example['name']}.jpg")

if __name__ == '__main__':
    main()
