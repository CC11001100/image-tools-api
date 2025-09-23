#!/usr/bin/env python3
"""
项目清理脚本
安全删除不必要的文件和目录以减少项目大小
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def run_command(command: str) -> tuple:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, cwd=project_root, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_size(path: Path) -> str:
    """获取路径大小"""
    if not path.exists():
        return "0B"
    
    success, stdout, stderr = run_command(f"du -sh '{path}'")
    if success:
        return stdout.strip().split()[0]
    return "未知"


def safe_remove(path: Path, description: str) -> bool:
    """安全删除文件或目录"""
    if not path.exists():
        print(f"  ⚠️  {description}: 不存在")
        return False
    
    size = get_size(path)
    try:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        print(f"  ✅ {description}: 已删除 ({size})")
        return True
    except Exception as e:
        print(f"  ❌ {description}: 删除失败 - {e}")
        return False


def cleanup_node_modules():
    """清理node_modules"""
    print("📦 清理Node.js依赖...")
    
    frontend_nm = project_root / "frontend" / "node_modules"
    if safe_remove(frontend_nm, "frontend/node_modules"):
        print("  💡 提示: 运行 'cd frontend && npm install' 重新安装依赖")


def cleanup_python_venvs():
    """清理Python虚拟环境"""
    print("\n🐍 清理Python虚拟环境...")
    
    venvs = ['venv', 'venv_playwright']
    for venv_name in venvs:
        venv_path = project_root / venv_name
        if safe_remove(venv_path, venv_name):
            if venv_name == 'venv':
                print("  💡 提示: 运行 'python -m venv venv && source venv/bin/activate && pip install -r requirements.txt' 重新创建")
            else:
                print("  💡 提示: 运行 'python -m venv venv_playwright && source venv_playwright/bin/activate && pip install playwright' 重新创建")


def cleanup_cache_files():
    """清理缓存文件"""
    print("\n🗑️  清理缓存文件...")
    
    cache_items = [
        (".pytest_cache", "pytest缓存"),
        ("__pycache__", "Python缓存"),
        ("*.pyc", "Python字节码文件"),
        (".DS_Store", "macOS系统文件")
    ]
    
    for pattern, description in cache_items:
        if '*' in pattern:
            success, stdout, stderr = run_command(f"find . -name '{pattern}' -delete")
            if success:
                print(f"  ✅ {description}: 已清理")
        else:
            path = project_root / pattern
            safe_remove(path, description)


def cleanup_backup_files():
    """清理备份文件"""
    print("\n📄 清理备份文件...")
    
    backup_files = [
        "frontend-new.tar",
        ".gitignore.backup",
        "*.backup",
        "*_backup.*"
    ]
    
    for pattern in backup_files:
        if '*' in pattern:
            success, stdout, stderr = run_command(f"find . -name '{pattern}' -type f")
            if success and stdout.strip():
                files = stdout.strip().split('\n')
                for file_path in files:
                    if file_path:
                        path = Path(file_path)
                        safe_remove(path, f"备份文件: {path.name}")
        else:
            path = project_root / pattern
            safe_remove(path, f"备份文件: {pattern}")


def cleanup_report_files():
    """清理报告文件"""
    print("\n📊 清理报告文件...")
    
    report_patterns = [
        "*_report.json",
        "*_results.json",
        "test_*.py",  # 根目录下的测试脚本
        "*.md"  # 一些临时markdown文件
    ]
    
    for pattern in report_patterns:
        success, stdout, stderr = run_command(f"find . -maxdepth 1 -name '{pattern}' -type f")
        if success and stdout.strip():
            files = stdout.strip().split('\n')
            for file_path in files:
                if file_path and not file_path.endswith('README.md'):  # 保留README
                    path = Path(file_path)
                    if path.name not in ['requirements.txt']:  # 保留重要文件
                        safe_remove(path, f"报告文件: {path.name}")


def cleanup_logs():
    """清理日志文件"""
    print("\n📝 清理日志文件...")
    
    logs_dir = project_root / "logs"
    if logs_dir.exists():
        # 只清理旧日志，保留目录结构
        success, stdout, stderr = run_command(f"find {logs_dir} -name '*.log' -mtime +7 -delete")
        if success:
            print("  ✅ 旧日志文件: 已清理")


def optimize_git_repository():
    """优化Git仓库"""
    print("\n🔧 优化Git仓库...")
    
    print("  🔍 当前Git仓库大小:", get_size(project_root / ".git"))
    
    # Git垃圾回收
    success, stdout, stderr = run_command("git gc --aggressive --prune=now")
    if success:
        print("  ✅ Git垃圾回收: 完成")
    else:
        print(f"  ❌ Git垃圾回收: 失败 - {stderr}")
    
    # 清理reflog
    success, stdout, stderr = run_command("git reflog expire --expire=now --all")
    if success:
        print("  ✅ 清理reflog: 完成")
    
    print("  📏 优化后Git仓库大小:", get_size(project_root / ".git"))


def show_cleanup_summary():
    """显示清理总结"""
    print("\n" + "=" * 60)
    print("🧹 清理完成总结")
    print("=" * 60)
    
    # 重新计算项目大小
    success, stdout, stderr = run_command("du -sh . --exclude=node_modules --exclude=venv*")
    if success:
        new_size = stdout.strip().split()[0]
        print(f"📊 清理后项目大小: {new_size}")
    
    print("\n💡 后续步骤:")
    print("1. 重新安装前端依赖: cd frontend && npm install")
    print("2. 重新创建Python环境: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt")
    print("3. 如需Playwright: python -m venv venv_playwright && source venv_playwright/bin/activate && pip install playwright")
    print("4. 运行测试确保功能正常")


def main():
    """主函数"""
    print("=" * 60)
    print("🧹 项目清理脚本")
    print("=" * 60)
    
    # 显示当前大小
    success, stdout, stderr = run_command("du -sh .")
    if success:
        current_size = stdout.strip().split()[0]
        print(f"📊 当前项目大小: {current_size}")
    
    print("\n⚠️  警告: 此操作将删除以下内容:")
    print("  • node_modules (可重新安装)")
    print("  • Python虚拟环境 (可重新创建)")
    print("  • 缓存文件")
    print("  • 备份文件")
    print("  • 报告文件")
    print("  • 旧日志文件")
    
    # 确认操作
    response = input("\n是否继续? (y/N): ").strip().lower()
    if response != 'y':
        print("操作已取消")
        return
    
    # 执行清理
    cleanup_node_modules()
    cleanup_python_venvs()
    cleanup_cache_files()
    cleanup_backup_files()
    cleanup_report_files()
    cleanup_logs()
    optimize_git_repository()
    
    # 显示总结
    show_cleanup_summary()


if __name__ == "__main__":
    main()
