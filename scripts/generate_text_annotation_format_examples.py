#!/usr/bin/env python3
"""
生成text、annotation、format页面的OSS示例图片
"""

import sys
import os
import requests
import io
from PIL import Image
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.oss_client import oss_client
from app.services.text_service_backup import TextService
from app.services.annotation_service_backup import AnnotationService
from app.services.format_service import FormatService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    print(f"上传到OSS: {filename}")
    oss_client.upload_bytes(image_bytes, filename)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/{filename}"

def generate_text_examples():
    """生成text页面示例"""
    print("\n📝 生成Text页面示例...")
    
    examples = [
        {
            'title': '简单文字',
            'name': 'simple',
            'seed': 'text-simple-001',
            'params': {
                'text': '示例文字',
                'font_size': 48,
                'color': '#FFFFFF',
                'position': 'center'
            }
        },
        {
            'title': '阴影文字',
            'name': 'shadow',
            'seed': 'text-shadow-002',
            'params': {
                'text': '阴影效果',
                'font_size': 56,
                'color': '#FF0000',
                'position': 'center',
                'shadow': True
            }
        },
        {
            'title': '描边文字',
            'name': 'stroke',
            'seed': 'text-stroke-003',
            'params': {
                'text': '描边文字',
                'font_size': 52,
                'color': '#00FF00',
                'position': 'center',
                'stroke': True
            }
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            print(f"下载图片: https://picsum.photos/seed/{example['seed']}/800/800")
            image_bytes = download_image(f"https://picsum.photos/seed/{example['seed']}/800/800")
            
            # 上传原图
            original_url = upload_to_oss(image_bytes, f"text/original-{example['name']}.jpg")
            
            # 处理文字添加
            print(f"处理图片: {example['params']['text']} 文字")
            processed_bytes = TextService.add_text(
                image_bytes=image_bytes,
                text=example['params']['text'],
                position=example['params']['position'],
                font_size=example['params']['font_size'],
                font_color=example['params']['color']
            )
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"text/text-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nText示例生成完成！成功: {success_count}/{len(examples)}")

def generate_annotation_examples():
    """生成annotation页面示例"""
    print("\n📍 生成Annotation页面示例...")
    
    examples = [
        {
            'title': '箭头标注',
            'name': 'arrow',
            'seed': 'annotation-arrow-001',
            'params': {
                'annotation_type': 'arrow',
                'color': '#FF0000',
                'position': '100,100',
                'size': 1.0
            }
        },
        {
            'title': '文字标注',
            'name': 'text',
            'seed': 'annotation-text-002',
            'params': {
                'annotation_type': 'text',
                'text': '标注文字',
                'color': '#000000',
                'position': '150,150',
                'size': 1.5
            }
        },
        {
            'title': '形状标注',
            'name': 'shape',
            'seed': 'annotation-shape-003',
            'params': {
                'annotation_type': 'rectangle',
                'color': '#0000FF',
                'position': '50,50',
                'size': 2.0
            }
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            print(f"下载图片: https://picsum.photos/seed/{example['seed']}/800/800")
            image_bytes = download_image(f"https://picsum.photos/seed/{example['seed']}/800/800")
            
            # 上传原图
            original_url = upload_to_oss(image_bytes, f"annotation/original-{example['name']}.jpg")
            
            # 处理标注添加
            print(f"处理图片: {example['params']['annotation_type']} 标注")
            processed_bytes = AnnotationService.add_annotation(
                image_bytes=image_bytes,
                **example['params']
            )
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"annotation/annotation-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nAnnotation示例生成完成！成功: {success_count}/{len(examples)}")

def generate_format_examples():
    """生成format页面示例"""
    print("\n🔄 生成Format页面示例...")
    
    examples = [
        {
            'title': 'JPEG转PNG',
            'name': 'jpg-to-png',
            'seed': 'format-jpg-001',
            'params': {'target_format': 'PNG', 'quality': 90}
        },
        {
            'title': 'PNG转WEBP',
            'name': 'png-to-webp',
            'seed': 'format-png-002',
            'params': {'target_format': 'WEBP', 'quality': 85}
        },
        {
            'title': 'WEBP转JPEG',
            'name': 'webp-to-jpg',
            'seed': 'format-webp-003',
            'params': {'target_format': 'JPEG', 'quality': 90}
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载原图
            print(f"下载图片: https://picsum.photos/seed/{example['seed']}/800/800")
            image_bytes = download_image(f"https://picsum.photos/seed/{example['seed']}/800/800")
            
            # 上传原图
            original_url = upload_to_oss(image_bytes, f"format/original-{example['name']}.jpg")
            
            # 处理格式转换
            print(f"处理图片: {example['params']['target_format']} 格式转换")
            processed_bytes = FormatService.convert_format(
                image_bytes=image_bytes,
                **example['params']
            )
            
            # 确定文件扩展名
            ext = example['params']['target_format'].lower()
            if ext == 'jpeg':
                ext = 'jpg'
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"format/format-{example['name']}.{ext}")
            
            print(f"✅ 成功生成: {example['title']}")
            print(f"   原图: {original_url}")
            print(f"   效果: {processed_url}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\nFormat示例生成完成！成功: {success_count}/{len(examples)}")

def main():
    """主函数"""
    print("🚀 开始生成text、annotation、format页面示例图片...")
    
    # 生成各页面示例
    generate_text_examples()
    generate_annotation_examples()
    generate_format_examples()
    
    print("\n🎉 所有示例生成完成！")

if __name__ == "__main__":
    main()
