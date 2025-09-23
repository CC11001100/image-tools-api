#!/usr/bin/env python3
"""
主控制器模块
协调各个模块完成示例生成任务
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.oss_client import oss_client

from .config import ExampleConfig
from .image_downloader import ImageDownloader
from .oss_uploader import OSSUploader
from .interface_processor import InterfaceProcessor
from .interface_processor_extended import InterfaceProcessorExtended
from .config_updater import ConfigUpdater


class ExampleGeneratorController:
    """示例生成器主控制器"""
    
    def __init__(self):
        """初始化主控制器"""
        self.project_root = project_root
        self.temp_dir = Path("temp_examples")
        
        # 初始化各个组件
        self.downloader = ImageDownloader(self.temp_dir)
        self.uploader = OSSUploader(oss_client)
        self.processor = InterfaceProcessor(self.downloader, self.uploader)
        self.processor_extended = InterfaceProcessorExtended(self.downloader, self.uploader)
        self.config_updater = ConfigUpdater(self.project_root)
        
        # 获取配置
        self.interfaces = ExampleConfig.get_interface_configs()
        self.config_files = ExampleConfig.get_config_files()
        
        # 生成结果记录
        self.generated_examples: Dict[str, List[Dict]] = {}
    
    def generate_all_examples(self):
        """生成所有示例"""
        print("=" * 60)
        print("开始生成所有接口的示例图片并上传到OSS")
        print("=" * 60)
        
        # 检查OSS连接
        print("\n1. 检查OSS连接...")
        if not self.uploader.check_oss_connection():
            return
        
        # 生成各类示例
        try:
            self._generate_interface_examples()
            
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断操作")
        except Exception as e:
            print(f"\n✗ 生成过程中发生错误: {e}")
        finally:
            # 清理临时文件
            self.downloader.cleanup_temp_files()
        
        # 输出结果
        self._print_results()
        
        # 更新配置文件
        oss_urls = self.uploader.get_uploaded_urls()
        if oss_urls:
            self.config_updater.update_config_files(oss_urls, self.config_files)
    
    def _generate_interface_examples(self):
        """生成各个接口的示例"""
        # 调整大小示例
        if "resize" in self.interfaces:
            examples = self.processor.generate_resize_examples(
                self.interfaces["resize"]["examples"]
            )
            self.generated_examples["resize"] = examples
        
        # 裁剪示例
        if "crop" in self.interfaces:
            examples = self.processor.generate_crop_examples(
                self.interfaces["crop"]["examples"]
            )
            self.generated_examples["crop"] = examples
        
        # 水印示例
        if "watermark" in self.interfaces:
            examples = self.processor.generate_watermark_examples(
                self.interfaces["watermark"]["examples"]
            )
            self.generated_examples["watermark"] = examples
        
        # 滤镜示例
        if "filter" in self.interfaces:
            examples = self.processor_extended.generate_filter_examples(
                self.interfaces["filter"]["examples"]
            )
            self.generated_examples["filter"] = examples
        
        # 变换示例
        if "transform" in self.interfaces:
            examples = self.processor_extended.generate_transform_examples(
                self.interfaces["transform"]["examples"]
            )
            self.generated_examples["transform"] = examples
    
    def _print_results(self):
        """打印生成结果"""
        print("\n" + "=" * 60)
        print("生成完成!")
        print("=" * 60)
        
        total_examples = sum(len(examples) for examples in self.generated_examples.values())
        print(f"总共生成: {total_examples} 个示例")
        
        for interface, examples in self.generated_examples.items():
            print(f"  - {interface}: {len(examples)} 个示例")
        
        oss_urls = self.uploader.get_uploaded_urls()
        print(f"\n总共上传: {len(oss_urls)} 个文件到OSS")
