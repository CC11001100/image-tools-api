#!/usr/bin/env python3
"""
接口处理器模块
负责调用各种图片处理接口生成示例
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.resize_service import ResizeService
from app.services.crop_service import CropService
from app.services.watermark_service import WatermarkService
from app.services.filter_service import FilterService
from app.services.transform_service import TransformService

from .image_downloader import ImageDownloader
from .oss_uploader import OSSUploader


class InterfaceProcessor:
    """接口处理器类"""
    
    def __init__(self, downloader: ImageDownloader, uploader: OSSUploader):
        """
        初始化接口处理器
        
        Args:
            downloader: 图片下载器实例
            uploader: OSS上传器实例
        """
        self.downloader = downloader
        self.uploader = uploader
    
    def generate_resize_examples(self, examples_config: List[Dict]) -> List[Dict]:
        """生成调整大小示例"""
        print("\n=== 生成调整大小示例 ===")
        examples = []
        
        for i, example in enumerate(examples_config):
            print(f"\n生成示例 {i+1}/{len(examples_config)}: {example['name']}")
            
            # 下载原图
            original_filename = f"original-{example['name']}"
            seed = f"resize-{i+1}"
            original_path = self.downloader.download_random_image(original_filename, seed=seed)
            if not original_path:
                continue
            
            try:
                # 读取原图
                with open(original_path, 'rb') as f:
                    image_bytes = f.read()
                
                # 调用调整大小服务
                processed_bytes = ResizeService.resize_image(
                    image_bytes,
                    width=example["params"].get("width"),
                    height=example["params"].get("height"),
                    maintain_ratio=example["params"].get("maintain_ratio", True),
                    quality=example["params"].get("quality", 90)
                )
                
                # 保存处理后的图片
                processed_filename = f"resize-{example['name']}"
                processed_path = self.downloader.temp_dir / f"{processed_filename}.jpg"
                with open(processed_path, 'wb') as f:
                    f.write(processed_bytes)
                
                print(f"✓ 效果图已生成: {processed_path}")
                
                # 上传到OSS
                original_oss_url = self.uploader.upload_to_oss(original_path, f"resize/{original_filename}.jpg")
                processed_oss_url = self.uploader.upload_to_oss(processed_path, f"resize/{processed_filename}.jpg")
                
                if original_oss_url and processed_oss_url:
                    examples.append({
                        "name": example["name"],
                        "original_url": original_oss_url,
                        "processed_url": processed_oss_url,
                        "params": example["params"]
                    })
                    print(f"✓ 已上传到OSS")
                
            except Exception as e:
                print(f"✗ 生成示例失败: {e}")
                continue
        
        return examples
    
    def generate_crop_examples(self, examples_config: List[Dict]) -> List[Dict]:
        """生成裁剪示例"""
        print("\n=== 生成裁剪示例 ===")
        examples = []
        
        for i, example in enumerate(examples_config):
            print(f"\n生成示例 {i+1}/{len(examples_config)}: {example['name']}")
            
            # 下载原图
            original_filename = f"original-{example['name']}"
            seed = f"crop-{i+1}"
            original_path = self.downloader.download_random_image(original_filename, seed=seed)
            if not original_path:
                continue
            
            try:
                # 读取原图
                with open(original_path, 'rb') as f:
                    image_bytes = f.read()
                
                # 调用裁剪服务
                if example["name"] == "center":
                    processed_bytes = CropService.crop_smart_center(
                        image_bytes,
                        example["params"]["target_width"],
                        example["params"]["target_height"],
                        example["params"]["quality"]
                    )
                else:
                    processed_bytes = CropService.crop_rectangle(
                        image_bytes,
                        example["params"]["x"],
                        example["params"]["y"],
                        example["params"]["width"],
                        example["params"]["height"],
                        example["params"]["quality"]
                    )
                
                # 保存处理后的图片
                processed_filename = f"crop-{example['name']}"
                processed_path = self.downloader.temp_dir / f"{processed_filename}.jpg"
                with open(processed_path, 'wb') as f:
                    f.write(processed_bytes)
                
                print(f"✓ 效果图已生成: {processed_path}")
                
                # 上传到OSS
                original_oss_url = self.uploader.upload_to_oss(original_path, f"crop/{original_filename}.jpg")
                processed_oss_url = self.uploader.upload_to_oss(processed_path, f"crop/{processed_filename}.jpg")
                
                if original_oss_url and processed_oss_url:
                    examples.append({
                        "name": example["name"],
                        "original_url": original_oss_url,
                        "processed_url": processed_oss_url,
                        "params": example["params"]
                    })
                    print(f"✓ 已上传到OSS")
                
            except Exception as e:
                print(f"✗ 生成示例失败: {e}")
                continue
        
        return examples

    def generate_watermark_examples(self, examples_config: List[Dict]) -> List[Dict]:
        """生成水印示例"""
        print("\n=== 生成水印示例 ===")
        examples = []

        for i, example in enumerate(examples_config):
            print(f"\n生成示例 {i+1}/{len(examples_config)}: {example['name']}")

            # 下载原图
            original_filename = f"original-{example['name']}"
            seed = f"watermark-{i+1}"
            original_path = self.downloader.download_random_image(original_filename, seed=seed)
            if not original_path:
                continue

            try:
                # 读取原图
                with open(original_path, 'rb') as f:
                    image_bytes = f.read()

                # 调用水印服务
                processed_bytes = WatermarkService.add_watermark(
                    image_bytes,
                    text=example["params"]["text"],
                    position=example["params"]["position"],
                    opacity=example["params"]["opacity"],
                    color=example["params"]["color"],
                    font_size=example["params"]["font_size"],
                    angle=example["params"].get("angle", 0)
                )

                # 保存处理后的图片
                processed_filename = f"watermark-{example['name']}"
                processed_path = self.downloader.temp_dir / f"{processed_filename}.jpg"
                with open(processed_path, 'wb') as f:
                    f.write(processed_bytes)

                print(f"✓ 效果图已生成: {processed_path}")

                # 上传到OSS
                original_oss_url = self.uploader.upload_to_oss(original_path, f"watermark/{original_filename}.jpg")
                processed_oss_url = self.uploader.upload_to_oss(processed_path, f"watermark/{processed_filename}.jpg")

                if original_oss_url and processed_oss_url:
                    examples.append({
                        "name": example["name"],
                        "original_url": original_oss_url,
                        "processed_url": processed_oss_url,
                        "params": example["params"]
                    })
                    print(f"✓ 已上传到OSS")

            except Exception as e:
                print(f"✗ 生成示例失败: {e}")
                continue

        return examples
