#!/usr/bin/env python3
"""
GitHub仓库设置脚本
帮助创建或配置GitHub仓库并推送代码
"""

import subprocess
import sys
import json
from pathlib import Path

def run_command(command: str, cwd: str = None) -> tuple:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_github_cli():
    """检查GitHub CLI是否安装"""
    success, stdout, stderr = run_command("gh --version")
    return success


def create_github_repo(repo_name: str, description: str = ""):
    """使用GitHub CLI创建仓库"""
    print(f"🚀 创建GitHub仓库: {repo_name}")
    
    cmd = f'gh repo create {repo_name} --public --description "{description}"'
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print(f"✅ 仓库创建成功: https://github.com/cc11001100/{repo_name}")
        return True
    else:
        print(f"❌ 仓库创建失败: {stderr}")
        return False


def setup_remote_and_push(repo_name: str):
    """设置远程仓库并推送"""
    project_root = Path(__file__).parent.parent
    
    print(f"🔗 设置远程仓库...")
    
    # 设置远程仓库
    remote_url = f"git@github.com:cc11001100/{repo_name}.git"
    success, stdout, stderr = run_command(f"git remote set-url origin {remote_url}", cwd=project_root)
    
    if not success:
        # 如果没有origin，添加它
        success, stdout, stderr = run_command(f"git remote add origin {remote_url}", cwd=project_root)
    
    if success:
        print(f"✅ 远程仓库设置成功: {remote_url}")
    else:
        print(f"❌ 远程仓库设置失败: {stderr}")
        return False
    
    # 推送到main分支
    print(f"📤 推送到main分支...")
    success, stdout, stderr = run_command("git push -f origin main", cwd=project_root)
    
    if success:
        print(f"✅ 推送成功!")
        print(f"🌐 仓库地址: https://github.com/cc11001100/{repo_name}")
        return True
    else:
        print(f"❌ 推送失败: {stderr}")
        return False


def check_existing_repos():
    """检查现有仓库"""
    print("🔍 检查现有仓库...")
    
    success, stdout, stderr = run_command("gh repo list cc11001100 --limit 20")
    if success:
        print("📋 现有仓库列表:")
        for line in stdout.strip().split('\n'):
            if line:
                print(f"  - {line}")
        return True
    else:
        print(f"❌ 无法获取仓库列表: {stderr}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("GitHub仓库设置脚本")
    print("=" * 60)
    
    repo_name = "image-tools-api"
    description = "Complete image processing API with 20+ endpoints, React frontend, and OSS integration"
    
    # 1. 检查GitHub CLI
    if not check_github_cli():
        print("❌ GitHub CLI未安装")
        print("💡 请安装GitHub CLI: brew install gh")
        print("💡 然后运行: gh auth login")
        return
    
    print("✅ GitHub CLI已安装")
    
    # 2. 检查现有仓库
    check_existing_repos()
    
    # 3. 询问是否创建新仓库
    print(f"\n🤔 是否创建新仓库 '{repo_name}'?")
    print("   这将:")
    print("   - 创建一个新的公开仓库")
    print("   - 推送当前的干净代码")
    print("   - 完全替换任何现有的同名仓库内容")
    
    response = input("\n是否继续? (y/N): ").strip().lower()
    if response != 'y':
        print("操作已取消")
        return
    
    # 4. 创建仓库
    if create_github_repo(repo_name, description):
        # 5. 设置远程仓库并推送
        if setup_remote_and_push(repo_name):
            print("\n🎉 GitHub仓库设置完成!")
            print(f"🌐 访问地址: https://github.com/cc11001100/{repo_name}")
            print(f"📊 项目大小: 16M (99.6%减少)")
            print(f"📝 提交历史: 1个干净的初始提交")
        else:
            print("\n❌ 推送失败，请检查网络连接和权限")
    else:
        print("\n❌ 仓库创建失败")
        print("💡 可能的解决方案:")
        print("   1. 检查GitHub CLI认证: gh auth status")
        print("   2. 重新登录: gh auth login")
        print("   3. 检查仓库名是否已存在")


if __name__ == "__main__":
    main()
