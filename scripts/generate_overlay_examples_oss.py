#!/usr/bin/env python3
"""
生成叠加页面的OSS示例图片
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
from app.services.overlay_service import OverlayService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"overlay/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{file_key}"

def process_overlay_image(image_bytes: bytes, overlay_type: str, opacity: float = 0.8, **kwargs) -> bytes:
    """使用OverlayService处理图片"""
    print(f"处理图片: {overlay_type}, opacity={opacity}")
    
    return OverlayService.add_overlay(
        image_bytes=image_bytes,
        overlay_type=overlay_type,
        opacity=opacity,
        **kwargs
    )

def main():
    """生成overlay示例图片"""
    print("开始生成overlay示例图片...")
    
    # 定义示例配置
    examples = [
        {
            "title": "中心叠加",
            "name": "center",
            "overlay_type": "gradient",
            "opacity": 0.8,
            "seed": "overlay1",
            "params": {
                "gradient_type": "radial",
                "start_color": "#000000",
                "end_color": "#FFFFFF",
                "start_opacity": 0.0,
                "end_opacity": 0.8
            }
        },
        {
            "title": "左上角叠加",
            "name": "top-left", 
            "overlay_type": "gradient",
            "opacity": 0.7,
            "seed": "overlay2",
            "params": {
                "gradient_type": "linear",
                "gradient_direction": "to_bottom",
                "start_color": "#000000",
                "end_color": "#FFFFFF",
                "start_opacity": 0.0,
                "end_opacity": 0.7
            }
        },
        {
            "title": "右下角叠加",
            "name": "bottom-right",
            "overlay_type": "vignette",
            "opacity": 0.9,
            "seed": "overlay3",
            "params": {
                "vignette_intensity": 0.6,
                "vignette_radius": 1.2
            }
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
            
            # 处理叠加效果
            print(f"处理图片: {example['overlay_type']} 叠加")
            processed_bytes = process_overlay_image(
                image_bytes, 
                example['overlay_type'], 
                example['opacity'],
                **example['params']
            )
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"overlay-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出配置更新信息
    print("\n请更新 frontend/src/config/examples/overlayExamples.ts 中的URL:")
    for example in examples:
        original_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-{example['name']}.jpg"
        processed_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-{example['name']}.jpg"
        print(f"  {example['title']}:")
        print(f"    originalImage: \"{original_url}\"")
        print(f"    processedImage: \"{processed_url}\"")

if __name__ == "__main__":
    main()
