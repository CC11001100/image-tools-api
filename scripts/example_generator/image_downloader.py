#!/usr/bin/env python3
"""
图片下载器模块
负责从 picsum.photos 下载随机图片
"""

import requests
from pathlib import Path
from typing import Optional


class ImageDownloader:
    """图片下载器类"""
    
    def __init__(self, temp_dir: Path):
        """
        初始化图片下载器
        
        Args:
            temp_dir: 临时目录路径
        """
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(exist_ok=True)
    
    def download_random_image(
        self, 
        filename: str, 
        width: int = 1600, 
        height: int = 2400, 
        seed: Optional[str] = None
    ) -> Optional[Path]:
        """
        从 picsum.photos 下载随机图片
        
        Args:
            filename: 文件名（不含扩展名）
            width: 图片宽度
            height: 图片高度
            seed: 随机种子，用于生成固定的图片
            
        Returns:
            下载成功返回文件路径，失败返回None
        """
        if seed:
            url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
        else:
            url = f"https://picsum.photos/{width}/{height}"
        
        print(f"正在下载图片: {url}")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 保存原图
            original_path = self.temp_dir / f"{filename}.jpg"
            with open(original_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ 原图已保存: {original_path}")
            return original_path
            
        except Exception as e:
            print(f"✗ 下载图片失败: {e}")
            return None
    
    def cleanup_temp_files(self):
        """清理临时文件"""
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                print(f"✓ 已清理临时目录: {self.temp_dir}")
        except Exception as e:
            print(f"⚠️ 清理临时文件失败: {e}")
