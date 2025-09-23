#!/usr/bin/env python3
"""
生成混合页面的OSS示例图片
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
from app.services.blend_service import BlendService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"blend/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{file_key}"

def process_blend_image(base_image_bytes: bytes, blend_image_bytes: bytes, blend_mode: str, opacity: float = 0.8) -> bytes:
    """使用BlendService处理图片"""
    print(f"处理图片: {blend_mode}, opacity={opacity}")
    
    return BlendService.blend_images(
        base_image_bytes=base_image_bytes,
        blend_image_bytes=blend_image_bytes,
        blend_mode=blend_mode,
        opacity=opacity
    )

def main():
    """生成blend示例图片"""
    print("开始生成blend示例图片...")
    
    # 定义示例配置
    examples = [
        {
            "title": "正常混合",
            "name": "normal",
            "blend_mode": "normal",
            "opacity": 0.8,
            "base_seed": "blend1",
            "blend_seed": "blend2"
        },
        {
            "title": "正片叠底",
            "name": "multiply", 
            "blend_mode": "multiply",
            "opacity": 0.7,
            "base_seed": "blend3",
            "blend_seed": "blend4"
        },
        {
            "title": "滤色混合",
            "name": "screen",
            "blend_mode": "screen",
            "opacity": 0.8,
            "base_seed": "blend5",
            "blend_seed": "blend6"
        },
        {
            "title": "叠加混合",
            "name": "overlay",
            "blend_mode": "overlay",
            "opacity": 0.9,
            "base_seed": "blend7",
            "blend_seed": "blend8"
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载基础图片
            print(f"下载基础图片: https://picsum.photos/seed/{example['base_seed']}/800/800")
            base_image_bytes = download_image(f"https://picsum.photos/seed/{example['base_seed']}/800/800")
            
            # 下载混合图片
            print(f"下载混合图片: https://picsum.photos/seed/{example['blend_seed']}/800/800")
            blend_image_bytes = download_image(f"https://picsum.photos/seed/{example['blend_seed']}/800/800")
            
            # 上传基础图片
            base_url = upload_to_oss(base_image_bytes, f"base-{example['name']}.jpg")
            
            # 处理混合效果
            print(f"处理图片: {example['blend_mode']} 混合")
            processed_bytes = process_blend_image(base_image_bytes, blend_image_bytes, example['blend_mode'], example['opacity'])
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"blend-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   基础图: {base_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出配置更新信息
    print("\n请更新 frontend/src/config/examples/blendExamples.ts 中的URL:")
    for example in examples:
        base_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-{example['name']}.jpg"
        processed_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-{example['name']}.jpg"
        print(f"  {example['title']}:")
        print(f"    originalImage: \"{base_url}\"")
        print(f"    processedImage: \"{processed_url}\"")

if __name__ == "__main__":
    main()
