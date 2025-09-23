#!/usr/bin/env python3
"""
接口处理器扩展模块
包含滤镜和变换处理方法
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.filter_service import FilterService
from app.services.transform_service import TransformService

from .image_downloader import ImageDownloader
from .oss_uploader import OSSUploader


class InterfaceProcessorExtended:
    """接口处理器扩展类"""
    
    def __init__(self, downloader: ImageDownloader, uploader: OSSUploader):
        """
        初始化接口处理器扩展
        
        Args:
            downloader: 图片下载器实例
            uploader: OSS上传器实例
        """
        self.downloader = downloader
        self.uploader = uploader
    
    def generate_filter_examples(self, examples_config: List[Dict]) -> List[Dict]:
        """生成滤镜示例"""
        print("\n=== 生成滤镜示例 ===")
        examples = []

        for i, example in enumerate(examples_config):
            print(f"\n生成示例 {i+1}/{len(examples_config)}: {example['name']}")

            # 下载原图
            original_filename = f"original-{example['name']}"
            seed = f"filter-{i+1}"
            original_path = self.downloader.download_random_image(original_filename, seed=seed)
            if not original_path:
                continue

            try:
                # 读取原图
                with open(original_path, 'rb') as f:
                    image_bytes = f.read()

                # 调用滤镜服务
                processed_bytes = FilterService.apply_filter(
                    image_bytes,
                    filter_type=example["params"]["filter_type"],
                    intensity=example["params"]["intensity"]
                )

                # 保存处理后的图片
                processed_filename = f"filter-{example['name']}"
                processed_path = self.downloader.temp_dir / f"{processed_filename}.jpg"
                with open(processed_path, 'wb') as f:
                    f.write(processed_bytes)

                print(f"✓ 效果图已生成: {processed_path}")

                # 上传到OSS
                original_oss_url = self.uploader.upload_to_oss(original_path, f"filter/{original_filename}.jpg")
                processed_oss_url = self.uploader.upload_to_oss(processed_path, f"filter/{processed_filename}.jpg")

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
    
    def generate_transform_examples(self, examples_config: List[Dict]) -> List[Dict]:
        """生成变换示例"""
        print("\n=== 生成变换示例 ===")
        examples = []

        for i, example in enumerate(examples_config):
            print(f"\n生成示例 {i+1}/{len(examples_config)}: {example['name']}")

            # 下载原图
            original_filename = f"original-{example['name']}"
            seed = f"transform-{i+1}"
            original_path = self.downloader.download_random_image(original_filename, seed=seed)
            if not original_path:
                continue

            try:
                # 读取原图
                with open(original_path, 'rb') as f:
                    image_bytes = f.read()

                # 调用变换服务
                if "angle" in example["params"]:
                    processed_bytes = TransformService.rotate_image(
                        image_bytes,
                        angle=example["params"]["angle"],
                        expand=example["params"].get("expand", True),
                        fill_color=example["params"].get("fill_color", "white")
                    )
                elif example["params"].get("flip_horizontal"):
                    processed_bytes = TransformService.flip_horizontal(image_bytes)
                elif example["params"].get("flip_vertical"):
                    processed_bytes = TransformService.flip_vertical(image_bytes)
                else:
                    continue

                # 保存处理后的图片
                processed_filename = f"transform-{example['name']}"
                processed_path = self.downloader.temp_dir / f"{processed_filename}.jpg"
                with open(processed_path, 'wb') as f:
                    f.write(processed_bytes)

                print(f"✓ 效果图已生成: {processed_path}")

                # 上传到OSS
                original_oss_url = self.uploader.upload_to_oss(original_path, f"transform/{original_filename}.jpg")
                processed_oss_url = self.uploader.upload_to_oss(processed_path, f"transform/{processed_filename}.jpg")

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
