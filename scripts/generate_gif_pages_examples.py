#!/usr/bin/env python3
"""
生成gif-optimize、gif-create、gif-extract三个页面的完整示例图片
参照resize等接口的脚本逻辑
"""

import sys
import os
import requests
import io
from pathlib import Path
from PIL import Image

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.oss_client import oss_client
from app.services.gif_service import GifService

def download_random_image(seed: str, width: int = 1080, height: int = 1920) -> bytes:
    """下载随机图片"""
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    print(f"📥 下载图片: {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    print(f"📤 上传到OSS: {filename}")
    oss_client.upload_bytes(image_bytes, filename)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{filename}"

def generate_gif_optimize_examples():
    """生成GIF优化页面示例 (gif-optimize)"""
    print("\n" + "=" * 60)
    print("🎬 生成GIF优化页面示例 (gif-optimize)...")
    print("=" * 60)
    
    examples = [
        {
            'name': 'web',
            'description': '网页优化',
            'seeds': ['gif-opt-web-1', 'gif-opt-web-2', 'gif-opt-web-3'],
            'params': {
                'max_colors': 128,
                'resize_factor': 0.8
            }
        },
        {
            'name': 'social',
            'description': '社交媒体',
            'seeds': ['gif-opt-social-1', 'gif-opt-social-2', 'gif-opt-social-3', 'gif-opt-social-4'],
            'params': {
                'max_colors': 64,
                'resize_factor': 0.7,
                'target_fps': 12
            }
        },
        {
            'name': 'quality',
            'description': '高质量保留',
            'seeds': ['gif-opt-quality-1', 'gif-opt-quality-2', 'gif-opt-quality-3'],
            'params': {
                'max_colors': 256,
                'resize_factor': 1.0
            }
        },
        {
            'name': 'extreme',
            'description': '极限压缩',
            'seeds': ['gif-opt-extreme-1', 'gif-opt-extreme-2'],
            'params': {
                'max_colors': 32,
                'resize_factor': 0.5,
                'target_fps': 8
            }
        },
        {
            'name': 'smooth',
            'description': '流畅动画',
            'seeds': ['gif-opt-smooth-1', 'gif-opt-smooth-2', 'gif-opt-smooth-3', 'gif-opt-smooth-4'],
            'params': {
                'max_colors': 128,
                'resize_factor': 0.9,
                'target_fps': 20
            }
        },
        {
            'name': 'mobile',
            'description': '移动端优化',
            'seeds': ['gif-opt-mobile-1', 'gif-opt-mobile-2', 'gif-opt-mobile-3'],
            'params': {
                'max_colors': 96,
                'resize_factor': 0.6,
                'target_fps': 15
            }
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['description']}")
            
            # 下载多帧图片
            frames = []
            for i, seed in enumerate(example['seeds']):
                frame_bytes = download_random_image(seed)
                frames.append(Image.open(io.BytesIO(frame_bytes)))
            
            print(f"✅ 已准备 {len(frames)} 帧图片")
            
            # 创建原始GIF
            print(f"🎬 创建原始GIF...")
            original_gif_bytes = GifService.images_to_gif(
                frames,
                duration=400,
                loop=0,
                optimize=False
            )
            
            # 上传原始GIF
            original_filename = f"gif/original-{example['name']}.gif"
            original_url = upload_to_oss(original_gif_bytes, original_filename)
            print(f"✅ 原图上传成功: {original_url}")
            
            # 优化GIF
            print(f"🔧 优化GIF: {example['params']}")
            optimized_gif_bytes = GifService.optimize_gif(
                original_gif_bytes,
                **example['params']
            )
            
            # 上传优化后的GIF
            optimized_filename = f"gif/optimized-{example['name']}.gif"
            optimized_url = upload_to_oss(optimized_gif_bytes, optimized_filename)
            print(f"✅ 效果图上传成功: {optimized_url}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['description']} - {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n✅ GIF优化页面生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def generate_create_gif_examples():
    """生成创建GIF页面示例 (create-gif)"""
    print("\n" + "=" * 60)
    print("🎨 生成创建GIF页面示例 (create-gif)...")
    print("=" * 60)
    
    examples = [
        {
            'name': 'standard',
            'description': '标准GIF创建',
            'seeds': ['gif-create-std-1', 'gif-create-std-2', 'gif-create-std-3'],
            'params': {
                'duration': 500,
                'loop': 0,
                'optimize': True
            }
        },
        {
            'name': 'fast',
            'description': '快速GIF创建',
            'seeds': ['gif-create-fast-1', 'gif-create-fast-2', 'gif-create-fast-3', 'gif-create-fast-4'],
            'params': {
                'duration': 200,
                'loop': 0,
                'optimize': True
            }
        },
        {
            'name': 'slow',
            'description': '慢速GIF创建',
            'seeds': ['gif-create-slow-1', 'gif-create-slow-2'],
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
            print(f"\n处理示例: {example['description']}")
            
            # 下载多帧图片
            frames = []
            frame_urls = []
            
            for i, seed in enumerate(example['seeds']):
                frame_bytes = download_random_image(seed)
                frames.append(Image.open(io.BytesIO(frame_bytes)))
                
                # 上传第一帧作为原图展示
                if i == 0:
                    frame_filename = f"create-gif/frame-{example['name']}-{i+1}.jpg"
                    frame_url = upload_to_oss(frame_bytes, frame_filename)
                    frame_urls.append(frame_url)
                    print(f"✅ 原图上传成功: {frame_url}")
            
            print(f"✅ 已准备 {len(frames)} 帧图片")
            
            # 创建GIF
            print(f"🎬 创建GIF: 间隔{example['params']['duration']}ms")
            gif_bytes = GifService.images_to_gif(
                frames,
                **example['params']
            )
            
            # 上传GIF
            gif_filename = f"create-gif/create-gif-{example['name']}.gif"
            gif_url = upload_to_oss(gif_bytes, gif_filename)
            print(f"✅ GIF上传成功: {gif_url}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['description']} - {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n✅ 创建GIF页面生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def generate_extract_gif_examples():
    """生成提取GIF帧页面示例 (extract-gif)"""
    print("\n" + "=" * 60)
    print("🔍 生成提取GIF帧页面示例 (extract-gif)...")
    print("=" * 60)
    
    examples = [
        {
            'name': 'all',
            'description': '全帧提取',
            'seeds': ['gif-extract-all-1', 'gif-extract-all-2', 'gif-extract-all-3'],
            'extract_type': 'all'
        },
        {
            'name': 'png',
            'description': '高质量PNG',
            'seeds': ['gif-extract-png-1', 'gif-extract-png-2', 'gif-extract-png-3'],
            'extract_type': 'png'
        },
        {
            'name': 'key',
            'description': '关键帧提取',
            'seeds': ['gif-extract-key-1', 'gif-extract-key-2', 'gif-extract-key-3', 'gif-extract-key-4'],
            'extract_type': 'key'
        },
        {
            'name': 'range',
            'description': '范围提取',
            'seeds': ['gif-extract-range-1', 'gif-extract-range-2', 'gif-extract-range-3'],
            'extract_type': 'range'
        },
        {
            'name': 'compress',
            'description': '压缩提取',
            'seeds': ['gif-extract-comp-1', 'gif-extract-comp-2'],
            'extract_type': 'compress'
        },
        {
            'name': 'selected',
            'description': '精选帧提取',
            'seeds': ['gif-extract-sel-1', 'gif-extract-sel-2', 'gif-extract-sel-3', 'gif-extract-sel-4'],
            'extract_type': 'selected'
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['description']}")
            
            # 下载多帧图片
            frames = []
            for seed in example['seeds']:
                frame_bytes = download_random_image(seed)
                frames.append(Image.open(io.BytesIO(frame_bytes)))
            
            print(f"✅ 已准备 {len(frames)} 帧图片")
            
            # 创建原始GIF
            print(f"🎬 创建原始GIF...")
            original_gif_bytes = GifService.images_to_gif(
                frames,
                duration=400,
                loop=0,
                optimize=True
            )
            
            # 上传原始GIF
            original_filename = f"gif/original-extract-{example['name']}.gif"
            original_url = upload_to_oss(original_gif_bytes, original_filename)
            print(f"✅ 原图上传成功: {original_url}")
            
            # 提取帧
            print(f"🔍 提取帧: {example['description']}")
            extracted_frames = GifService.gif_to_images(original_gif_bytes)
            
            if extracted_frames:
                # 保存第一帧作为展示
                first_frame_bytes = io.BytesIO()
                if example['extract_type'] == 'png':
                    extracted_frames[0].save(first_frame_bytes, format='PNG')
                    ext = 'png'
                else:
                    extracted_frames[0].save(first_frame_bytes, format='JPEG', quality=95)
                    ext = 'png'  # 前端配置用的都是png
                
                extracted_filename = f"gif/extracted-{example['name']}-frames.{ext}"
                extracted_url = upload_to_oss(first_frame_bytes.getvalue(), extracted_filename)
                print(f"✅ 提取帧上传成功: {extracted_url} (共提取{len(extracted_frames)}帧)")
                
                success_count += 1
            else:
                print(f"❌ 帧提取失败: {example['description']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['description']} - {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n✅ 提取GIF帧页面生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def main():
    """主函数"""
    print("🚀 开始生成GIF相关页面示例...")
    print("=" * 60)
    
    total_success = 0
    total_examples = 0
    
    # 生成GIF优化页面示例
    optimize_success, optimize_total = generate_gif_optimize_examples()
    total_success += optimize_success
    total_examples += optimize_total
    
    # 生成创建GIF页面示例
    create_success, create_total = generate_create_gif_examples()
    total_success += create_success
    total_examples += create_total
    
    # 生成提取GIF帧页面示例
    extract_success, extract_total = generate_extract_gif_examples()
    total_success += extract_success
    total_examples += extract_total
    
    # 总结
    print("\n" + "=" * 60)
    print("📋 总体生成结果")
    print("=" * 60)
    
    overall_success_rate = (total_success / total_examples) * 100 if total_examples > 0 else 0
    print(f"📊 总体成功率: {total_success}/{total_examples} ({overall_success_rate:.1f}%)")
    
    print(f"\n🎯 各页面生成情况:")
    print(f"  ✅ GIF优化 (gif-optimize): {optimize_success}/{optimize_total}")
    print(f"  ✅ 创建GIF (gif-create): {create_success}/{create_total}")
    print(f"  ✅ 提取GIF帧 (gif-extract): {extract_success}/{extract_total}")
    
    print("\n" + "=" * 60)
    print("🎉 所有GIF页面示例生成完成！")

if __name__ == "__main__":
    main()
