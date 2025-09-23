#!/usr/bin/env python3
"""
视频转GIF脚本
使用API将下载的短视频转换为GIF图片
"""

import os
import sys
import requests
import json
import base64
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# API配置
API_BASE_URL = "http://localhost:58888"
USERNAME = "13791486931"
PASSWORD = "123456"

class VideoToGifConverter:
    def __init__(self):
        self.session = requests.Session()
    
    def convert_video_to_gif(self, video_path, output_path, fps=10, quality=90, width=None, height=None):
        """转换视频为GIF"""
        try:
            # 准备文件
            with open(video_path, 'rb') as f:
                video_data = f.read()
            
            # 准备请求数据
            files = {
                'file': (os.path.basename(video_path), video_data, 'video/mp4')
            }
            
            data = {
                'fps': fps,
                'quality': quality
            }
            
            if width:
                data['width'] = width
            if height:
                data['height'] = height
            
            # 发送请求
            url = f"{API_BASE_URL}/api/v1/gif"
            response = self.session.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:  # 修正：检查code字段而不是success字段
                    # 解码base64图片数据
                    image_data = result.get("data", {}).get("image_data")
                    if image_data:
                        gif_bytes = base64.b64decode(image_data)

                        # 保存GIF文件
                        with open(output_path, 'wb') as f:
                            f.write(gif_bytes)

                        print(f"成功转换: {video_path} -> {output_path}")
                        return True
                    else:
                        print(f"响应中没有图片数据")
                else:
                    print(f"API返回错误: {result.get('message')}")
            else:
                print(f"请求失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"转换异常: {str(e)}")
            
        return False
    
    def convert_all_videos(self, video_dir, output_dir):
        """转换目录中的所有视频"""
        video_dir = Path(video_dir)
        output_dir = Path(output_dir)
        
        # 确保输出目录存在
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 支持的视频格式
        video_extensions = ['.mp4', '.avi', '.mov', '.webm', '.mkv']
        
        # 查找所有视频文件
        video_files = []
        for ext in video_extensions:
            video_files.extend(video_dir.glob(f'*{ext}'))
        
        if not video_files:
            print(f"在 {video_dir} 中没有找到视频文件")
            return
        
        print(f"找到 {len(video_files)} 个视频文件")
        
        # 转换每个视频
        success_count = 0
        for video_file in video_files:
            output_file = output_dir / f"{video_file.stem}.gif"
            
            print(f"\n正在转换: {video_file.name}")
            
            # 根据文件名设置不同的参数
            if "720p" in video_file.name:
                width, height = 640, 360  # 缩小720p视频
                fps = 8
            else:
                width, height = None, None
                fps = 10
            
            if self.convert_video_to_gif(
                video_path=str(video_file),
                output_path=str(output_file),
                fps=fps,
                quality=85,
                width=width,
                height=height
            ):
                success_count += 1
        
        print(f"\n转换完成: {success_count}/{len(video_files)} 个文件成功")

def main():
    """主函数"""
    converter = VideoToGifConverter()

    # 设置路径
    video_dir = project_root / "public" / "examples" / "gif"
    output_dir = video_dir  # 输出到同一目录

    # 转换所有视频
    converter.convert_all_videos(video_dir, output_dir)

if __name__ == "__main__":
    main()
