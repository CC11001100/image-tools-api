#!/usr/bin/env python3
"""
验证前端配置文件的结构和内容
检查TypeScript配置文件的语法正确性和数据完整性
"""

import os
import re
import json
from pathlib import Path

def extract_examples_from_ts(file_path):
    """从TypeScript文件中提取示例配置"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取示例数组
        examples = []
        
        # 查找所有图片URL
        url_pattern = r'https://aigchub-static\.oss-cn-beijing\.aliyuncs\.com/[^"\']*\.jpg'
        urls = re.findall(url_pattern, content)
        
        # 查找title
        title_pattern = r"title:\s*['\"]([^'\"]*)['\"]"
        titles = re.findall(title_pattern, content)
        
        # 查找description
        desc_pattern = r"description:\s*['\"]([^'\"]*)['\"]"
        descriptions = re.findall(desc_pattern, content)
        
        # 检查重复路径问题
        duplicate_paths = [url for url in urls if 'image-tools-api/examples/image-tools-api/examples/' in url]
        
        return {
            "file": file_path,
            "titles": titles,
            "descriptions": descriptions,
            "urls": urls,
            "duplicate_paths": duplicate_paths,
            "url_count": len(urls),
            "example_count": len(titles)
        }
        
    except Exception as e:
        return {
            "file": file_path,
            "error": str(e),
            "titles": [],
            "descriptions": [],
            "urls": [],
            "duplicate_paths": [],
            "url_count": 0,
            "example_count": 0
        }

def validate_url_structure(url):
    """验证URL结构是否正确"""
    # 检查是否包含重复路径
    if 'image-tools-api/examples/image-tools-api/examples/' in url:
        return False, "包含重复路径"
    
    # 检查基本结构
    if not url.startswith('https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/'):
        return False, "URL基础路径不正确"
    
    # 检查文件扩展名
    if not url.endswith('.jpg'):
        return False, "文件扩展名不是.jpg"
    
    return True, "URL结构正确"

def main():
    """主验证函数"""
    print("开始验证前端配置文件...")
    
    # 定义要检查的配置文件
    config_files = [
        "frontend/src/config/examples/artFilterExamples.ts",
        "frontend/src/config/examples/blendExamples.ts",
        "frontend/src/config/examples/stitchExamples.ts",
        "frontend/src/config/examples/overlayExamples.ts",
        "frontend/src/config/examples/maskExamples.ts",
        "frontend/src/config/examples/noiseExamples.ts",
        "frontend/src/config/examples/colorExamples.ts",
        "frontend/src/config/examples/annotationExamples.ts",
        "frontend/src/config/examples/formatExamples.ts",
        "frontend/src/config/examples/gifExamples.ts"
    ]
    
    results = []
    total_urls = 0
    total_duplicate_paths = 0
    total_examples = 0
    
    print(f"\n检查 {len(config_files)} 个配置文件...")
    
    for config_file in config_files:
        print(f"\n📁 检查文件: {config_file}")
        
        if not os.path.exists(config_file):
            print(f"  ❌ 文件不存在")
            continue
        
        result = extract_examples_from_ts(config_file)
        results.append(result)
        
        if "error" in result:
            print(f"  ❌ 解析错误: {result['error']}")
            continue
        
        print(f"  📊 示例数量: {result['example_count']}")
        print(f"  🖼️ 图片URL数量: {result['url_count']}")
        
        if result['duplicate_paths']:
            print(f"  ⚠️ 发现重复路径: {len(result['duplicate_paths'])} 个")
            for dup_url in result['duplicate_paths']:
                print(f"    - {dup_url}")
        else:
            print(f"  ✅ 无重复路径问题")
        
        # 验证URL结构
        invalid_urls = []
        for url in result['urls']:
            is_valid, message = validate_url_structure(url)
            if not is_valid:
                invalid_urls.append((url, message))
        
        if invalid_urls:
            print(f"  ⚠️ 发现无效URL: {len(invalid_urls)} 个")
            for url, message in invalid_urls:
                print(f"    - {url}: {message}")
        else:
            print(f"  ✅ 所有URL结构正确")
        
        total_urls += result['url_count']
        total_duplicate_paths += len(result['duplicate_paths'])
        total_examples += result['example_count']
    
    # 输出总结
    print(f"\n=== 验证结果总结 ===")
    print(f"配置文件数: {len(config_files)}")
    print(f"总示例数: {total_examples}")
    print(f"总URL数: {total_urls}")
    print(f"重复路径问题: {total_duplicate_paths} 个")
    
    if total_duplicate_paths == 0:
        print("✅ 所有配置文件都已修复重复路径问题")
    else:
        print("❌ 仍有重复路径问题需要修复")
    
    # 保存详细结果
    with open("config_validation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n详细结果已保存到: config_validation_results.json")
    
    # 生成修复建议
    if total_duplicate_paths > 0:
        print(f"\n=== 修复建议 ===")
        print("发现重复路径问题，建议执行以下修复:")
        for result in results:
            if result.get('duplicate_paths'):
                print(f"\n文件: {result['file']}")
                for dup_url in result['duplicate_paths']:
                    fixed_url = dup_url.replace(
                        'image-tools-api/examples/image-tools-api/examples/',
                        'image-tools-api/examples/'
                    )
                    print(f"  替换: {dup_url}")
                    print(f"  为:   {fixed_url}")

if __name__ == "__main__":
    main()
