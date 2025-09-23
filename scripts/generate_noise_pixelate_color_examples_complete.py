#!/usr/bin/env python3
"""
生成noise、pixelate、color页面的完整示例图片
包含任务要求的各种效果类型
"""

import sys
import os
from pathlib import Path
from PIL import Image
import io

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import OSSClient
from app.services.noise_service import NoiseService
from app.services.pixelate_service import PixelateService
from app.services.color_service import ColorService

# 初始化OSS客户端
oss_client = OSSClient()

def resize_image_to_1080x1920(image_path):
    """将图片调整为1080x1920尺寸"""
    with Image.open(image_path) as img:
        # 调整尺寸
        resized = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        
        # 转换为RGB模式（如果需要）
        if resized.mode != 'RGB':
            resized = resized.convert('RGB')
        
        # 转换为字节
        output = io.BytesIO()
        resized.save(output, format='JPEG', quality=95)
        return output.getvalue()

def upload_to_oss(image_bytes, filename):
    """上传图片到OSS"""
    try:
        url = oss_client.upload_bytes(image_bytes, filename)
        return url
    except Exception as e:
        print(f"OSS上传失败: {e}")
        return None

def generate_noise_examples():
    """生成noise示例"""
    print("🔊 生成noise页面示例图片...")
    
    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/sample-image-1.jpg",
        "frontend/public/examples/sample-image-2.jpg", 
        "frontend/public/examples/sample-image-3.jpg",
        "frontend/public/examples/original-nature.jpg"
    ]
    
    examples = [
        {
            'title': '高斯噪点',
            'name': 'gaussian',
            'noise_type': 'gaussian',
            'image_path': local_images[0],
            'description': '添加高斯噪点，模拟传感器噪点效果',
            'params': {
                'noise_type': 'gaussian',
                'intensity': 15
            }
        },
        {
            'title': '椒盐噪点',
            'name': 'salt_pepper',
            'noise_type': 'salt_and_pepper',
            'image_path': local_images[1],
            'description': '添加椒盐噪点，产生黑白斑点效果',
            'params': {
                'noise_type': 'salt_and_pepper',
                'intensity': 8
            }
        },
        {
            'title': '泊松噪点',
            'name': 'poisson',
            'noise_type': 'poisson',
            'image_path': local_images[2],
            'description': '添加泊松噪点，模拟光子噪声效果',
            'params': {
                'noise_type': 'poisson',
                'intensity': 12
            }
        },
        {
            'title': '斑点噪点',
            'name': 'speckle',
            'noise_type': 'speckle',
            'image_path': local_images[3],
            'description': '添加斑点噪点，模拟雷达图像噪声',
            'params': {
                'noise_type': 'speckle',
                'intensity': 10
            }
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 检查图片文件是否存在
            image_path = Path(example['image_path'])
            if not image_path.exists():
                print(f"❌ 图片文件不存在: {image_path}")
                continue
            
            # 调整图片尺寸为1080x1920
            print(f"调整图片尺寸: {image_path}")
            original_bytes = resize_image_to_1080x1920(image_path)
            
            # 上传原图
            original_filename = f"noise/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue
            
            print(f"✅ 原图上传成功: {original_url}")
            
            # 生成噪点效果
            print(f"生成噪点效果: {example['noise_type']}")
            processed_bytes = NoiseService.add_noise(
                image_bytes=original_bytes,
                quality=90,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_filename = f"noise/noise-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_filename)
            
            if processed_url:
                print(f"✅ 效果图上传成功: {processed_url}")
                success_count += 1
            else:
                print(f"❌ 效果图上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nnoise生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def generate_pixelate_examples():
    """生成pixelate示例"""
    print("🎮 生成pixelate页面示例图片...")
    
    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/original-landscape.jpg",
        "frontend/public/examples/watermark/watermark-example-2.jpg",
        "frontend/public/examples/watermark/watermark-example-3.jpg",
        "frontend/public/examples/sample-image-1.jpg"
    ]
    
    examples = [
        {
            'title': '像素化效果',
            'name': 'pixelate',
            'image_path': local_images[0],
            'description': '对整张图片应用10像素马赛克，像素化效果',
            'params': {
                'pixel_size': 10
            }
        },
        {
            'title': '马赛克效果',
            'name': 'mosaic',
            'image_path': local_images[1],
            'description': '对整张图片应用20像素马赛克，马赛克效果',
            'params': {
                'pixel_size': 20
            }
        },
        {
            'title': '复古像素',
            'name': 'retro',
            'image_path': local_images[2],
            'description': '对整张图片应用8像素马赛克，复古像素效果',
            'params': {
                'pixel_size': 8
            }
        },
        {
            'title': '低分辨率',
            'name': 'lowres',
            'image_path': local_images[3],
            'description': '对整张图片应用30像素马赛克，低分辨率效果',
            'params': {
                'pixel_size': 30
            }
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 检查图片文件是否存在
            image_path = Path(example['image_path'])
            if not image_path.exists():
                print(f"❌ 图片文件不存在: {image_path}")
                continue
            
            # 调整图片尺寸为1080x1920
            print(f"调整图片尺寸: {image_path}")
            original_bytes = resize_image_to_1080x1920(image_path)
            
            # 上传原图
            original_filename = f"pixelate/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue
            
            print(f"✅ 原图上传成功: {original_url}")
            
            # 生成像素化效果
            print(f"生成像素化效果: {example['params']['pixel_size']}px")
            processed_bytes = PixelateService.pixelate_full(
                image_bytes=original_bytes,
                quality=90,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_filename = f"pixelate/pixelate-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_filename)
            
            if processed_url:
                print(f"✅ 效果图上传成功: {processed_url}")
                success_count += 1
            else:
                print(f"❌ 效果图上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\npixelate生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def generate_color_examples():
    """生成color示例"""
    print("🎨 生成color页面示例图片...")

    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/sample-image-2.jpg",
        "frontend/public/examples/sample-image-3.jpg",
        "frontend/public/examples/original-nature.jpg",
        "frontend/public/examples/original-landscape.jpg",
        "frontend/public/examples/watermark/watermark-example-1.jpg"
    ]

    examples = [
        {
            'title': '亮度调整',
            'name': 'brightness',
            'image_path': local_images[0],
            'description': '增强图片亮度，让图片更明亮清晰',
            'params': {
                'brightness': 30.0
            }
        },
        {
            'title': '对比度调整',
            'name': 'contrast',
            'image_path': local_images[1],
            'description': '增强图片对比度，让明暗对比更鲜明',
            'params': {
                'contrast': 25.0
            }
        },
        {
            'title': '饱和度调整',
            'name': 'saturation',
            'image_path': local_images[2],
            'description': '增强图片饱和度，让色彩更鲜艳生动',
            'params': {
                'saturation': 40.0
            }
        },
        {
            'title': '色相调整',
            'name': 'hue',
            'image_path': local_images[3],
            'description': '调整图片色相，改变整体色调',
            'params': {
                'hue': 30.0
            }
        },
        {
            'title': '伽马调整',
            'name': 'gamma',
            'image_path': local_images[4],
            'description': '调整图片伽马值，改善明暗层次',
            'params': {
                'gamma': 1.5
            }
        }
    ]

    success_count = 0

    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")

            # 检查图片文件是否存在
            image_path = Path(example['image_path'])
            if not image_path.exists():
                print(f"❌ 图片文件不存在: {image_path}")
                continue

            # 调整图片尺寸为1080x1920
            print(f"调整图片尺寸: {image_path}")
            original_bytes = resize_image_to_1080x1920(image_path)

            # 上传原图
            original_filename = f"color/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)

            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue

            print(f"✅ 原图上传成功: {original_url}")

            # 生成颜色调整效果
            print(f"生成颜色调整效果: {example['name']}")
            processed_bytes = ColorService.adjust_color(
                image_bytes=original_bytes,
                quality=90,
                **example['params']
            )

            # 上传处理后的图片
            processed_filename = f"color/color-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_filename)

            if processed_url:
                print(f"✅ 效果图上传成功: {processed_url}")
                success_count += 1
            else:
                print(f"❌ 效果图上传失败: {example['title']}")

        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue

    print(f"\ncolor生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def main():
    """主函数"""
    print("🚀 开始生成noise、pixelate、color示例...")
    print("=" * 60)

    total_success = 0
    total_examples = 0

    # 生成noise示例
    noise_success, noise_total = generate_noise_examples()
    total_success += noise_success
    total_examples += noise_total

    print("\n" + "=" * 60)

    # 生成pixelate示例
    pixelate_success, pixelate_total = generate_pixelate_examples()
    total_success += pixelate_success
    total_examples += pixelate_total

    print("\n" + "=" * 60)

    # 生成color示例
    color_success, color_total = generate_color_examples()
    total_success += color_success
    total_examples += color_total

    print("\n" + "=" * 60)
    print("📋 总体生成结果")
    print("=" * 60)

    overall_success_rate = (total_success / total_examples) * 100 if total_examples > 0 else 0
    print(f"📊 总体成功率: {total_success}/{total_examples} ({overall_success_rate:.1f}%)")

    print(f"\n🎯 生成情况:")
    print(f"✅ noise页面: {noise_success}/{noise_total}")
    print(f"✅ pixelate页面: {pixelate_success}/{pixelate_total}")
    print(f"✅ color页面: {color_success}/{color_total}")

    print("\n" + "=" * 60)
    print("🎉 noise、pixelate、color示例生成完成！")

if __name__ == "__main__":
    main()
