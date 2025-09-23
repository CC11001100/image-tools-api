#!/usr/bin/env python3
"""
生成图片噪点示例的脚本
从 https://picsum.photos/1080/1920 下载随机图片，然后通过噪点接口生成效果图
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

class NoiseExampleGenerator:
    def __init__(self):
        self.api_base_url = "http://localhost:58888"
        self.public_dir = project_root / "frontend" / "public" / "examples" / "noise"
        self.public_dir.mkdir(parents=True, exist_ok=True)
        
        # 噪点示例配置
        self.noise_examples = [
            {
                "name": "gaussian-light",
                "title": "高斯噪点 - 轻微",
                "description": "添加轻微的高斯噪点，模拟传感器噪点",
                "params": {
                    "noise_type": "gaussian",
                    "intensity": 20,
                    "quality": 90
                }
            },
            {
                "name": "gaussian-medium",
                "title": "高斯噪点 - 中等",
                "description": "添加中等强度的高斯噪点",
                "params": {
                    "noise_type": "gaussian",
                    "intensity": 50,
                    "quality": 90
                }
            },
            {
                "name": "gaussian-strong",
                "title": "高斯噪点 - 强烈",
                "description": "添加强烈的高斯噪点，创造特殊视觉效果",
                "params": {
                    "noise_type": "gaussian",
                    "intensity": 80,
                    "quality": 90
                }
            },
            {
                "name": "salt-pepper-light",
                "title": "椒盐噪点 - 轻微",
                "description": "添加轻微的椒盐噪点，模拟老照片效果",
                "params": {
                    "noise_type": "salt_and_pepper",
                    "intensity": 15,
                    "quality": 90
                }
            },
            {
                "name": "salt-pepper-medium",
                "title": "椒盐噪点 - 中等",
                "description": "添加中等强度的椒盐噪点，创造复古感",
                "params": {
                    "noise_type": "salt_and_pepper",
                    "intensity": 35,
                    "quality": 90
                }
            },
            {
                "name": "poisson-effect",
                "title": "泊松噪点",
                "description": "添加泊松噪点，模拟低光照条件",
                "params": {
                    "noise_type": "poisson",
                    "intensity": 40,
                    "quality": 90
                }
            },
            {
                "name": "speckle-effect",
                "title": "斑点噪点",
                "description": "添加斑点噪点，创造颗粒感效果",
                "params": {
                    "noise_type": "speckle",
                    "intensity": 30,
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

    def generate_noise_effect(self, original_image_path, params, output_filename):
        """调用噪点接口生成效果图"""
        print(f"正在生成噪点效果: {output_filename}")
        
        try:
            url = f"{self.api_base_url}/api/v1/noise-test"
            
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
        """生成所有噪点示例"""
        print("开始生成图片噪点示例...")
        
        generated_examples = []
        
        for i, example in enumerate(self.noise_examples):
            print(f"\n--- 处理示例 {i+1}/{len(self.noise_examples)}: {example['title']} ---")
            
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
            effect_path = self.generate_noise_effect(
                original_path, 
                example['params'], 
                effect_filename
            )
            
            if effect_path:
                generated_examples.append({
                    'title': example['title'],
                    'description': example['description'],
                    'originalImage': f'/examples/noise/{original_filename}',
                    'processedImage': f'/examples/noise/{effect_filename}',
                    'parameters': [
                        {'label': '噪点类型', 'value': example['params']['noise_type']},
                        {'label': '强度', 'value': str(example['params']['intensity'])},
                        {'label': '质量', 'value': str(example['params']['quality'])}
                    ],
                    'apiParams': example['params']
                })
        
        print(f"\n✓ 成功生成 {len(generated_examples)} 个示例")
        return generated_examples

    def update_config_file(self, examples):
        """更新配置文件"""
        print("\n正在更新配置文件...")
        
        config_path = project_root / "frontend" / "src" / "config" / "examples" / "noiseExamples.ts"
        
        # 生成TypeScript配置内容
        config_content = """import { EffectExample } from '../../types/api';

export const noiseExamples: EffectExample[] = [
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
      endpoint: '/api/noise',
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
    generator = NoiseExampleGenerator()
    
    # 检查API服务是否运行
    try:
        response = requests.get(f"{generator.api_base_url}/docs", timeout=5)
        if response.status_code != 200:
            print("❌ API服务未运行，请先启动后端服务")
            return
    except:
        print("❌ 无法连接到API服务，请确保后端服务在 http://localhost:58888 运行")
        return
    
    # 生成示例
    examples = generator.generate_all_examples()
    
    if examples:
        generator.update_config_file(examples)
        print("\n🎉 所有噪点示例生成完成！")
    else:
        print("\n❌ 没有成功生成任何示例")

if __name__ == "__main__":
    main()
