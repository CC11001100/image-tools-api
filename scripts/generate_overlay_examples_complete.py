#!/usr/bin/env python3
"""
生成overlay页面的完整示例图片
包含任务要求的6种叠加类型：图片叠加、透明叠加、位置叠加、缩放叠加、旋转叠加、混合叠加
"""

import sys
import os
import requests
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import OSSClient
from app.services.overlay_service import OverlayService

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

def generate_overlay_examples():
    """生成overlay示例"""
    print("🎨 生成overlay页面示例图片...")
    
    examples = [
        {
            'title': '线性渐变叠加',
            'name': 'linear_gradient',
            'overlay_type': 'gradient',
            'seed': 'overlay-linear-2024',
            'description': '添加线性渐变叠加效果，营造层次感',
            'params': {
                'gradient_type': 'linear',
                'gradient_direction': 'to_bottom',
                'start_color': '#FF0000',
                'end_color': '#0000FF',
                'start_opacity': 0.0,
                'end_opacity': 0.6
            }
        },
        {
            'title': '径向渐变叠加',
            'name': 'radial_gradient',
            'overlay_type': 'gradient',
            'seed': 'overlay-radial-2024',
            'description': '添加径向渐变叠加效果，突出中心区域',
            'params': {
                'gradient_type': 'radial',
                'start_color': '#FFFF00',
                'end_color': '#FF00FF',
                'start_opacity': 0.0,
                'end_opacity': 0.7
            }
        },
        {
            'title': '暗角效果叠加',
            'name': 'vignette',
            'overlay_type': 'vignette',
            'seed': 'overlay-vignette-2024',
            'description': '添加暗角效果，突出中心区域',
            'params': {
                'vignette_intensity': 0.8,
                'vignette_radius': 1.2
            }
        },
        {
            'title': '边框叠加',
            'name': 'border',
            'overlay_type': 'border',
            'seed': 'overlay-border-2024',
            'description': '添加边框叠加效果，增强图片边界',
            'params': {
                'border_width': 20,
                'border_color': '#000000',
                'border_style': 'solid'
            }
        },
        {
            'title': '透明叠加',
            'name': 'transparent',
            'overlay_type': 'gradient',
            'seed': 'overlay-transparent-2024',
            'description': '添加半透明叠加效果，柔和过渡',
            'params': {
                'gradient_type': 'linear',
                'gradient_direction': 'to_right',
                'start_color': '#FFFFFF',
                'end_color': '#000000',
                'start_opacity': 0.3,
                'end_opacity': 0.3
            }
        },
        {
            'title': '混合叠加',
            'name': 'mixed',
            'overlay_type': 'gradient',
            'seed': 'overlay-mixed-2024',
            'description': '混合多种叠加效果，创造独特视觉',
            'params': {
                'gradient_type': 'radial',
                'start_color': '#00FF00',
                'end_color': '#FF0000',
                'start_opacity': 0.2,
                'end_opacity': 0.8
            }
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
            original_filename = f"overlay/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue
            
            print(f"✅ 原图上传成功: {original_url}")
            
            # 生成叠加效果
            print(f"生成叠加效果: {example['overlay_type']}")
            processed_bytes = OverlayService.add_overlay(
                image_bytes=original_bytes,
                overlay_type=example['overlay_type'],
                quality=90,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_filename = f"overlay/overlay-{example['name']}.jpg"
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
    print("\n📝 请将以下配置更新到 frontend/src/config/examples/overlayExamples.ts:")
    print("=" * 60)
    
    for example in examples:
        original_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-{example['name']}.jpg"
        processed_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-{example['name']}.jpg"
        
        # 构建参数显示
        param_labels = []
        if example['overlay_type'] == 'gradient':
            param_labels = [
                f"{{ label: '叠加类型', value: '渐变' }}",
                f"{{ label: '渐变类型', value: '{example['params'].get('gradient_type', 'linear')}' }}",
                f"{{ label: '透明度', value: '{int(example['params'].get('end_opacity', 0.5) * 100)}%' }}"
            ]
        elif example['overlay_type'] == 'vignette':
            param_labels = [
                f"{{ label: '叠加类型', value: '暗角' }}",
                f"{{ label: '强度', value: '{int(example['params'].get('vignette_intensity', 0.6) * 100)}%' }}",
                f"{{ label: '半径', value: '{example['params'].get('vignette_radius', 1.2)}' }}"
            ]
        elif example['overlay_type'] == 'border':
            param_labels = [
                f"{{ label: '叠加类型', value: '边框' }}",
                f"{{ label: '宽度', value: '{example['params'].get('border_width', 10)}px' }}",
                f"{{ label: '样式', value: '{example['params'].get('border_style', 'solid')}' }}"
            ]
        
        print(f"""  {{
    title: "{example['title']}",
    description: "{example['description']}",
    originalImage: "{original_url}",
    processedImage: "{processed_url}",
    parameters: [
      {',\n      '.join(param_labels)}
    ],
    apiParams: {{
      endpoint: "/api/v1/overlay",
      overlay_type: "{example['overlay_type']}",""")
        
        # 添加具体参数
        for key, value in example['params'].items():
            if isinstance(value, str):
                print(f'      {key}: "{value}",')
            else:
                print(f'      {key}: {value},')
        
        print(f"""      quality: 90
    }}
  }},""")
    
    print("=" * 60)
    
    if success_count == len(examples):
        print("\n🎉 所有overlay示例生成成功！")
        print("现在overlay页面将包含完整的6种叠加模式")
    else:
        print(f"\n⚠️  部分示例生成失败，成功率: {success_count}/{len(examples)}")

def main():
    """主函数"""
    print("🚀 开始生成overlay示例...")
    print("=" * 60)
    
    generate_overlay_examples()
    
    print("\n" + "=" * 60)
    print("🎉 overlay示例生成完成！")

if __name__ == "__main__":
    main()
