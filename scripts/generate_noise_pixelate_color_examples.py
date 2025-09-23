#!/usr/bin/env python3
"""
生成noise、pixelate、color页面的OSS示例图片
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
from app.services.noise_service_backup import NoiseService
from app.services.pixelate_service import PixelateService
from app.services.color_service import ColorService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    print(f"上传到OSS: {filename}")
    oss_client.upload_bytes(image_bytes, filename)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{filename}"

def generate_noise_examples():
    """生成noise页面示例"""
    print("\n🔊 生成Noise页面示例...")
    
    examples = [
        {
            'title': '高斯噪点',
            'name': 'gaussian',
            'seed': 'noise-gaussian-001',
            'params': {'noise_type': 'gaussian', 'intensity': 0.3}
        },
        {
            'title': '泊松噪点',
            'name': 'poisson',
            'seed': 'noise-poisson-002',
            'params': {'noise_type': 'poisson', 'intensity': 0.2}
        },
        {
            'title': '椒盐噪点',
            'name': 'salt_pepper',
            'seed': 'noise-salt-003',
            'params': {'noise_type': 'salt_pepper', 'intensity': 0.1}
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
            original_url = upload_to_oss(image_bytes, f"noise/original-{example['name']}.jpg")
            
            # 处理噪点效果
            print(f"处理图片: {example['params']['noise_type']} 噪点")
            processed_bytes = NoiseService.add_noise(
                image_bytes=image_bytes,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"noise/noise-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nNoise示例生成完成！成功: {success_count}/{len(examples)}")

def generate_pixelate_examples():
    """生成pixelate页面示例"""
    print("\n🔲 生成Pixelate页面示例...")
    
    examples = [
        {
            'title': '轻度像素化',
            'name': 'light',
            'seed': 'pixelate-light-001',
            'params': {'pixel_size': 8}
        },
        {
            'title': '中度像素化',
            'name': 'medium',
            'seed': 'pixelate-medium-002',
            'params': {'pixel_size': 16}
        },
        {
            'title': '重度像素化',
            'name': 'heavy',
            'seed': 'pixelate-heavy-003',
            'params': {'pixel_size': 32}
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
            original_url = upload_to_oss(image_bytes, f"pixelate/original-{example['name']}.jpg")
            
            # 处理像素化效果
            print(f"处理图片: {example['params']['pixel_size']}px 像素化")
            processed_bytes = PixelateService.pixelate_full(
                image_bytes=image_bytes,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"pixelate/pixelate-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nPixelate示例生成完成！成功: {success_count}/{len(examples)}")

def generate_color_examples():
    """生成color页面示例"""
    print("\n🎨 生成Color页面示例...")
    
    examples = [
        {
            'title': '亮度调整',
            'name': 'brightness',
            'seed': 'color-brightness-001',
            'params': {'brightness': 0.3}
        },
        {
            'title': '对比度调整',
            'name': 'contrast',
            'seed': 'color-contrast-002',
            'params': {'contrast': 0.5}
        },
        {
            'title': '饱和度调整',
            'name': 'saturation',
            'seed': 'color-saturation-003',
            'params': {'saturation': 0.8}
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
            original_url = upload_to_oss(image_bytes, f"color/original-{example['name']}.jpg")
            
            # 处理颜色调整
            print(f"处理图片: {example['name']} 调整")
            processed_bytes = ColorService.adjust_color(
                image_bytes=image_bytes,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"color/color-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nColor示例生成完成！成功: {success_count}/{len(examples)}")

def main():
    """主函数"""
    print("🚀 开始生成noise、pixelate、color页面示例图片...")
    
    # 生成各页面示例
    generate_noise_examples()
    generate_pixelate_examples()
    generate_color_examples()
    
    print("\n🎉 所有示例生成完成！")

if __name__ == "__main__":
    main()
