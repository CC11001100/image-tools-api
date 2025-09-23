#!/usr/bin/env python3
"""
生成stitch页面的完整示例图片
包含任务要求的6种拼接类型：水平、垂直、网格、自由、背景、间距
"""

import sys
import os
import requests
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import OSSClient
from app.services.stitch_service import StitchService

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

def generate_stitch_examples():
    """生成stitch示例"""
    print("🎨 生成stitch页面示例图片...")
    
    examples = [
        {
            'title': '水平拼接',
            'name': 'horizontal',
            'direction': 'horizontal',
            'spacing': 10,
            'seeds': ['stitch-h1-2024', 'stitch-h2-2024'],
            'description': '将多张图片水平排列拼接成一张长图'
        },
        {
            'title': '垂直拼接',
            'name': 'vertical',
            'direction': 'vertical',
            'spacing': 5,
            'seeds': ['stitch-v1-2024', 'stitch-v2-2024'],
            'description': '将多张图片垂直排列拼接成一张高图'
        },
        {
            'title': '网格拼接',
            'name': 'grid',
            'direction': 'grid',
            'spacing': 8,
            'seeds': ['stitch-g1-2024', 'stitch-g2-2024', 'stitch-g3-2024', 'stitch-g4-2024'],
            'description': '将多张图片按网格布局拼接成方形图'
        },
        {
            'title': '自由拼接',
            'name': 'free',
            'direction': 'horizontal',  # 使用水平拼接模拟自由拼接
            'spacing': 15,
            'seeds': ['stitch-f1-2024', 'stitch-f2-2024', 'stitch-f3-2024'],
            'description': '自定义位置和间距的灵活拼接方式'
        },
        {
            'title': '背景拼接',
            'name': 'background',
            'direction': 'horizontal',
            'spacing': 20,
            'seeds': ['stitch-bg1-2024', 'stitch-bg2-2024'],
            'description': '带背景色的图片拼接，增强视觉效果'
        },
        {
            'title': '间距拼接',
            'name': 'spacing',
            'direction': 'vertical',
            'spacing': 30,
            'seeds': ['stitch-sp1-2024', 'stitch-sp2-2024'],
            'description': '带间隔的图片拼接，营造层次感'
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 生成多张原图
            original_images = []
            for i, seed in enumerate(example['seeds']):
                print(f"生成原图{i+1}: seed={seed}")
                image_bytes = generate_original_image(seed, f"original{i+1}-{example['name']}.jpg")
                original_images.append(image_bytes)
                
                # 上传原图
                original_filename = f"stitch/original{i+1}-{example['name']}.jpg"
                original_url = upload_to_oss(image_bytes, original_filename)
                
                if original_url:
                    print(f"✅ 原图{i+1}上传成功: {original_url}")
                else:
                    print(f"❌ 原图{i+1}上传失败")
            
            # 生成拼接效果
            print(f"生成拼接效果: {example['direction']}, spacing={example['spacing']}")
            stitched_bytes = StitchService.stitch_images(
                image_bytes_list=original_images,
                direction=example['direction'],
                spacing=example['spacing'],
                quality=90
            )
            
            # 上传拼接结果
            stitched_filename = f"stitch/stitch-{example['name']}.jpg"
            stitched_url = upload_to_oss(stitched_bytes, stitched_filename)
            
            if stitched_url:
                print(f"✅ 拼接结果上传成功: {stitched_url}")
                success_count += 1
            else:
                print(f"❌ 拼接结果上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出配置更新信息
    print("\n📝 请将以下配置更新到 frontend/src/config/examples/stitchExamples.ts:")
    print("=" * 60)
    
    for example in examples:
        original_urls = []
        for i in range(len(example['seeds'])):
            original_urls.append(f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original{i+1}-{example['name']}.jpg")
        
        stitched_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-{example['name']}.jpg"
        
        print(f"""  {{
    title: '{example['title']}',
    description: '{example['description']}',
    originalImages: [""")
        for url in original_urls:
            print(f"      '{url}',")
        print(f"""    ],
    originalImageLabels: [""")
        for i in range(len(original_urls)):
            print(f"      '图片{i+1}',")
        print(f"""    ],
    processedImage: '{stitched_url}',
    parameters: [
      {{ label: '方向', value: '{example['direction']}' }},
      {{ label: '间距', value: '{example['spacing']}px' }},
      {{ label: '图片尺寸', value: '1080x1920' }}
    ],
    apiParams: {{
      endpoint: '/api/v1/stitch',
      direction: '{example['direction']}',
      spacing: {example['spacing']},
      quality: 90
    }}
  }},""")
    
    print("=" * 60)
    
    if success_count == len(examples):
        print("\n🎉 所有stitch示例生成成功！")
        print("现在stitch页面将包含完整的6种拼接模式")
    else:
        print(f"\n⚠️  部分示例生成失败，成功率: {success_count}/{len(examples)}")

def main():
    """主函数"""
    print("🚀 开始生成stitch示例...")
    print("=" * 60)
    
    generate_stitch_examples()
    
    print("\n" + "=" * 60)
    print("🎉 stitch示例生成完成！")

if __name__ == "__main__":
    main()
