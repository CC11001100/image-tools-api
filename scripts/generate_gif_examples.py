#!/usr/bin/env python3
"""
生成gif页面的OSS示例图片
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
from app.services.gif_service import GifService

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

def generate_gif_examples():
    """生成gif页面示例"""
    print("\n🎬 生成GIF页面示例...")
    
    examples = [
        {
            'title': '图片转GIF',
            'name': 'images-to-gif',
            'seeds': ['gif-frame1-001', 'gif-frame2-001', 'gif-frame3-001'],
            'params': {'duration': 500, 'loop': 0}
        },
        {
            'title': '快速GIF',
            'name': 'fast-gif',
            'seeds': ['gif-fast1-002', 'gif-fast2-002'],
            'params': {'duration': 200, 'loop': 0}
        },
        {
            'title': '慢速GIF',
            'name': 'slow-gif',
            'seeds': ['gif-slow1-003', 'gif-slow2-003', 'gif-slow3-003'],
            'params': {'duration': 1000, 'loop': 0}
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载多张图片作为帧
            frames = []
            frame_urls = []
            for i, seed in enumerate(example['seeds']):
                print(f"下载帧 {i+1}: https://picsum.photos/seed/{seed}/540/540")
                frame_bytes = download_image(f"https://picsum.photos/seed/{seed}/540/540")
                frames.append(frame_bytes)
                
                # 上传原始帧
                frame_url = upload_to_oss(frame_bytes, f"gif/frame-{example['name']}-{i+1}.jpg")
                frame_urls.append(frame_url)
            
            # 处理GIF生成
            print(f"🎬 处理GIF生成: {example['title']}")
            
            # 将字节数据转换为PIL图像
            pil_frames = []
            for frame_bytes in frames:
                pil_frames.append(Image.open(io.BytesIO(frame_bytes)))
            
            gif_bytes = GifService.images_to_gif(
                pil_frames,
                duration=example['params']['duration'],
                loop=example['params']['loop']
            )
            
            # 上传GIF结果
            gif_url = upload_to_oss(gif_bytes, f"gif/gif-{example['name']}.gif")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   帧数: {len(frames)}")
            print(f"   GIF: {gif_url}")
            for i, frame_url in enumerate(frame_urls):
                print(f"   帧{i+1}: {frame_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nGIF示例生成完成！成功: {success_count}/{len(examples)}")

def main():
    """主函数"""
    print("🚀 开始生成gif页面示例图片...")
    
    # 生成GIF示例
    generate_gif_examples()
    
    print("\n🎉 所有示例生成完成！")

if __name__ == "__main__":
    main()
