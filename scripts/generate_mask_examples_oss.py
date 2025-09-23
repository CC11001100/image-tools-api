#!/usr/bin/env python3
"""
生成遮罩页面的OSS示例图片
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
from app.services.mask_service import MaskService

def download_image(url: str) -> bytes:
    """下载图片并返回字节数据"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_oss(image_bytes: bytes, filename: str) -> str:
    """上传图片到OSS并返回URL"""
    file_key = f"image-tools-api/examples/mask/{filename}"
    print(f"上传到OSS: {file_key}")
    
    oss_client.upload_bytes(image_bytes, file_key)
    return f"https://aigchub-static.oss-cn-beijing.aliyuncs.com/{file_key}"

def process_mask_image(image_bytes: bytes, mask_type: str, **kwargs) -> bytes:
    """处理遮罩效果"""
    mask_service = MaskService()
    return mask_service.apply_mask(
        image_bytes=image_bytes,
        mask_type=mask_type,
        quality=90,
        **kwargs
    )

def main():
    """主函数"""
    print("开始生成遮罩效果示例图片...")
    
    # 定义3个示例
    examples = [
        {
            "name": "circle",
            "mask_type": "circle",
            "seed": 5001,
            "title": "圆形遮罩",
            "description": "将图片裁剪为圆形",
            "params": {}
        },
        {
            "name": "rounded",
            "mask_type": "rounded_rectangle",
            "seed": 5002,
            "title": "圆角矩形",
            "description": "将图片裁剪为圆角矩形",
            "params": {"radius": 20}
        },
        {
            "name": "gradient",
            "mask_type": "gradient",
            "seed": 5003,
            "title": "渐变遮罩",
            "description": "应用渐变透明度遮罩",
            "params": {"direction": "radial"}
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
            original_url = upload_to_oss(image_bytes, f"original-{example['name']}.jpg")
            
            # 处理遮罩
            print(f"处理图片: {example['mask_type']} 遮罩")
            processed_bytes = process_mask_image(image_bytes, example['mask_type'], **example['params'])
            
            # 上传处理后的图片
            processed_url = upload_to_oss(processed_bytes, f"mask-{example['name']}.jpg")
            
            print(f"✅ 成功生成: {example['title']}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败: {example['title']} - {str(e)}")
            continue
    
    print(f"\n🎉 遮罩效果示例生成完成!")
    print(f"成功生成: {success_count}/{len(examples)} 个示例")
    
    if success_count > 0:
        print(f"\n📸 生成的示例:")
        for i, example in enumerate(examples[:success_count]):
            print(f"📸 {example['title']}:")
            print(f"   原图: https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-{example['name']}.jpg")
            print(f"   遮罩图: https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-{example['name']}.jpg")

if __name__ == '__main__':
    main()
