#!/usr/bin/env python3
"""
配置文件更新器模块
负责更新前端配置文件，将本地路径替换为OSS URL
"""

import re
from pathlib import Path
from typing import Dict


class ConfigUpdater:
    """配置文件更新器类"""
    
    def __init__(self, project_root: Path):
        """
        初始化配置文件更新器
        
        Args:
            project_root: 项目根目录路径
        """
        self.project_root = project_root
    
    def update_config_files(self, oss_urls: Dict[str, str], config_files: list) -> int:
        """
        更新前端配置文件，将本地路径替换为OSS URL
        
        Args:
            oss_urls: OSS URL映射字典
            config_files: 需要更新的配置文件列表
            
        Returns:
            更新的文件数量
        """
        print("\n" + "=" * 60)
        print("更新前端配置文件")
        print("=" * 60)
        
        updated_count = 0

        for config_file in config_files:
            file_path = self.project_root / config_file
            if not file_path.exists():
                print(f"⚠️ 配置文件不存在: {config_file}")
                continue

            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # 替换本地路径为OSS URL
                for object_key, oss_url in oss_urls.items():
                    # 构建本地路径模式
                    local_path = f"/examples/{object_key}"

                    # 替换所有引号包围的本地路径
                    patterns = [
                        rf'"/examples/{re.escape(object_key)}"',
                        rf"'/examples/{re.escape(object_key)}'",
                        rf'`/examples/{re.escape(object_key)}`',
                    ]

                    for pattern in patterns:
                        quote_char = pattern[0]
                        replacement = f'{quote_char}{oss_url}{quote_char}'
                        content = re.sub(pattern, replacement, content)

                # 如果内容有变化，写回文件
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ 已更新: {config_file}")
                    updated_count += 1
                else:
                    print(f"➖ 无需更新: {config_file}")

            except Exception as e:
                print(f"✗ 更新配置文件失败 {config_file}: {e}")

        print(f"\n✓ 总共更新了 {updated_count} 个配置文件")
        return updated_count
