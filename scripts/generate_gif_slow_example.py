#!/usr/bin/env python3
"""
补充生成慢速GIF创建示例（之前失败的那个）
"""

import sys
import os
import io
from pathlib import Path
from PIL import Image

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.oss_client import oss_client
from app.services.gif_service import GifService

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    print(f"📤 上传到OSS: {filename}")
    oss_client.upload_bytes(image_bytes, filename)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{filename}"

def main():
    """生成慢速GIF示例"""
    print("🎬 生成慢速GIF创建示例...")
    
    # 使用本地已有的图片
    local_images = [
        "frontend/public/examples/sample-image-1.jpg",
        "frontend/public/examples/sample-image-2.jpg"
    ]
    
    frames = []
    
    # 加载本地图片
    for image_path in local_images:
        if not Path(image_path).exists():
            print(f"❌ 图片文件不存在: {image_path}")
            continue
        
        with Image.open(image_path) as img:
            # 调整为1080x1920
            resized = img.resize((1080, 1920), Image.Resampling.LANCZOS)
            if resized.mode != 'RGB':
                resized = resized.convert('RGB')
            frames.append(resized.copy())
    
    if len(frames) < 2:
        print("❌ 帧数不足")
        return
    
    print(f"✅ 已准备 {len(frames)} 帧图片")
    
    # 保存并上传第一帧作为原图
    first_frame_bytes = io.BytesIO()
    frames[0].save(first_frame_bytes, format='JPEG', quality=95)
    frame_url = upload_to_oss(first_frame_bytes.getvalue(), "create-gif/frame-slow-1.jpg")
    print(f"✅ 原图上传成功: {frame_url}")
    
    # 创建慢速GIF
    print("🎬 创建慢速GIF: 间隔1000ms")
    gif_bytes = GifService.images_to_gif(
        frames,
        duration=1000,
        loop=0,
        optimize=True
    )
    
    # 上传GIF
    gif_url = upload_to_oss(gif_bytes, "create-gif/create-gif-slow.gif")
    print(f"✅ GIF上传成功: {gif_url}")
    
    print("\n🎉 慢速GIF示例生成完成！")

if __name__ == "__main__":
    main()
