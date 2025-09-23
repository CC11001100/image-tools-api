#!/usr/bin/env python3
"""
清理.gitignore文件中的重复规则
保持注释和空行，只去除重复的规则行
"""

import os
import sys
from collections import OrderedDict

def cleanup_gitignore():
    """清理.gitignore文件中的重复规则"""
    
    gitignore_path = '.gitignore'
    
    if not os.path.exists(gitignore_path):
        print("❌ .gitignore文件不存在")
        return False
    
    # 读取原文件
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"🔍 原文件共 {len(lines)} 行")
    
    # 处理行，保持顺序并去重
    seen_rules = set()
    cleaned_lines = []
    removed_count = 0
    
    for line_num, line in enumerate(lines, 1):
        original_line = line
        stripped_line = line.strip()
        
        # 保留空行和注释行
        if not stripped_line or stripped_line.startswith('#'):
            cleaned_lines.append(original_line)
            continue
        
        # 检查规则行是否重复
        if stripped_line in seen_rules:
            print(f"⚠️  删除重复规则 (行 {line_num}): {stripped_line}")
            removed_count += 1
            continue
        
        # 添加到已见规则集合和清理后的行列表
        seen_rules.add(stripped_line)
        cleaned_lines.append(original_line)
    
    print(f"✅ 删除了 {removed_count} 个重复规则")
    print(f"📊 清理后共 {len(cleaned_lines)} 行")
    
    # 备份原文件
    backup_path = f"{gitignore_path}.backup"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"💾 原文件已备份为: {backup_path}")
    
    # 写入清理后的文件
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print(f"🎉 .gitignore文件已清理完成")
    return True

def show_statistics():
    """显示.gitignore文件统计信息"""
    
    gitignore_path = '.gitignore'
    
    if not os.path.exists(gitignore_path):
        print("❌ .gitignore文件不存在")
        return
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
    empty_lines = sum(1 for line in lines if not line.strip())
    rule_lines = total_lines - comment_lines - empty_lines
    
    print("📊 .gitignore文件统计:")
    print(f"  总行数: {total_lines}")
    print(f"  注释行: {comment_lines}")
    print(f"  空行: {empty_lines}")
    print(f"  规则行: {rule_lines}")

def main():
    """主函数"""
    print("🧹 清理.gitignore重复规则")
    print("=" * 50)
    
    # 显示清理前统计
    print("清理前:")
    show_statistics()
    print()
    
    # 执行清理
    if cleanup_gitignore():
        print()
        print("清理后:")
        show_statistics()
        print()
        print("✅ 清理完成！")
        print("💡 建议运行 'git diff .gitignore' 查看更改")
    else:
        print("❌ 清理失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
