#!/usr/bin/env python3
"""
使用本地图片生成mask页面的完整示例图片
包含任务要求的6种遮罩类型：圆形遮罩、矩形遮罩、椭圆遮罩、星形遮罩、心形遮罩、圆角矩形遮罩
"""

import sys
import os
from pathlib import Path
from PIL import Image
import io

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import OSSClient
from app.services.mask_service import MaskService

# 初始化OSS客户端
oss_client = OSSClient()

def resize_image_to_1080x1920(image_path):
    """将图片调整为1080x1920尺寸"""
    with Image.open(image_path) as img:
        # 调整尺寸
        resized = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        
        # 转换为RGB模式（如果需要）
        if resized.mode != 'RGB':
            resized = resized.convert('RGB')
        
        # 转换为字节
        output = io.BytesIO()
        resized.save(output, format='JPEG', quality=95)
        return output.getvalue()

def upload_to_oss(image_bytes, filename):
    """上传图片到OSS"""
    try:
        url = oss_client.upload_bytes(image_bytes, filename)
        return url
    except Exception as e:
        print(f"OSS上传失败: {e}")
        return None

def generate_mask_examples():
    """生成mask示例"""
    print("🎭 生成mask页面示例图片...")
    
    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/sample-image-1.jpg",
        "frontend/public/examples/sample-image-2.jpg", 
        "frontend/public/examples/sample-image-3.jpg",
        "frontend/public/examples/original-nature.jpg",
        "frontend/public/examples/original-landscape.jpg",
        "frontend/public/examples/watermark/watermark-example-2.jpg"
    ]
    
    examples = [
        {
            'title': '圆形遮罩',
            'name': 'circle',
            'mask_type': 'circle',
            'image_path': local_images[0],
            'description': '使用圆形遮罩裁剪图片，创建圆形效果',
            'params': {
                'feather': 10
            }
        },
        {
            'title': '矩形遮罩',
            'name': 'rectangle',
            'mask_type': 'rectangle',
            'image_path': local_images[1],
            'description': '使用矩形遮罩裁剪图片，创建矩形效果',
            'params': {
                'feather': 5
            }
        },
        {
            'title': '椭圆遮罩',
            'name': 'ellipse',
            'mask_type': 'ellipse',
            'image_path': local_images[2],
            'description': '使用椭圆遮罩裁剪图片，创建椭圆效果',
            'params': {
                'feather': 8
            }
        },
        {
            'title': '星形遮罩',
            'name': 'star',
            'mask_type': 'star',
            'image_path': local_images[3],
            'description': '使用星形遮罩裁剪图片，创建星形效果',
            'params': {
                'feather': 5,
                'points': 5
            }
        },
        {
            'title': '心形遮罩',
            'name': 'heart',
            'mask_type': 'heart',
            'image_path': local_images[4],
            'description': '使用心形遮罩裁剪图片，创建心形效果',
            'params': {
                'feather': 8
            }
        },
        {
            'title': '圆角矩形遮罩',
            'name': 'rounded_rectangle',
            'mask_type': 'rounded_rectangle',
            'image_path': local_images[5],
            'description': '使用圆角矩形遮罩裁剪图片，创建圆角效果',
            'params': {
                'feather': 5,
                'radius': 50
            }
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 检查图片文件是否存在
            image_path = Path(example['image_path'])
            if not image_path.exists():
                print(f"❌ 图片文件不存在: {image_path}")
                continue
            
            # 调整图片尺寸为1080x1920
            print(f"调整图片尺寸: {image_path}")
            original_bytes = resize_image_to_1080x1920(image_path)
            
            # 上传原图
            original_filename = f"mask/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue
            
            print(f"✅ 原图上传成功: {original_url}")
            
            # 生成遮罩效果
            print(f"生成遮罩效果: {example['mask_type']}")
            processed_bytes = MaskService.apply_mask(
                image_bytes=original_bytes,
                mask_type=example['mask_type'],
                quality=90,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_filename = f"mask/mask-{example['name']}.jpg"
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
    print("\n📝 请将以下配置更新到 frontend/src/config/examples/maskExamples.ts:")
    print("=" * 60)
    
    for example in examples:
        original_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-{example['name']}.jpg"
        processed_url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-{example['name']}.jpg"
        
        # 构建参数显示
        param_labels = [
            f"{{ label: '遮罩类型', value: '{example['title'].replace('遮罩', '')}' }}",
            f"{{ label: '羽化', value: '{example['params'].get('feather', 0)}px' }}",
            f"{{ label: '质量', value: '90' }}"
        ]
        
        # 添加特殊参数
        if 'points' in example['params']:
            param_labels.insert(1, f"{{ label: '角数', value: '{example['params']['points']}' }}")
        if 'radius' in example['params']:
            param_labels.insert(1, f"{{ label: '圆角半径', value: '{example['params']['radius']}px' }}")
        
        print(f"""  {{
    title: "{example['title']}",
    description: "{example['description']}",
    originalImage: "{original_url}",
    processedImage: "{processed_url}",
    parameters: [
      {',\n      '.join(param_labels)}
    ],
    apiParams: {{
      endpoint: "/api/v1/mask",
      mask_type: "{example['mask_type']}",""")
        
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
        print("\n🎉 所有mask示例生成成功！")
        print("现在mask页面将包含完整的6种遮罩形状")
    else:
        print(f"\n⚠️  部分示例生成失败，成功率: {success_count}/{len(examples)}")

def main():
    """主函数"""
    print("🚀 开始生成mask示例...")
    print("=" * 60)
    
    generate_mask_examples()
    
    print("\n" + "=" * 60)
    print("🎉 mask示例生成完成！")

if __name__ == "__main__":
    main()
