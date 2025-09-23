#!/usr/bin/env python3
"""
生成text、annotation、format页面的完整示例图片
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
from app.services.text_service import TextService
from app.services.annotation_service import AnnotationService
from app.services.format_service import FormatService

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

def generate_text_examples():
    """生成text示例"""
    print("📝 生成text页面示例图片...")
    
    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/sample-image-1.jpg",
        "frontend/public/examples/sample-image-2.jpg",
        "frontend/public/examples/sample-image-3.jpg",
        "frontend/public/examples/original-nature.jpg"
    ]
    
    examples = [
        {
            'title': '简单文字',
            'name': 'simple',
            'image_path': local_images[0],
            'description': '在图片上添加简单的文字内容',
            'params': {
                'text': 'Hello World',
                'position': 'center',
                'font_size': 48,
                'font_color': '#FFFFFF'
            }
        },
        {
            'title': '标题文字',
            'name': 'title',
            'image_path': local_images[1],
            'description': '添加大号标题文字',
            'params': {
                'text': '美丽风景',
                'position': 'center',
                'font_size': 64,
                'font_color': '#FFD700'
            }
        },
        {
            'title': '水印文字',
            'name': 'watermark',
            'image_path': local_images[2],
            'description': '添加半透明水印文字',
            'params': {
                'text': '© 2024 Photo',
                'position': 'bottom-right',
                'font_size': 32,
                'font_color': '#FFFFFF'
            }
        },
        {
            'title': '装饰文字',
            'name': 'decorative',
            'image_path': local_images[3],
            'description': '添加装饰性文字效果',
            'params': {
                'text': 'Nature',
                'position': 'center',
                'font_size': 56,
                'font_color': '#00FF00'
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
            original_filename = f"text/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue
            
            print(f"✅ 原图上传成功: {original_url}")
            
            # 生成文字效果
            print(f"生成文字效果: {example['params']['text']}")
            processed_bytes = TextService.add_text(
                image_bytes=original_bytes,
                quality=90,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_filename = f"text/text-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_filename)
            
            if processed_url:
                print(f"✅ 效果图上传成功: {processed_url}")
                success_count += 1
            else:
                print(f"❌ 效果图上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\ntext生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def generate_annotation_examples():
    """生成annotation示例"""
    print("📍 生成annotation页面示例图片...")
    
    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/original-landscape.jpg",
        "frontend/public/examples/watermark/watermark-example-2.jpg",
        "frontend/public/examples/watermark/watermark-example-3.jpg",
        "frontend/public/examples/sample-image-1.jpg"
    ]
    
    examples = [
        {
            'title': '矩形标注',
            'name': 'rectangle',
            'image_path': local_images[0],
            'description': '添加矩形框标注，突出重点区域',
            'params': {
                'annotation_type': 'rectangle',
                'color': '#FF0000',
                'position': '200,300,600,700',
                'size': 1.0
            }
        },
        {
            'title': '圆形标注',
            'name': 'circle',
            'image_path': local_images[1],
            'description': '添加圆形标注，标记重要位置',
            'params': {
                'annotation_type': 'circle',
                'color': '#00FF00',
                'position': '400,600,200',
                'size': 1.0
            }
        },
        {
            'title': '箭头标注',
            'name': 'arrow',
            'image_path': local_images[2],
            'description': '添加箭头指向，引导视线',
            'params': {
                'annotation_type': 'arrow',
                'color': '#0000FF',
                'position': '300,400,500,600',
                'size': 1.0
            }
        },
        {
            'title': '文字标注',
            'name': 'text',
            'image_path': local_images[3],
            'description': '添加文字说明，支持自定义样式',
            'params': {
                'annotation_type': 'text',
                'text': '重要标注',
                'color': '#FFFFFF',
                'position': '400,500',
                'size': 1.0
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
            original_filename = f"annotation/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)
            
            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue
            
            print(f"✅ 原图上传成功: {original_url}")
            
            # 生成标注效果
            print(f"生成标注效果: {example['params']['annotation_type']}")
            processed_bytes = AnnotationService.add_annotation(
                image_bytes=original_bytes,
                quality=90,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_filename = f"annotation/annotation-{example['name']}.jpg"
            processed_url = upload_to_oss(processed_bytes, processed_filename)
            
            if processed_url:
                print(f"✅ 效果图上传成功: {processed_url}")
                success_count += 1
            else:
                print(f"❌ 效果图上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nannotation生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def generate_format_examples():
    """生成format示例"""
    print("🔄 生成format页面示例图片...")

    # 使用现有的本地图片
    local_images = [
        "frontend/public/examples/sample-image-2.jpg",
        "frontend/public/examples/sample-image-3.jpg",
        "frontend/public/examples/original-nature.jpg",
        "frontend/public/examples/original-landscape.jpg",
        "frontend/public/examples/watermark/watermark-example-1.jpg"
    ]

    examples = [
        {
            'title': 'JPEG格式转换',
            'name': 'jpeg',
            'image_path': local_images[0],
            'description': '将图片转换为JPEG格式，适合照片存储',
            'params': {
                'target_format': 'jpeg',
                'quality': 90
            }
        },
        {
            'title': 'PNG格式转换',
            'name': 'png',
            'image_path': local_images[1],
            'description': '将图片转换为PNG格式，保持透明度',
            'params': {
                'target_format': 'png',
                'quality': 90
            }
        },
        {
            'title': 'WebP格式转换',
            'name': 'webp',
            'image_path': local_images[2],
            'description': '将图片转换为WebP格式，更小文件体积',
            'params': {
                'target_format': 'webp',
                'quality': 85
            }
        },
        {
            'title': '高质量JPEG',
            'name': 'jpeg_hq',
            'image_path': local_images[3],
            'description': '转换为高质量JPEG格式',
            'params': {
                'target_format': 'jpeg',
                'quality': 95
            }
        },
        {
            'title': '压缩JPEG',
            'name': 'jpeg_compressed',
            'image_path': local_images[4],
            'description': '转换为压缩JPEG格式，减小文件大小',
            'params': {
                'target_format': 'jpeg',
                'quality': 70
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
            original_filename = f"format/original-{example['name']}.jpg"
            original_url = upload_to_oss(original_bytes, original_filename)

            if not original_url:
                print(f"❌ 原图上传失败: {example['title']}")
                continue

            print(f"✅ 原图上传成功: {original_url}")

            # 生成格式转换效果
            print(f"生成格式转换效果: {example['params']['target_format']}")
            processed_bytes = FormatService.convert_format(
                image_bytes=original_bytes,
                **example['params']
            )

            # 确定文件扩展名
            format_ext = example['params']['target_format']
            if format_ext == 'jpeg':
                format_ext = 'jpg'

            # 上传处理后的图片
            processed_filename = f"format/format-{example['name']}.{format_ext}"
            processed_url = upload_to_oss(processed_bytes, processed_filename)

            if processed_url:
                print(f"✅ 效果图上传成功: {processed_url}")
                success_count += 1
            else:
                print(f"❌ 效果图上传失败: {example['title']}")

        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue

    print(f"\nformat生成完成！成功: {success_count}/{len(examples)}")
    return success_count, len(examples)

def main():
    """主函数"""
    print("🚀 开始生成text、annotation、format示例...")
    print("=" * 60)

    total_success = 0
    total_examples = 0

    # 生成text示例
    text_success, text_total = generate_text_examples()
    total_success += text_success
    total_examples += text_total

    print("\n" + "=" * 60)

    # 生成annotation示例
    annotation_success, annotation_total = generate_annotation_examples()
    total_success += annotation_success
    total_examples += annotation_total

    print("\n" + "=" * 60)

    # 生成format示例
    format_success, format_total = generate_format_examples()
    total_success += format_success
    total_examples += format_total

    print("\n" + "=" * 60)
    print("📋 总体生成结果")
    print("=" * 60)

    overall_success_rate = (total_success / total_examples) * 100 if total_examples > 0 else 0
    print(f"📊 总体成功率: {total_success}/{total_examples} ({overall_success_rate:.1f}%)")

    print(f"\n🎯 生成情况:")
    print(f"✅ text页面: {text_success}/{text_total}")
    print(f"✅ annotation页面: {annotation_success}/{annotation_total}")
    print(f"✅ format页面: {format_success}/{format_total}")

    print("\n" + "=" * 60)
    print("🎉 text、annotation、format示例生成完成！")

if __name__ == "__main__":
    main()
