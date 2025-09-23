#!/usr/bin/env python3
"""
批量更新配置文件中的本地路径为OSS URL
将所有 /examples/ 开头的本地路径替换为对应的OSS URL
"""

import os
import re
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# OSS基础URL
OSS_BASE_URL = "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api"

# 需要更新的配置文件
CONFIG_FILES = [
    "frontend/src/config/constants.ts",
    "frontend/src/config/sampleImageUrls.ts",
    "frontend/src/config/examples/resizeExamples.ts",
    "frontend/src/config/examples/watermarkExamples.ts",
    "frontend/src/config/examples/enhanceExamples.ts",
    "frontend/src/config/examples/maskExamples.ts",
    "frontend/src/config/examples/overlayExamples.ts",
    "frontend/src/config/examples/noiseExamples.ts",
    "frontend/src/config/examples/annotationExamples.ts",
    "frontend/src/config/examples/artFilterExamples.ts",
    "frontend/src/config/examples/stitchShowcaseExamples.ts",
]

def update_single_file(file_path: str) -> bool:
    """
    更新单个配置文件中的本地路径
    
    Args:
        file_path: 配置文件路径
        
    Returns:
        是否有更新
    """
    full_path = project_root / file_path
    
    if not full_path.exists():
        print(f"⚠️  文件不存在: {file_path}")
        return False
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 匹配所有 /examples/ 开头的路径
        # 支持单引号、双引号和反引号
        patterns = [
            r'"/examples/([^"]+)"',
            r"'/examples/([^']+)'",
            r'`/examples/([^`]+)`',
        ]
        
        for pattern in patterns:
            def replace_match(match):
                relative_path = match.group(1)
                oss_url = f"{OSS_BASE_URL}/examples/{relative_path}"
                quote_char = match.group(0)[0]  # 获取引号类型
                return f'{quote_char}{oss_url}{quote_char}'
            
            content = re.sub(pattern, replace_match, content)
        
        # 检查是否有变化
        if content != original_content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已更新: {file_path}")
            return True
        else:
            print(f"➖ 无需更新: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 更新失败: {file_path} - {str(e)}")
        return False

def scan_for_local_paths():
    """扫描所有配置文件中的本地路径"""
    print("🔍 扫描配置文件中的本地路径...")
    
    local_paths = set()
    
    for file_path in CONFIG_FILES:
        full_path = project_root / file_path
        
        if not full_path.exists():
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找所有 /examples/ 路径
            patterns = [
                r'"/examples/([^"]+)"',
                r"'/examples/([^']+)'",
                r'`/examples/([^`]+)`',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    local_paths.add(f"/examples/{match}")
                    
        except Exception as e:
            print(f"❌ 读取文件失败: {file_path} - {str(e)}")
    
    return sorted(local_paths)

def main():
    """主函数"""
    print("=" * 60)
    print("批量更新配置文件中的本地路径为OSS URL")
    print("=" * 60)
    
    # 1. 扫描现有的本地路径
    local_paths = scan_for_local_paths()
    
    if local_paths:
        print(f"\n📋 找到 {len(local_paths)} 个本地路径:")
        for i, path in enumerate(local_paths[:20], 1):  # 只显示前20个
            print(f"  {i:2d}. {path}")
        if len(local_paths) > 20:
            print(f"     ... 还有 {len(local_paths) - 20} 个路径")
    else:
        print("\n✅ 没有找到需要更新的本地路径")
        return
    
    # 2. 确认更新
    print(f"\n🔄 即将更新 {len(CONFIG_FILES)} 个配置文件")
    print(f"📍 OSS基础URL: {OSS_BASE_URL}")
    
    confirm = input("\n是否继续更新? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 更新已取消")
        return
    
    # 3. 执行更新
    print(f"\n🚀 开始更新配置文件...")
    
    updated_count = 0
    for file_path in CONFIG_FILES:
        if update_single_file(file_path):
            updated_count += 1
    
    # 4. 总结
    print(f"\n" + "=" * 60)
    print(f"✅ 更新完成!")
    print(f"📊 更新统计:")
    print(f"   - 检查文件: {len(CONFIG_FILES)} 个")
    print(f"   - 更新文件: {updated_count} 个")
    print(f"   - 本地路径: {len(local_paths)} 个")
    print("=" * 60)
    
    if updated_count > 0:
        print("\n💡 提示: 请重新编译前端项目以使配置更改生效")

if __name__ == "__main__":
    main()
