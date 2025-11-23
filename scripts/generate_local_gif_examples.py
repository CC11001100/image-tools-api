#!/usr/bin/env python3
"""
生成本地GIF示例文件
"""

import sys
import requests
import io
from PIL import Image
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.gif_service import GifService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def save_file(data: bytes, filepath: Path):
    """保存文件到本地"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_bytes(data)
    print(f"✅ 保存: {filepath}")

def generate_gif_examples():
    """生成GIF示例"""
    print("\n🎬 生成本地GIF示例...")
    
    # 输出目录
    output_dir = project_root / "frontend" / "public" / "examples" / "gif"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    examples = [
        {
            'title': '基础动画GIF',
            'name': 'basic-animation',
            'seeds': ['gif-anim1', 'gif-anim2', 'gif-anim3', 'gif-anim4'],
            'params': {'duration': 300, 'loop': 0}
        },
        {
            'title': '快速动画',
            'name': 'fast-animation', 
            'seeds': ['gif-fast1', 'gif-fast2', 'gif-fast3'],
            'params': {'duration': 150, 'loop': 0}
        },
        {
            'title': '慢速动画',
            'name': 'slow-animation',
            'seeds': ['gif-slow1', 'gif-slow2', 'gif-slow3'],
            'params': {'duration': 600, 'loop': 0}
        },
        {
            'title': '循环动画',
            'name': 'loop-animation',
            'seeds': ['gif-loop1', 'gif-loop2'],
            'params': {'duration': 400, 'loop': 3}
        },
        {
            'title': '高帧率动画',
            'name': 'high-fps',
            'seeds': ['gif-hfps1', 'gif-hfps2', 'gif-hfps3', 'gif-hfps4', 'gif-hfps5'],
            'params': {'duration': 100, 'loop': 0}
        },
        {
            'title': '简单切换',
            'name': 'simple-switch',
            'seeds': ['gif-switch1', 'gif-switch2'],
            'params': {'duration': 500, 'loop': 0}
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理: {example['title']}")
            
            # 下载帧
            frames = []
            for i, seed in enumerate(example['seeds']):
                url = f"https://picsum.photos/seed/{seed}/400/300"
                print(f"  下载帧 {i+1}/{len(example['seeds'])}: {seed}")
                frame_bytes = download_image(url)
                
                # 保存原始帧
                frame_path = output_dir / f"{example['name']}-frame-{i+1}.jpg"
                save_file(frame_bytes, frame_path)
                
                frames.append(Image.open(io.BytesIO(frame_bytes)))
            
            # 生成GIF
            print(f"  🎬 生成GIF: {example['params']}")
            gif_bytes = GifService.images_to_gif(
                frames,
                duration=example['params']['duration'],
                loop=example['params']['loop']
            )
            
            # 保存GIF
            gif_path = output_dir / f"{example['name']}.gif"
            save_file(gif_bytes, gif_path)
            
            print(f"✅ 成功: {example['title']} ({len(frames)} 帧)")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n🎉 完成! 成功: {success_count}/{len(examples)}")
    print(f"📁 文件保存在: {output_dir}")

if __name__ == "__main__":
    generate_gif_examples()
