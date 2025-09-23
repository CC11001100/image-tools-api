#!/usr/bin/env python3
"""
生成blend页面的完整示例图片
包含任务要求的6种混合模式：正常、正片叠底、滤色、叠加、颜色减淡、颜色加深
"""

import sys
import os
import requests
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import OSSClient
from app.services.blend_service import BlendService

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

def generate_blend_examples():
    """生成blend示例"""
    print("🎨 生成blend页面示例图片...")
    
    examples = [
        {
            'title': '正常混合',
            'name': 'normal',
            'blend_mode': 'normal',
            'opacity': 0.6,
            'base_seed': 'blend-base-normal-2024',
            'overlay_seed': 'blend-overlay-normal-2024',
            'description': '标准的图层混合，保持自然的叠加效果'
        },
        {
            'title': '正片叠底',
            'name': 'multiply',
            'blend_mode': 'multiply',
            'opacity': 0.75,
            'base_seed': 'blend-base-multiply-2024',
            'overlay_seed': 'blend-overlay-multiply-2024',
            'description': '颜色变暗，产生深色阴影效果'
        },
        {
            'title': '滤色混合',
            'name': 'screen',
            'blend_mode': 'screen',
            'opacity': 0.65,
            'base_seed': 'blend-base-screen-2024',
            'overlay_seed': 'blend-overlay-screen-2024',
            'description': '颜色变亮，产生明亮的光影效果'
        },
        {
            'title': '叠加混合',
            'name': 'overlay',
            'blend_mode': 'overlay',
            'opacity': 0.7,
            'base_seed': 'blend-base-overlay-2024',
            'overlay_seed': 'blend-overlay-overlay-2024',
            'description': '结合正片叠底和滤色，增强对比度'
        },
        {
            'title': '颜色减淡',
            'name': 'color-dodge',
            'blend_mode': 'color-dodge',
            'opacity': 0.55,
            'base_seed': 'blend-base-dodge-2024',
            'overlay_seed': 'blend-overlay-dodge-2024',
            'description': '通过减少对比度来提亮颜色'
        },
        {
            'title': '颜色加深',
            'name': 'color-burn',
            'blend_mode': 'color-burn',
            'opacity': 0.6,
            'base_seed': 'blend-base-burn-2024',
            'overlay_seed': 'blend-overlay-burn-2024',
            'description': '通过增加对比度来加深颜色'
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 生成基础图片
            print(f"生成基础图片: seed={example['base_seed']}")
            base_bytes = generate_original_image(example['base_seed'], f"base-{example['name']}.jpg")
            
            # 生成叠加图片
            print(f"生成叠加图片: seed={example['overlay_seed']}")
            overlay_bytes = generate_original_image(example['overlay_seed'], f"overlay-{example['name']}.jpg")
            
            # 上传基础图片
            base_filename = f"blend/base-{example['name']}.jpg"
            base_url = upload_to_oss(base_bytes, base_filename)
            
            if not base_url:
                print(f"❌ 基础图片上传失败: {example['title']}")
                continue
            
            print(f"✅ 基础图片上传成功: {base_url}")
            
            # 上传叠加图片
            overlay_filename = f"blend/overlay-{example['name']}.jpg"
            overlay_url = upload_to_oss(overlay_bytes, overlay_filename)
            
            if not overlay_url:
                print(f"❌ 叠加图片上传失败: {example['title']}")
                continue
            
            print(f"✅ 叠加图片上传成功: {overlay_url}")
            
            # 生成混合效果
            print(f"生成混合效果: {example['blend_mode']}, opacity={example['opacity']}")
            blended_bytes = BlendService.blend_images(
                base_image_bytes=base_bytes,
                blend_image_bytes=overlay_bytes,
                blend_mode=example['blend_mode'],
                opacity=example['opacity'],
                quality=90
            )
            
            # 上传混合结果
            blended_filename = f"blend/blend-{example['name']}.jpg"
            blended_url = upload_to_oss(blended_bytes, blended_filename)
            
            if blended_url:
                print(f"✅ 混合结果上传成功: {blended_url}")
                success_count += 1
            else:
                print(f"❌ 混合结果上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出配置更新信息
    print("\n📝 请将以下配置更新到 frontend/src/config/examples/blendExamples.ts:")
    print("=" * 60)
    
    for example in examples:
        base_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-{example['name']}.jpg"
        blended_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-{example['name']}.jpg"
        
        print(f"""  {{
    title: "{example['title']}",
    description: "{example['description']}",
    originalImage: "{base_url}",
    processedImage: "{blended_url}",
    parameters: [
      {{ label: "混合模式", value: "{example['title']}" }},
      {{ label: "不透明度", value: "{int(example['opacity'] * 100)}%" }},
      {{ label: "质量", value: "90" }}
    ],
    apiParams: {{
      endpoint: "/api/v1/blend",
      blend_mode: "{example['blend_mode']}",
      opacity: {example['opacity']},
      quality: 90
    }}
  }},""")
    
    print("=" * 60)
    
    if success_count == len(examples):
        print("\n🎉 所有blend示例生成成功！")
        print("现在blend页面将包含完整的6种混合模式")
    else:
        print(f"\n⚠️  部分示例生成失败，成功率: {success_count}/{len(examples)}")

def main():
    """主函数"""
    print("🚀 开始生成blend示例...")
    print("=" * 60)
    
    generate_blend_examples()
    
    print("\n" + "=" * 60)
    print("🎉 blend示例生成完成！")

if __name__ == "__main__":
    main()
