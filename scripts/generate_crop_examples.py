#!/usr/bin/env python3
"""
生成crop页面示例图片脚本
为crop页面生成6个高质量的裁剪示例图片并上传到OSS
"""

import os
import sys
import requests
import io
from PIL import Image

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.crop_service import CropService
from app.services.oss_client import oss_client

def download_random_image(seed: int, width: int = 1080, height: int = 1920) -> bytes:
    """从picsum.photos下载指定尺寸的随机图片"""
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}.jpg"
    print(f"下载图片: {url}")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    return response.content

def process_crop_image(image_bytes: bytes, crop_type: str, **params) -> bytes:
    """使用CropService处理图片"""
    print(f"处理图片: {crop_type}, 参数: {params}")
    
    if crop_type == "rectangle" or crop_type == "center":
        return CropService.crop_rectangle(
            image_bytes=image_bytes,
            x=params.get('x', 0),
            y=params.get('y', 0),
            width=params.get('width', 400),
            height=params.get('height', 300),
            quality=params.get('quality', 90)
        )
    elif crop_type == "smart_center":
        return CropService.crop_smart_center(
            image_bytes=image_bytes,
            target_width=params.get('width', 400),
            target_height=params.get('height', 300),
            quality=params.get('quality', 90)
        )
    else:
        raise ValueError(f"不支持的裁剪类型: {crop_type}")

def upload_to_oss(image_bytes: bytes, object_key: str) -> str:
    """上传图片到OSS并返回URL"""
    print(f"上传到OSS: {object_key}")

    try:
        url = oss_client.upload_bytes(
            file_bytes=image_bytes,
            object_key=object_key,
            content_type="image/jpeg"
        )

        if url:
            print(f"上传成功: {url}")
            return url
        else:
            raise Exception("上传返回空URL")

    except Exception as e:
        print(f"上传失败: {object_key} - {e}")
        raise

def main():
    """主函数：生成6个crop示例"""
    
    # 定义6个示例配置
    examples = [
        {
            "name": "center-crop",
            "title": "中心裁剪",
            "seed": 1001,
            "crop_type": "center",
            "params": {"width": 800, "height": 800}
        },
        {
            "name": "square-crop", 
            "title": "正方形裁剪",
            "seed": 1002,
            "crop_type": "center",
            "params": {"width": 600, "height": 600}
        },
        {
            "name": "rectangle-crop",
            "title": "矩形裁剪",
            "seed": 1003,
            "crop_type": "rectangle",
            "params": {"x": 140, "y": 360, "width": 800, "height": 600}
        },
        {
            "name": "ratio-16-9",
            "title": "16:9比例裁剪",
            "seed": 1004,
            "crop_type": "rectangle", 
            "params": {"x": 0, "y": 420, "width": 1080, "height": 607}
        },
        {
            "name": "ratio-4-3",
            "title": "4:3比例裁剪",
            "seed": 1005,
            "crop_type": "rectangle",
            "params": {"x": 90, "y": 360, "width": 900, "height": 675}
        },
        {
            "name": "smart-center",
            "title": "智能居中裁剪",
            "seed": 1006,
            "crop_type": "smart_center",
            "params": {"width": 700, "height": 700}
        }
    ]
    
    print("开始生成crop示例图片...")
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            original_bytes = download_random_image(example['seed'])
            
            # 处理图片
            processed_bytes = process_crop_image(
                original_bytes, 
                example['crop_type'], 
                **example['params']
            )
            
            # 上传原图
            original_key = f"crop/crop-original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_key)

            # 上传处理后的图片
            processed_key = f"crop/crop-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_key)
            
            print(f"✅ {example['title']} 完成")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            
        except Exception as e:
            print(f"❌ {example['title']} 失败: {e}")
            continue
    
    print("\n所有crop示例图片生成完成！")

if __name__ == "__main__":
    main()
