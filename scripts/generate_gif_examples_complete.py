#!/usr/bin/env python3
"""
生成gif、create-gif、extract-gif页面的完整示例图片
"""

import sys
import os
from pathlib import Path
from PIL import Image
import io
import requests

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import OSSClient
from app.services.gif_service import GifService

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

def generate_gif_processing_examples():
    """生成gif页面示例（GIF处理）"""
    print("🎬 生成gif页面示例图片...")
    
    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/sample-image-1.jpg",
        "frontend/public/examples/sample-image-2.jpg",
        "frontend/public/examples/sample-image-3.jpg",
        "frontend/public/examples/original-nature.jpg"
    ]
    
    examples = [
        {
            'title': 'GIF压缩优化',
            'name': 'optimize',
            'image_paths': local_images[:3],
            'description': '压缩GIF文件大小，减少颜色数量',
            'params': {
                'max_colors': 64,
                'resize_factor': 0.8
            }
        },
        {
            'title': 'GIF帧率调整',
            'name': 'fps',
            'image_paths': local_images[1:4],
            'description': '调整GIF播放帧率，控制播放速度',
            'params': {
                'target_fps': 15
            }
        },
        {
            'title': 'GIF尺寸调整',
            'name': 'resize',
            'image_paths': local_images[:2],
            'description': '调整GIF尺寸，保持动画效果',
            'params': {
                'resize_factor': 0.6
            }
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 准备帧图片
            frames = []
            for i, image_path in enumerate(example['image_paths']):
                if not Path(image_path).exists():
                    print(f"❌ 图片文件不存在: {image_path}")
                    continue
                
                # 调整图片尺寸为1080x1920
                frame_bytes = resize_image_to_1080x1920(image_path)
                frames.append(Image.open(io.BytesIO(frame_bytes)))
            
            if len(frames) < 2:
                print(f"❌ 帧数不足: {example['title']}")
                continue
            
            # 创建原始GIF
            print(f"创建原始GIF: {len(frames)}帧")
            original_gif_bytes = GifService.images_to_gif(
                frames,
                duration=500,
                loop=0,
                optimize=True
            )
            
            # 上传原始GIF
            original_filename = f"gif/original-{example['name']}.gif"
            original_url = upload_to_oss(original_gif_bytes, original_filename)
            
            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue
            
            print(f"✅ 原图上传成功: {original_url}")
            
            # 处理GIF
            print(f"处理GIF: {example['description']}")
            if example['name'] == 'optimize':
                processed_gif_bytes = GifService.optimize_gif(
                    original_gif_bytes,
                    max_colors=example['params']['max_colors'],
                    resize_factor=example['params']['resize_factor']
                )
            elif example['name'] == 'fps':
                processed_gif_bytes = GifService.optimize_gif(
                    original_gif_bytes,
                    target_fps=example['params']['target_fps']
                )
            elif example['name'] == 'resize':
                processed_gif_bytes = GifService.optimize_gif(
                    original_gif_bytes,
                    resize_factor=example['params']['resize_factor']
                )
            else:
                processed_gif_bytes = original_gif_bytes
            
            # 上传处理后的GIF
            processed_filename = f"gif/gif-{example['name']}.gif"
            processed_url = upload_to_oss(processed_gif_bytes, processed_filename)
            
            if processed_url:
                print(f"✅ 效果图上传成功: {processed_url}")
                success_count += 1
            else:
                print(f"❌ 效果图上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\ngif页面生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def generate_create_gif_examples():
    """生成create-gif页面示例（创建GIF）"""
    print("🎨 生成create-gif页面示例图片...")
    
    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/watermark/watermark-example-1.jpg",
        "frontend/public/examples/watermark/watermark-example-2.jpg",
        "frontend/public/examples/watermark/watermark-example-3.jpg",
        "frontend/public/examples/original-landscape.jpg"
    ]
    
    examples = [
        {
            'title': '标准GIF创建',
            'name': 'standard',
            'image_paths': local_images[:3],
            'description': '将多张图片合成为标准GIF动画',
            'params': {
                'duration': 500,
                'loop': 0,
                'optimize': True
            }
        },
        {
            'title': '快速GIF创建',
            'name': 'fast',
            'image_paths': local_images[1:4],
            'description': '创建快速播放的GIF动画',
            'params': {
                'duration': 200,
                'loop': 0,
                'optimize': True
            }
        },
        {
            'title': '慢速GIF创建',
            'name': 'slow',
            'image_paths': local_images[:2],
            'description': '创建慢速播放的GIF动画',
            'params': {
                'duration': 1000,
                'loop': 0,
                'optimize': True
            }
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 准备帧图片
            frames = []
            frame_urls = []
            
            for i, image_path in enumerate(example['image_paths']):
                if not Path(image_path).exists():
                    print(f"❌ 图片文件不存在: {image_path}")
                    continue
                
                # 调整图片尺寸为1080x1920
                frame_bytes = resize_image_to_1080x1920(image_path)
                frames.append(Image.open(io.BytesIO(frame_bytes)))
                
                # 上传单独的帧图片
                frame_filename = f"create-gif/frame-{example['name']}-{i+1}.jpg"
                frame_url = upload_to_oss(frame_bytes, frame_filename)
                if frame_url:
                    frame_urls.append(frame_url)
            
            if len(frames) < 2:
                print(f"❌ 帧数不足: {example['title']}")
                continue
            
            # 上传第一帧作为原图展示
            if frame_urls:
                print(f"✅ 原图上传成功: {frame_urls[0]}")
            
            # 创建GIF
            print(f"创建GIF: {len(frames)}帧, 间隔{example['params']['duration']}ms")
            gif_bytes = GifService.images_to_gif(
                frames,
                duration=example['params']['duration'],
                loop=example['params']['loop'],
                optimize=example['params']['optimize']
            )
            
            # 上传GIF
            gif_filename = f"create-gif/create-gif-{example['name']}.gif"
            gif_url = upload_to_oss(gif_bytes, gif_filename)
            
            if gif_url:
                print(f"✅ GIF上传成功: {gif_url}")
                success_count += 1
            else:
                print(f"❌ GIF上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\ncreate-gif页面生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def generate_extract_gif_examples():
    """生成extract-gif页面示例（提取GIF帧）"""
    print("🔍 生成extract-gif页面示例图片...")

    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/sample-image-1.jpg",
        "frontend/public/examples/sample-image-2.jpg",
        "frontend/public/examples/sample-image-3.jpg"
    ]

    examples = [
        {
            'title': '提取所有帧',
            'name': 'all-frames',
            'image_paths': local_images,
            'description': '提取GIF中的所有帧图片',
            'extract_type': 'all'
        },
        {
            'title': '提取关键帧',
            'name': 'key-frames',
            'image_paths': local_images[:2],
            'description': '提取GIF中的关键帧',
            'extract_type': 'key'
        },
        {
            'title': '按时间提取',
            'name': 'time-frames',
            'image_paths': local_images[1:],
            'description': '按指定时间间隔提取帧',
            'extract_type': 'time'
        }
    ]

    success_count = 0

    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")

            # 准备帧图片
            frames = []
            for image_path in example['image_paths']:
                if not Path(image_path).exists():
                    print(f"❌ 图片文件不存在: {image_path}")
                    continue

                # 调整图片尺寸为1080x1920
                frame_bytes = resize_image_to_1080x1920(image_path)
                frames.append(Image.open(io.BytesIO(frame_bytes)))

            if len(frames) < 2:
                print(f"❌ 帧数不足: {example['title']}")
                continue

            # 创建原始GIF
            print(f"创建原始GIF: {len(frames)}帧")
            original_gif_bytes = GifService.images_to_gif(
                frames,
                duration=400,
                loop=0,
                optimize=True
            )

            # 上传原始GIF
            original_filename = f"extract-gif/original-{example['name']}.gif"
            original_url = upload_to_oss(original_gif_bytes, original_filename)

            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue

            print(f"✅ 原图上传成功: {original_url}")

            # 提取帧
            print(f"提取帧: {example['description']}")
            extracted_frames = GifService.gif_to_images(original_gif_bytes)

            # 上传提取的帧（作为示例展示第一帧）
            if extracted_frames:
                first_frame_bytes = io.BytesIO()
                extracted_frames[0].save(first_frame_bytes, format='JPEG', quality=95)

                extracted_filename = f"extract-gif/extracted-{example['name']}.jpg"
                extracted_url = upload_to_oss(first_frame_bytes.getvalue(), extracted_filename)

                if extracted_url:
                    print(f"✅ 提取帧上传成功: {extracted_url} (共提取{len(extracted_frames)}帧)")
                    success_count += 1
                else:
                    print(f"❌ 提取帧上传失败: {example['title']}")
            else:
                print(f"❌ 帧提取失败: {example['title']}")

        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue

    print(f"\nextract-gif页面生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def main():
    """主函数"""
    print("🚀 开始生成gif相关页面示例...")
    print("=" * 60)

    total_success = 0
    total_examples = 0

    # 生成gif页面示例
    gif_success, gif_total = generate_gif_processing_examples()
    total_success += gif_success
    total_examples += gif_total

    print("\n" + "=" * 60)

    # 生成create-gif页面示例
    create_gif_success, create_gif_total = generate_create_gif_examples()
    total_success += create_gif_success
    total_examples += create_gif_total

    print("\n" + "=" * 60)

    # 生成extract-gif页面示例
    extract_gif_success, extract_gif_total = generate_extract_gif_examples()
    total_success += extract_gif_success
    total_examples += extract_gif_total

    print("\n" + "=" * 60)
    print("📋 总体生成结果")
    print("=" * 60)

    overall_success_rate = (total_success / total_examples) * 100 if total_examples > 0 else 0
    print(f"📊 总体成功率: {total_success}/{total_examples} ({overall_success_rate:.1f}%)")

    print(f"\n🎯 生成情况:")
    print(f"✅ gif页面: {gif_success}/{gif_total}")
    print(f"✅ create-gif页面: {create_gif_success}/{create_gif_total}")
    print(f"✅ extract-gif页面: {extract_gif_success}/{extract_gif_total}")

    print("\n" + "=" * 60)
    print("🎉 gif相关示例生成完成！")

if __name__ == "__main__":
    main()
