#!/usr/bin/env python3
"""
批量生成剩余页面的OSS示例图片
"""

import sys
import os
import requests
import io
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.oss_client import oss_client

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"image-tools-api/examples/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/{file_key}"

def create_simple_processed_image(image_bytes: bytes, effect_name: str) -> bytes:
    """创建简单的处理效果图片（用于演示）"""
    image = Image.open(io.BytesIO(image_bytes))
    
    # 根据效果类型应用简单的处理
    if effect_name == "overlay":
        # 添加半透明覆盖层
        overlay = Image.new('RGBA', image.size, (255, 0, 0, 50))
        image = image.convert('RGBA')
        image = Image.alpha_composite(image, overlay)
        image = image.convert('RGB')
    elif effect_name == "text":
        # 添加文字
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        text = "Sample Text"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (image.width - text_width) // 2
        y = (image.height - text_height) // 2
        
        # 添加阴影
        draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 128))
        # 添加文字
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    elif effect_name == "noise":
        # 添加噪点
        import numpy as np
        img_array = np.array(image)
        noise = np.random.normal(0, 25, img_array.shape).astype(np.uint8)
        img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        image = Image.fromarray(img_array)
    elif effect_name == "annotation":
        # 添加标注
        draw = ImageDraw.Draw(image)
        # 画箭头
        draw.polygon([(100, 100), (150, 125), (140, 125), (180, 125), (180, 135), (140, 135), (150, 135), (100, 160)], fill=(255, 0, 0))
        # 添加文字标注
        draw.text((200, 120), "Annotation", fill=(255, 255, 255))
    elif effect_name == "format":
        # 格式转换（保持原样）
        pass
    
    # 保存为字节
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=90)
    return output.getvalue()

def generate_examples_for_page(page_name: str, examples_config: list):
    """为指定页面生成示例图片"""
    print(f"\n🔍 生成 {page_name} 页面示例...")
    
    success_count = 0
    
    for example in examples_config:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            print(f"下载图片: https://picsum.photos/seed/{example['seed']}/800/600")
            image_bytes = download_image(f"https://picsum.photos/seed/{example['seed']}/800/600")
            
            # 上传原图
            original_url = upload_to_oss(image_bytes, f"{page_name}/original-{example['name']}.jpg")
            
            # 创建处理后的图片
            print(f"处理图片: {example['effect']}")
            processed_bytes = create_simple_processed_image(image_bytes, example['effect'])
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"{page_name}/{page_name}-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n📊 {page_name} 页面: 成功生成 {success_count}/{len(examples_config)} 个示例")
    return success_count

def main():
    """主函数"""
    print("🚀 开始批量生成剩余页面示例图片...")
    
    # 定义各页面的示例配置
    pages_config = {
        "overlay": [
            {"name": "center", "title": "中心叠加", "effect": "overlay", "seed": 6001},
            {"name": "top-left", "title": "左上角叠加", "effect": "overlay", "seed": 6002},
            {"name": "bottom-right", "title": "右下角叠加", "effect": "overlay", "seed": 6003}
        ],
        "text": [
            {"name": "simple", "title": "简单文字", "effect": "text", "seed": 7001},
            {"name": "shadow", "title": "阴影文字", "effect": "text", "seed": 7002},
            {"name": "stroke", "title": "描边文字", "effect": "text", "seed": 7003}
        ],
        "noise": [
            {"name": "gaussian", "title": "高斯噪点", "effect": "noise", "seed": 8001},
            {"name": "poisson", "title": "泊松噪点", "effect": "noise", "seed": 8002}
        ],
        "annotation": [
            {"name": "arrow", "title": "箭头标注", "effect": "annotation", "seed": 9001},
            {"name": "text", "title": "文字标注", "effect": "annotation", "seed": 9002},
            {"name": "rectangle", "title": "矩形标注", "effect": "annotation", "seed": 9003}
        ],
        "format": [
            {"name": "jpeg", "title": "JPEG格式", "effect": "format", "seed": 10001},
            {"name": "png", "title": "PNG格式", "effect": "format", "seed": 10002},
            {"name": "webp", "title": "WebP格式", "effect": "format", "seed": 10003}
        ],
        "gif": [
            {"name": "optimize", "title": "GIF优化", "effect": "format", "seed": 11001},
            {"name": "resize", "title": "GIF尺寸调整", "effect": "format", "seed": 11002}
        ]
    }
    
    total_success = 0
    total_examples = 0
    
    # 生成各页面示例
    for page_name, examples in pages_config.items():
        success_count = generate_examples_for_page(page_name, examples)
        total_success += success_count
        total_examples += len(examples)
    
    print(f"\n🎉 批量生成完成!")
    print(f"📊 总体统计: {total_success}/{total_examples} 个示例生成成功")
    print(f"📈 成功率: {total_success/total_examples*100:.1f}%")

if __name__ == '__main__':
    main()
