#!/usr/bin/env python3
"""
生成advanced text页面的OSS示例图片
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
    file_key = f"advanced-text/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{file_key}"

def create_3d_depth_text(image_bytes: bytes) -> bytes:
    """创建3D深度文字效果"""
    img = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
    
    # 创建文字图层
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # 尝试加载字体
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Impact.ttc", 80)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default()
    
    # 计算文字位置
    text = "DEPTH"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2
    
    # 绘制3D深度效果（通过多层偏移实现）
    depth = 20
    for i in range(depth, 0, -1):
        # 深度阴影
        shadow_color = (50, 50, 50, 200 - i * 8)
        draw.text((x + i, y + i), text, font=font, fill=shadow_color)
    
    # 绘制主文字
    draw.text((x, y), text, font=font, fill=(255, 87, 51, 255))  # #FF5733
    
    # 合并图层
    result = Image.alpha_composite(img, txt_layer)
    result = result.convert('RGB')
    
    # 保存并返回
    output = io.BytesIO()
    result.save(output, format='PNG')
    return output.getvalue()

def create_aurora_text(image_bytes: bytes) -> bytes:
    """创建极光文字效果"""
    img = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
    
    # 创建文字图层
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # 尝试加载字体
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 70)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 70)
        except:
            font = ImageFont.load_default()
    
    # 计算文字位置
    text = "AURORA"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2
    
    # 绘制发光效果（多层模糊）
    glow_intensity = 15
    for i in range(glow_intensity, 0, -1):
        glow_color = (76, 175, 80, 100 - i * 5)  # #4CAF50 with varying alpha
        for dx in range(-i, i+1):
            for dy in range(-i, i+1):
                if dx*dx + dy*dy <= i*i:
                    draw.text((x + dx, y + dy), text, font=font, fill=glow_color)
    
    # 绘制主文字
    draw.text((x, y), text, font=font, fill=(76, 175, 80, 255))  # #4CAF50
    
    # 合并图层
    result = Image.alpha_composite(img, txt_layer)
    result = result.convert('RGB')
    
    # 保存并返回
    output = io.BytesIO()
    result.save(output, format='PNG')
    return output.getvalue()

def create_metallic_text(image_bytes: bytes) -> bytes:
    """创建金属质感文字效果"""
    img = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
    
    # 创建文字图层
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # 尝试加载字体
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 75)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 75)
        except:
            font = ImageFont.load_default()
    
    # 计算文字位置
    text = "METAL"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2
    
    # 绘制金属效果（渐变和高光）
    # 底层阴影
    draw.text((x + 3, y + 3), text, font=font, fill=(100, 100, 100, 200))
    
    # 主体金属色
    draw.text((x, y), text, font=font, fill=(192, 192, 192, 255))  # #C0C0C0
    
    # 高光效果
    draw.text((x - 1, y - 1), text, font=font, fill=(255, 255, 255, 150))
    
    # 合并图层
    result = Image.alpha_composite(img, txt_layer)
    result = result.convert('RGB')
    
    # 保存并返回
    output = io.BytesIO()
    result.save(output, format='PNG')
    return output.getvalue()

def main():
    """主函数"""
    print("🚀 开始生成Advanced Text页面示例图片...")
    
    # 定义示例配置
    examples = [
        {
            'name': 'text-3d-depth',
            'title': '3D深度文字',
            'seed': 'advanced-text-3d-001',
            'processor': create_3d_depth_text
        },
        {
            'name': 'text-aurora',
            'title': '极光文字',
            'seed': 'advanced-text-aurora-002',
            'processor': create_aurora_text
        },
        {
            'name': 'text-metallic',
            'title': '金属质感文字',
            'seed': 'advanced-text-metal-003',
            'processor': create_metallic_text
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图 - 使用标准手机尺寸
            print(f"下载图片: https://picsum.photos/seed/{example['seed']}/1080/1920")
            image_bytes = download_image(f"https://picsum.photos/seed/{example['seed']}/1080/1920")
            
            # 上传原图（使用相同图片作为原图和效果图）
            original_url = upload_to_oss(image_bytes, f"{example['name']}.png")
            
            # 处理文字效果
            print(f"处理图片: {example['title']} 效果")
            processed_bytes = example['processor'](image_bytes)
            
            # 上传处理后的图片（覆盖原图，因为配置中原图和效果图是同一个）
            processed_url = upload_to_oss(processed_bytes, f"{example['name']}.png")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   URL: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nAdvanced Text示例生成完成！成功: {success_count}/{len(examples)}")
    
    if success_count > 0:
        print(f"\n🎉 成功生成了 {success_count} 个Advanced Text示例图片！")
        print("现在 http://localhost:58889/text 页面的图片应该可以正常显示了")

if __name__ == "__main__":
    main()
