#!/usr/bin/env python3
"""
生成完整的艺术滤镜示例图片
包含任务要求的6种效果：油画、水彩、素描、卡通、复古、梦幻
"""

import sys
import os
import requests
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import OSSClient
from app.services.filters.artistic_filters import ArtisticFilters

# 初始化OSS客户端
oss_client = OSSClient()

def generate_original_image(seed, filename):
    """生成1080x1920的原图"""
    url = f"https://picsum.photos/seed/{seed}/1080/1920"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes, filename):
    """上传图片到OSS"""
    try:
        url = oss_client.upload_bytes(image_bytes, filename)
        return url
    except Exception as e:
        print(f"OSS上传失败: {e}")
        return None

def generate_art_filter_examples():
    """生成艺术滤镜示例"""
    print("🎨 生成艺术滤镜示例图片...")
    
    examples = [
        {
            'title': '水彩效果',
            'name': 'watercolor',
            'filter_type': 'watercolor',
            'intensity': 0.8,
            'seed': 'watercolor-art-2024',
            'description': '将图片转换为水彩画风格，呈现柔和的色彩过渡和自然的晕染效果'
        },
        {
            'title': '卡通效果',
            'name': 'cartoon',
            'filter_type': 'cartoon',
            'intensity': 0.9,
            'seed': 'cartoon-art-2024',
            'description': '将图片转换为卡通风格，色彩鲜艳，线条清晰'
        },
        {
            'title': '复古效果',
            'name': 'vintage',
            'filter_type': 'vintage',
            'intensity': 0.7,
            'seed': 'vintage-art-2024',
            'description': '添加复古怀旧色调，营造经典的胶片摄影氛围'
        },
        {
            'title': '梦幻效果',
            'name': 'dreamy',
            'filter_type': 'dreamy',
            'intensity': 0.6,
            'seed': 'dreamy-art-2024',
            'description': '创造柔和梦幻的视觉效果，增加朦胧美感'
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 生成原图
            print(f"生成原图: seed={example['seed']}")
            original_bytes = generate_original_image(example['seed'], f"original-{example['name']}.jpg")
            
            # 上传原图
            original_filename = f"art-filter/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue
            
            print(f"✅ 原图上传成功: {original_url}")
            
            # 生成艺术滤镜效果
            print(f"生成艺术滤镜: {example['filter_type']}, intensity={example['intensity']}")
            processed_bytes = ArtisticFilters.apply_filter(
                image_bytes=original_bytes,
                filter_type=example['filter_type'],
                intensity=example['intensity'],
                quality=90
            )
            
            # 上传处理后的图片
            processed_filename = f"art-filter/art-filter-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_filename)
            
            if processed_url:
                print(f"✅ 效果图上传成功: {processed_url}")
                success_count += 1
            else:
                print(f"❌ 效果图上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出配置更新信息
    print("\n📝 请将以下配置添加到 frontend/src/config/examples/artFilterExamples.ts:")
    print("=" * 60)
    
    for example in examples:
        original_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/original-{example['name']}.jpg"
        processed_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-filter-{example['name']}.jpg"
        
        print(f"""  {{
    title: "{example['title']}",
    description: "{example['description']}",
    originalImage: "{original_url}",
    processedImage: "{processed_url}",
    parameters: [
      {{ label: "滤镜类型", value: "{example['title']}" }},
      {{ label: "强度", value: "{int(example['intensity'] * 100)}%" }},
      {{ label: "质量", value: "90" }}
    ],
    apiParams: {{
      endpoint: "/api/v1/art-filter",
      filter_type: "{example['filter_type']}",
      intensity: {example['intensity']},
      quality: 90
    }}
  }},""")
    
    print("=" * 60)
    
    if success_count == len(examples):
        print("\n🎉 所有艺术滤镜示例生成成功！")
        print("现在art-filter页面将包含完整的6种艺术效果")
    else:
        print(f"\n⚠️  部分示例生成失败，成功率: {success_count}/{len(examples)}")

def main():
    """主函数"""
    print("🚀 开始生成艺术滤镜示例...")
    print("=" * 60)
    
    generate_art_filter_examples()
    
    print("\n" + "=" * 60)
    print("🎉 艺术滤镜示例生成完成！")

if __name__ == "__main__":
    main()
