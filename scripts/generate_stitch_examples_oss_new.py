#!/usr/bin/env python3
"""
生成拼接页面的OSS示例图片
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
from app.services.stitch_service_backup import StitchService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"stitch/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{file_key}"

def process_stitch_image(image_bytes_list: list, direction: str, spacing: int = 10) -> bytes:
    """使用StitchService处理图片"""
    print(f"处理图片: {direction}, spacing={spacing}")
    
    return StitchService.stitch_images(
        image_bytes_list=image_bytes_list,
        direction=direction,
        spacing=spacing
    )

def main():
    """生成stitch示例图片"""
    print("开始生成stitch示例图片...")
    
    # 定义示例配置
    examples = [
        {
            "title": "水平拼接",
            "name": "horizontal",
            "direction": "horizontal",
            "spacing": 10,
            "seeds": ["stitch1", "stitch2"]
        },
        {
            "title": "垂直拼接",
            "name": "vertical", 
            "direction": "vertical",
            "spacing": 5,
            "seeds": ["stitch3", "stitch4"]
        },
        {
            "title": "网格拼接",
            "name": "grid",
            "direction": "grid",
            "spacing": 8,
            "seeds": ["stitch5", "stitch6", "stitch7", "stitch8"]
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载多张图片
            image_bytes_list = []
            for i, seed in enumerate(example['seeds']):
                print(f"下载图片{i+1}: https://picsum.photos/seed/{seed}/400/400")
                image_bytes = download_image(f"https://picsum.photos/seed/{seed}/400/400")
                image_bytes_list.append(image_bytes)
                
                # 上传原图
                original_url = upload_to_oss(image_bytes, f"original{i+1}-{example['name']}.jpg")
                print(f"   原图{i+1}: {original_url}")
            
            # 处理拼接效果
            print(f"处理图片: {example['direction']} 拼接")
            processed_bytes = process_stitch_image(image_bytes_list, example['direction'], example['spacing'])
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"stitch-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出配置更新信息
    print("\n请更新 frontend/src/config/examples/stitchExamples.ts 中的URL:")
    for example in examples:
        original_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-{example['name']}.jpg"
        processed_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-{example['name']}.jpg"
        print(f"  {example['title']}:")
        print(f"    originalImage: \"{original_url}\"")
        print(f"    processedImage: \"{processed_url}\"")

if __name__ == "__main__":
    main()
