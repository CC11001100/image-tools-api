#!/usr/bin/env python3
"""
生成透视校正示例图片的脚本
从 picsum.photos 下载随机图片，通过透视校正接口处理，上传原图和效果图到OSS
"""

import os
import sys
import requests
import json
import time
from pathlib import Path
from typing import Optional, Dict, List

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.perspective_service import PerspectiveService
from app.services.oss_client import oss_client


class PerspectiveExampleGenerator:
    """透视校正示例生成器"""
    
    def __init__(self):
        self.project_root = project_root
        self.temp_dir = Path("temp_perspective_examples")
        self.public_dir = Path("public/examples/perspective")
        
        # 创建目录
        self.temp_dir.mkdir(exist_ok=True)
        self.public_dir.mkdir(parents=True, exist_ok=True)
        
        # 示例配置 - 统一使用手机尺寸1080x1920
        self.examples = [
            {
                "name": "correct-standard",
                "description": "透视校正 - 标准",
                "seed": "perspective-1",
                "width": 1080,
                "height": 1920,
                "points": "[[100,200],[980,180],[950,1700],[50,1720]]",
                "output_width": 800,
                "output_height": 600
            },
            {
                "name": "correct-tilted",
                "description": "透视校正 - 倾斜",
                "seed": "perspective-2",
                "width": 1080,
                "height": 1920,
                "points": "[[150,300],[930,250],[900,1650],[100,1700]]",
                "output_width": 500,
                "output_height": 400
            },
            {
                "name": "auto-document-1",
                "description": "自动文档校正 1",
                "seed": "perspective-3",
                "width": 1080,
                "height": 1920,
                "auto_document": True
            },
            {
                "name": "auto-document-2",
                "description": "自动文档校正 2",
                "seed": "perspective-4",
                "width": 1080,
                "height": 1920,
                "auto_document": True
            },
            {
                "name": "correct-architecture",
                "description": "透视校正 - 建筑",
                "seed": "perspective-5",
                "width": 1080,
                "height": 1920,
                "points": "[[200,100],[880,100],[880,1800],[200,1800]]",
                "output_width": 600,
                "output_height": 800
            },
            {
                "name": "correct-landscape",
                "description": "透视校正 - 景观",
                "seed": "perspective-6",
                "width": 1080,
                "height": 1920,
                "points": "[[100,600],[980,600],[980,1300],[100,1300]]",
                "output_width": 800,
                "output_height": 500
            }
        ]
    
    def download_random_image(self, seed: str, width: int = 1080, height: int = 1920) -> Optional[bytes]:
        """从 picsum.photos 下载随机图片"""
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
        print(f"正在下载图片: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            print(f"✓ 图片下载成功")
            return response.content
        except Exception as e:
            print(f"✗ 下载图片失败: {e}")
            return None
    
    def process_perspective_image(self, image_bytes: bytes, example: Dict) -> Optional[bytes]:
        """处理透视校正"""
        try:
            if example.get("auto_document"):
                # 自动文档校正
                result = PerspectiveService.process_perspective(
                    image_bytes=image_bytes,
                    auto_document=True,
                    quality=90
                )
            else:
                # 手动四点校正
                result = PerspectiveService.process_perspective(
                    image_bytes=image_bytes,
                    points=example["points"],
                    width=example.get("output_width"),
                    height=example.get("output_height"),
                    quality=90
                )
            
            print(f"✓ 透视校正处理成功")
            return result
            
        except Exception as e:
            print(f"✗ 透视校正处理失败: {e}")
            return None
    
    def upload_to_oss(self, file_path: Path, object_key: str) -> Optional[str]:
        """上传文件到OSS"""
        try:
            url = oss_client.upload_file(str(file_path), object_key)
            if url:
                print(f"✓ 上传到OSS成功: {url}")
                return url
            else:
                print(f"✗ 上传到OSS失败")
                return None
        except Exception as e:
            print(f"✗ 上传到OSS失败: {e}")
            return None
    
    def generate_examples(self):
        """生成所有示例"""
        print("=" * 60)
        print("开始生成透视校正示例图片")
        print("=" * 60)
        
        # 检查OSS连接
        try:
            buckets = oss_client.list_buckets()
            print(f"✓ OSS连接成功")
        except Exception as e:
            print(f"✗ OSS连接失败: {e}")
            return
        
        success_count = 0
        total_count = len(self.examples)
        
        for i, example in enumerate(self.examples):
            print(f"\n生成示例 {i+1}/{total_count}: {example['description']}")
            print("-" * 40)
            
            # 下载原图
            original_data = self.download_random_image(
                example["seed"], 
                example["width"], 
                example["height"]
            )
            if not original_data:
                continue
            
            # 保存原图到临时文件
            original_filename = f"perspective-original-{example['name']}.jpg"
            original_path = self.temp_dir / original_filename
            with open(original_path, 'wb') as f:
                f.write(original_data)
            print(f"✓ 原图已保存: {original_path}")
            
            # 处理透视校正
            processed_data = self.process_perspective_image(original_data, example)
            if not processed_data:
                continue
            
            # 保存处理后的图片
            processed_filename = f"{example['name']}.jpg"
            processed_path = self.temp_dir / processed_filename
            with open(processed_path, 'wb') as f:
                f.write(processed_data)
            print(f"✓ 效果图已保存: {processed_path}")
            
            # 上传原图到OSS
            original_oss_key = f"perspective/{original_filename}"
            original_url = self.upload_to_oss(original_path, original_oss_key)
            
            # 上传效果图到OSS
            processed_oss_key = f"perspective/{processed_filename}"
            processed_url = self.upload_to_oss(processed_path, processed_oss_key)
            
            if original_url and processed_url:
                success_count += 1
                print(f"✓ 示例 {example['name']} 生成完成")
            else:
                print(f"✗ 示例 {example['name']} 生成失败")
        
        print(f"\n生成完成: {success_count}/{total_count} 个示例成功")
        
        # 清理临时文件
        self.cleanup_temp_files()
    
    def cleanup_temp_files(self):
        """清理临时文件"""
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                print(f"✓ 临时文件已清理: {self.temp_dir}")
        except Exception as e:
            print(f"✗ 清理临时文件失败: {e}")


def main():
    """主函数"""
    generator = PerspectiveExampleGenerator()
    generator.generate_examples()


if __name__ == "__main__":
    main()
