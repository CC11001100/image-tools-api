#!/usr/bin/env python3
"""
重新生成stitch页面的拼接结果
使用新的多张原图生成正确的拼接效果
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

def download_image(url):
    """下载图片"""
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

def regenerate_stitch_results():
    """重新生成拼接结果"""
    print("🔧 重新生成stitch页面拼接结果...")
    
    examples = [
        {
            'title': '水平拼接',
            'name': 'horizontal',
            'direction': 'horizontal',
            'spacing': 10,
            'original_urls': [
                'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-horizontal.jpg',
                'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-horizontal.jpg'
            ]
        },
        {
            'title': '垂直拼接',
            'name': 'vertical',
            'direction': 'vertical',
            'spacing': 5,
            'original_urls': [
                'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-vertical.jpg',
                'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-vertical.jpg'
            ]
        },
        {
            'title': '网格拼接',
            'name': 'grid',
            'direction': 'grid',
            'spacing': 8,
            'original_urls': [
                'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-grid.jpg',
                'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-grid.jpg',
                'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original3-grid.jpg',
                'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original4-grid.jpg'
            ]
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 下载所有原图
            image_bytes_list = []
            for i, url in enumerate(example['original_urls']):
                print(f"下载原图{i+1}: {url}")
                image_bytes = download_image(url)
                image_bytes_list.append(image_bytes)
            
            # 生成拼接结果
            print(f"生成拼接结果: {example['direction']}, spacing={example['spacing']}")
            result_bytes = StitchService.stitch_images(
                image_bytes_list=image_bytes_list,
                direction=example['direction'],
                spacing=example['spacing'],
                quality=90
            )
            
            # 上传拼接结果
            result_filename = f"stitch/stitch-{example['name']}.jpg"
            result_url = upload_to_oss(result_bytes, result_filename)
            
            if result_url:
                print(f"✅ 成功生成: {example['title']}")
                print(f"   结果: {result_url}")
                success_count += 1
            else:
                print(f"❌ 上传失败: {example['title']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n重新生成完成！成功: {success_count}/{len(examples)}")
    
    if success_count == len(examples):
        print("\n🎉 所有拼接结果已更新！")
        print("现在拼接结果使用的是新的多张原图")
    else:
        print(f"\n⚠️  部分拼接结果更新失败")

def main():
    """主函数"""
    print("🚀 开始重新生成stitch拼接结果...")
    print("=" * 60)
    
    regenerate_stitch_results()
    
    print("\n" + "=" * 60)
    print("🎉 拼接结果重新生成完成！")

if __name__ == "__main__":
    main()
