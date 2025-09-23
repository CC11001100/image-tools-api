#!/usr/bin/env python3
"""
示例生成器配置模块
定义所有接口的示例配置
"""

from typing import Dict, List, Any


class ExampleConfig:
    """示例配置类"""
    
    @staticmethod
    def get_interface_configs() -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """获取所有接口的配置"""
        return {
            "resize": {
                "examples": [
                    {"name": "800px", "params": {"width": 800, "maintain_ratio": True, "quality": 90}},
                    {"name": "500px", "params": {"width": 500, "maintain_ratio": True, "quality": 90}},
                    {"name": "400px", "params": {"width": 400, "maintain_ratio": True, "quality": 90}},
                    {"name": "stretch", "params": {"width": 400, "height": 800, "maintain_ratio": False, "quality": 90}},
                    {"name": "hq-600", "params": {"width": 600, "maintain_ratio": True, "quality": 100}},
                    {"name": "300px", "params": {"width": 300, "maintain_ratio": True, "quality": 90}},
                ]
            },
            "crop": {
                "examples": [
                    {"name": "rectangle", "params": {"x": 100, "y": 100, "width": 400, "height": 300, "quality": 90}},
                    {"name": "square", "params": {"x": 150, "y": 150, "width": 350, "height": 350, "quality": 90}},
                    {"name": "center", "params": {"target_width": 400, "target_height": 300, "quality": 90}},
                ]
            },
            "watermark": {
                "examples": [
                    {"name": "center", "params": {"text": "SAMPLE", "position": "center", "opacity": 0.5, "color": "white", "font_size": 60}},
                    {"name": "corner", "params": {"text": "© 2024", "position": "bottom-right", "opacity": 0.7, "color": "black", "font_size": 40}},
                    {"name": "diagonal", "params": {"text": "WATERMARK", "position": "center", "opacity": 0.3, "color": "red", "font_size": 80, "angle": 45}},
                ]
            },
            "filter": {
                "examples": [
                    {"name": "blur", "params": {"filter_type": "blur", "intensity": 2.0}},
                    {"name": "sharpen", "params": {"filter_type": "sharpen", "intensity": 1.5}},
                    {"name": "emboss", "params": {"filter_type": "emboss", "intensity": 1.0}},
                    {"name": "edge", "params": {"filter_type": "edge_enhance", "intensity": 2.0}},
                ]
            },
            "transform": {
                "examples": [
                    {"name": "rotate-45", "params": {"angle": 45, "expand": True, "fill_color": "white"}},
                    {"name": "rotate-90", "params": {"angle": 90, "expand": True, "fill_color": "white"}},
                    {"name": "flip-h", "params": {"flip_horizontal": True}},
                    {"name": "flip-v", "params": {"flip_vertical": True}},
                ]
            }
        }
    
    @staticmethod
    def get_config_files() -> List[str]:
        """获取需要更新的配置文件列表"""
        return [
            "frontend/src/config/examples/resizeExamples.ts",
            "frontend/src/config/examples/cropExamples.ts",
            "frontend/src/config/examples/watermarkExamples.ts",
            "frontend/src/config/examples/filterExamples.ts",
            "frontend/src/config/examples/transformExamples.ts",
            "frontend/src/config/sampleImageUrls.ts",
            "frontend/src/config/constants.ts",
        ]
