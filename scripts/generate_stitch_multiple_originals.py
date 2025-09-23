#!/usr/bin/env python3
"""
为stitch页面生成多张原图
每个拼接示例需要2张原图来展示拼接效果
"""

import sys
import os
import requests
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import OSSClient

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

def generate_stitch_originals():
    """生成stitch页面的多张原图"""
    print("🔧 生成stitch页面的多张原图...")
    
    examples = [
        {
            'title': '水平拼接',
            'name': 'horizontal',
            'seeds': ['stitch-h1', 'stitch-h2']
        },
        {
            'title': '垂直拼接',
            'name': 'vertical',
            'seeds': ['stitch-v1', 'stitch-v2']
        },
        {
            'title': '网格拼接',
            'name': 'grid',
            'seeds': ['stitch-g1', 'stitch-g2', 'stitch-g3', 'stitch-g4']
        }
    ]
    
    success_count = 0
    
    for example in examples:
        try:
            print(f"\n处理示例: {example['title']}")
            
            # 为每个示例生成多张原图
            for i, seed in enumerate(example['seeds']):
                print(f"生成原图{i+1}: {seed}")
                
                # 下载1080x1920尺寸的图片
                image_url = f"https://picsum.photos/seed/{seed}/1080/1920"
                print(f"下载图片: {image_url}")
                image_bytes = download_image(image_url)
                
                # 上传到OSS
                filename = f"stitch/original{i+1}-{example['name']}.jpg"
                oss_url = upload_to_oss(image_bytes, filename)
                
                if oss_url:
                    print(f"✅ 成功上传原图{i+1}: {oss_url}")
                else:
                    print(f"❌ 上传失败: {filename}")
                    continue
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n生成完成！成功: {success_count}/{len(examples)}")
    
    # 输出URL信息
    print("\n📋 生成的原图URL:")
    for example in examples:
        print(f"\n{example['title']}:")
        for i in range(len(example['seeds'])):
            url = f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original{i+1}-{example['name']}.jpg"
            print(f"  原图{i+1}: {url}")

def main():
    """主函数"""
    print("🚀 开始生成stitch页面多张原图...")
    print("=" * 60)
    
    generate_stitch_originals()
    
    print("\n" + "=" * 60)
    print("🎉 多张原图生成完成！")

if __name__ == "__main__":
    main()
