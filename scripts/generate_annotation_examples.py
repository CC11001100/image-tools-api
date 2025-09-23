#!/usr/bin/env python3
"""
生成图片标注示例的脚本
从 https://picsum.photos/1080/1920 下载随机图片，然后通过标注接口生成效果图
"""

import os
import sys
import requests
import json
import time
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

class AnnotationExampleGenerator:
    def __init__(self):
        self.api_base_url = "http://localhost:58888"
        self.public_dir = project_root / "frontend" / "public" / "examples" / "annotation"
        self.public_dir.mkdir(parents=True, exist_ok=True)
        
        # 标注示例配置
        self.annotation_examples = [
            {
                "name": "arrow-annotation",
                "title": "箭头标注",
                "description": "添加箭头标注，可以自定义颜色、大小和方向",
                "params": {
                    "annotation_type": "arrow",
                    "color": "#FF0000",
                    "position": "100,100",
                    "size": 1.0,
                    "quality": 90
                }
            },
            {
                "name": "text-annotation", 
                "title": "文字标注",
                "description": "添加文字标注，支持自定义字体、颜色和背景",
                "params": {
                    "annotation_type": "text",
                    "text": "示例文字",
                    "color": "#000000",
                    "position": "150,150",
                    "size": 1.5,
                    "quality": 90
                }
            },
            {
                "name": "shape-annotation",
                "title": "形状标注", 
                "description": "添加矩形或圆形标注，可以自定义边框和填充样式",
                "params": {
                    "annotation_type": "rectangle",
                    "color": "#0000FF",
                    "position": "50,50",
                    "size": 2.0,
                    "quality": 90
                }
            }
        ]

    def download_random_image(self, filename):
        """从 picsum.photos 下载随机图片"""
        print(f"正在下载随机图片: {filename}")
        
        try:
            # 添加随机参数确保每次都是不同的图片
            timestamp = int(time.time() * 1000)
            url = f"https://picsum.photos/1080/1920?random={timestamp}"
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            filepath = self.public_dir / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ 成功下载: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ 下载失败: {e}")
            return None

    def generate_annotation_effect(self, original_image_path, params, output_filename):
        """调用标注接口生成效果图"""
        print(f"正在生成标注效果: {output_filename}")
        
        try:
            url = f"{self.api_base_url}/api/v1/annotation"
            
            # 准备文件和参数
            with open(original_image_path, 'rb') as f:
                files = {'file': f}
                data = params
                
                response = requests.post(url, files=files, data=data, timeout=60)
                response.raise_for_status()
                
                result = response.json()

                if result.get('code') == 200:
                    # 解码base64图片数据
                    import base64
                    image_data = base64.b64decode(result['data']['image_data'])
                    
                    output_path = self.public_dir / output_filename
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"✓ 成功生成效果图: {output_path}")
                    return output_path
                else:
                    print(f"✗ API返回错误: {result.get('message', '未知错误')}")
                    return None
                    
        except Exception as e:
            print(f"✗ 生成效果图失败: {e}")
            return None

    def generate_all_examples(self):
        """生成所有标注示例"""
        print("开始生成图片标注示例...")
        
        generated_examples = []
        
        for i, example in enumerate(self.annotation_examples):
            print(f"\n--- 处理示例 {i+1}/{len(self.annotation_examples)}: {example['title']} ---")
            
            # 下载原图
            original_filename = f"original-{example['name']}.jpg"
            original_path = self.download_random_image(original_filename)
            
            if not original_path:
                print(f"跳过示例 {example['title']}，原图下载失败")
                continue
            
            # 等待一秒确保下次下载的是不同图片
            time.sleep(1)
            
            # 生成效果图
            effect_filename = f"{example['name']}.jpg"
            effect_path = self.generate_annotation_effect(
                original_path, 
                example['params'], 
                effect_filename
            )
            
            if effect_path:
                generated_examples.append({
                    'title': example['title'],
                    'description': example['description'],
                    'originalImage': f'/examples/annotation/{original_filename}',
                    'processedImage': f'/examples/annotation/{effect_filename}',
                    'parameters': [
                        {'label': '标注类型', 'value': example['params']['annotation_type']},
                        {'label': '颜色', 'value': example['params']['color']},
                        {'label': '位置', 'value': example['params']['position']},
                        {'label': '大小', 'value': str(example['params']['size'])}
                    ],
                    'apiParams': example['params']
                })
        
        print(f"\n✓ 成功生成 {len(generated_examples)} 个示例")
        return generated_examples

    def update_config_file(self, examples):
        """更新配置文件"""
        print("\n正在更新配置文件...")
        
        config_path = project_root / "frontend" / "src" / "config" / "examples" / "annotationExamples.ts"
        
        # 生成TypeScript配置内容
        config_content = """import { EffectExample } from '../../types/api';

export const annotationExamples: EffectExample[] = [
"""
        
        for example in examples:
            config_content += f"""  {{
    title: '{example['title']}',
    description: '{example['description']}',
    originalImage: '{example['originalImage']}',
    processedImage: '{example['processedImage']}',
    parameters: [
"""
            for param in example['parameters']:
                config_content += f"      {{ label: '{param['label']}', value: '{param['value']}' }},\n"
            
            config_content += """    ],
    apiParams: {
      endpoint: '/api/annotation',
"""
            for key, value in example['apiParams'].items():
                if isinstance(value, str):
                    config_content += f"      {key}: '{value}',\n"
                else:
                    config_content += f"      {key}: {value},\n"
            
            config_content += """    }
  },
"""
        
        config_content += """];
"""
        
        # 写入文件
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"✓ 配置文件已更新: {config_path}")

def main():
    generator = AnnotationExampleGenerator()
    
    # 检查API服务是否运行
    try:
        response = requests.get(f"{generator.api_base_url}/docs", timeout=5)
        if response.status_code != 200:
            print("❌ API服务未运行，请先启动后端服务")
            return
    except:
        print("❌ 无法连接到API服务，请确保后端服务在 http://localhost:8000 运行")
        return
    
    # 生成示例
    examples = generator.generate_all_examples()
    
    if examples:
        generator.update_config_file(examples)
        print("\n🎉 所有标注示例生成完成！")
    else:
        print("\n❌ 没有成功生成任何示例")

if __name__ == "__main__":
    main()
