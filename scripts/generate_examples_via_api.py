#!/usr/bin/env python3
"""
通过HTTP API调用生成示例图片并上传到OSS
"""

import os
import sys
import requests
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.oss_client import OSSClient

# API基础URL
API_BASE_URL = "http://localhost:58888/api"

# 示例配置 - 支持多种接口类型
EXAMPLES_CONFIG = {
    "resize": [
        {
            "name": "800px",
            "description": "等比缩放 - 800px",
            "params": {"width": 800, "quality": 90},
            "seed": "resize-1",
            "interface_name": "resize"
        },
        {
            "name": "500px",
            "description": "等比缩放 - 500px",
            "params": {"width": 500, "quality": 90},
            "seed": "resize-2",
            "interface_name": "resize"
        },
        {
            "name": "400px",
            "description": "小尺寸缩放（400px宽度）",
            "params": {"width": 400, "quality": 90},
            "seed": "resize-3",
            "interface_name": "resize"
        }
    ],
    "crop": [
        {
            "name": "center-square",
            "description": "中心正方形裁剪",
            "params": {"crop_type": "rectangle", "x": 400, "y": 300, "width": 800, "height": 800, "quality": 90},
            "seed": "crop-1",
            "interface_name": "crop"
        },
        {
            "name": "top-banner",
            "description": "顶部横幅裁剪",
            "params": {"crop_type": "rectangle", "x": 0, "y": 0, "width": 1600, "height": 600, "quality": 90},
            "seed": "crop-2",
            "interface_name": "crop"
        },
        {
            "name": "portrait",
            "description": "竖版裁剪",
            "params": {"crop_type": "rectangle", "x": 600, "y": 0, "width": 400, "height": 600, "quality": 90},
            "seed": "crop-3",
            "interface_name": "crop"
        }
    ],
    "watermark": [
        {
            "name": "center-text",
            "description": "中心文字水印",
            "params": {"watermark_text": "SAMPLE", "position": "center", "font_size": 48, "font_color": "#FFFFFF", "opacity": 0.7, "quality": 90},
            "seed": "watermark-1",
            "interface_name": "watermark"
        },
        {
            "name": "bottom-right",
            "description": "右下角水印",
            "params": {"watermark_text": "© 2024", "position": "bottom-right", "font_size": 24, "font_color": "#000000", "opacity": 0.8, "quality": 90},
            "seed": "watermark-2",
            "interface_name": "watermark"
        }
    ],
    "filter": [
        {
            "name": "blur",
            "description": "模糊效果",
            "params": {"filter_type": "blur", "intensity": 0.6},
            "seed": "filter-1",
            "interface_name": "filter"
        },
        {
            "name": "sharpen",
            "description": "锐化效果",
            "params": {"filter_type": "sharpen", "intensity": 0.8},
            "seed": "filter-2",
            "interface_name": "filter"
        },
        {
            "name": "emboss",
            "description": "浮雕效果",
            "params": {"filter_type": "emboss", "intensity": 1.0},
            "seed": "filter-3",
            "interface_name": "filter"
        }
    ],
    "transform": [
        {
            "name": "rotate-45",
            "description": "旋转45度",
            "params": {"transform_type": "rotate", "angle": 45, "quality": 90},
            "seed": "transform-1",
            "interface_name": "transform"
        },
        {
            "name": "flip-horizontal",
            "description": "水平翻转",
            "params": {"transform_type": "flip-horizontal", "quality": 90},
            "seed": "transform-2",
            "interface_name": "transform"
        },
        {
            "name": "rotate-90-cw",
            "description": "顺时针旋转90度",
            "params": {"transform_type": "rotate-90-cw", "quality": 90},
            "seed": "transform-3",
            "interface_name": "transform"
        }
    ]
}

def download_image(seed, width=1600, height=2400):
    """下载随机图片"""
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content

def call_api_with_file(endpoint, image_data, params):
    """通过文件上传调用API接口处理图片"""
    url = f"{API_BASE_URL}/{endpoint}"

    # 根据接口类型确定文件参数名
    file_param_name = 'image' if 'watermark' in endpoint else 'file'

    # 准备文件数据
    files = {file_param_name: ('image.jpg', image_data, 'image/jpeg')}

    # 添加认证头 - 使用API Token
    api_token = "aigc-hub-781bd81e809c4c7d875fc7a355972432"

    # 设置Authorization头
    headers = {
        'Authorization': api_token
    }

    # 发送请求
    response = requests.post(url, files=files, data=params, headers=headers, timeout=60)

    if response.status_code == 200:
        # 检查响应类型
        content_type = response.headers.get('content-type', '')

        if 'application/json' in content_type:
            # JSON响应 - resize, crop, filter, watermark接口
            result = response.json()
            if result.get('code') == 200 and result.get('data', {}).get('file', {}).get('url'):
                # 从响应中获取处理后图片的URL
                processed_image_url = result['data']['file']['url']
                # 下载处理后的图片
                img_response = requests.get(processed_image_url, timeout=60)
                img_response.raise_for_status()
                return img_response.content
            elif result.get('code') == 200 and result.get('data', {}).get('image_data'):
                # base64编码的图片数据 - transform接口
                import base64
                return base64.b64decode(result['data']['image_data'])
            else:
                raise Exception(f"API响应格式错误: {result}")
        else:
            # 直接返回图片数据
            return response.content
    else:
        raise Exception(f"API调用失败: {response.status_code} - {response.text}")

def main():
    print("=" * 60)
    print("开始通过HTTP API生成示例图片并上传到OSS")
    print("=" * 60)
    
    # 初始化OSS客户端
    print("\n1. 检查OSS连接...")
    try:
        oss_client = OSSClient()
        print("✓ OSS连接成功，目标存储桶:", oss_client.bucket_name)
    except Exception as e:
        print(f"✗ OSS连接失败: {e}")
        return
    
    # 创建临时目录
    temp_dir = Path("temp_examples")
    temp_dir.mkdir(exist_ok=True)
    
    total_examples = 0
    total_files = 0
    
    try:
        # 处理每种接口类型
        for api_endpoint, examples in EXAMPLES_CONFIG.items():
            interface_name = examples[0]['interface_name']
            print(f"\n=== 生成{interface_name}示例 ===")

            for i, example in enumerate(examples, 1):
                print(f"\n生成示例 {i}/{len(examples)}: {example['name']}")

                try:
                    # 下载原图
                    print(f"正在下载图片: https://picsum.photos/seed/{example['seed']}/1600/2400")
                    original_data = download_image(example['seed'])

                    # 保存原图到临时文件
                    original_path = temp_dir / f"original-{example['name']}.jpg"
                    with open(original_path, 'wb') as f:
                        f.write(original_data)
                    print(f"✓ 原图已保存: {original_path}")

                    # 调用API处理图片
                    print(f"正在调用API: /api/v1/{api_endpoint}")
                    processed_data = call_api_with_file(f"v1/{api_endpoint}", original_data, example['params'])

                    # 保存处理后的图片
                    processed_path = temp_dir / f"{interface_name}-{example['name']}.jpg"
                    with open(processed_path, 'wb') as f:
                        f.write(processed_data)
                    print(f"✓ 效果图已生成: {processed_path}")

                    # 上传原图到OSS
                    original_oss_key = f"{interface_name}/original-{example['name']}.jpg"
                    original_url = oss_client.upload_file(str(original_path), original_oss_key)
                    print(f"✓ 原图已上传到OSS: {original_url}")

                    # 上传处理后的图片到OSS
                    processed_oss_key = f"{interface_name}/{interface_name}-{example['name']}.jpg"
                    processed_url = oss_client.upload_file(str(processed_path), processed_oss_key)
                    print(f"✓ 效果图已上传到OSS: {processed_url}")

                    total_examples += 1
                    total_files += 2

                except Exception as e:
                    print(f"✗ 处理示例失败: {e}")
                    continue
        
        print(f"\n✓ 已清理临时目录: {temp_dir}")
        shutil.rmtree(temp_dir)
        
        print("\n" + "=" * 60)
        print("生成完成!")
        print("=" * 60)
        print(f"总共生成: {total_examples} 个示例")
        print(f"总共上传: {total_files} 个文件到OSS")
        
    except Exception as e:
        print(f"\n✗ 处理过程中出现错误: {e}")
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
