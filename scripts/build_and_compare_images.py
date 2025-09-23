#!/usr/bin/env python3
"""
构建Docker镜像并比较大小
检查静态资源迁移后的镜像大小变化
"""

import sys
import os
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def run_command(command: str, cwd: str = None) -> tuple:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd or project_root,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "命令超时"
    except Exception as e:
        return False, "", str(e)


def get_docker_image_size(image_name: str) -> str:
    """获取Docker镜像大小"""
    success, stdout, stderr = run_command(f"docker images {image_name} --format 'table {{{{.Size}}}}'")
    if success and stdout:
        lines = stdout.strip().split('\n')
        if len(lines) > 1:
            return lines[1].strip()
    return "未知"


def get_current_image_sizes() -> Dict[str, str]:
    """获取当前镜像大小"""
    images = {
        'frontend': 'image-tools-api-frontend:latest',
        'backend': 'image-tools-api-backend:latest'
    }
    
    sizes = {}
    for name, image in images.items():
        sizes[name] = get_docker_image_size(image)
    
    return sizes


def build_frontend_image() -> bool:
    """构建前端镜像"""
    print("🏗️  构建前端镜像...")
    
    # 确保前端已构建
    print("  📦 构建前端代码...")
    success, stdout, stderr = run_command("npm run build", cwd=str(project_root / "frontend"))
    if not success:
        print(f"  ❌ 前端构建失败: {stderr}")
        return False
    
    # 构建Docker镜像
    print("  🐳 构建Docker镜像...")
    success, stdout, stderr = run_command("docker build -t image-tools-api-frontend:latest -f frontend/Dockerfile .")
    if not success:
        print(f"  ❌ 前端镜像构建失败: {stderr}")
        return False
    
    print("  ✅ 前端镜像构建成功")
    return True


def build_backend_image() -> bool:
    """构建后端镜像"""
    print("🏗️  构建后端镜像...")
    
    success, stdout, stderr = run_command("docker build -t image-tools-api-backend:latest -f backend.Dockerfile .")
    if not success:
        print(f"  ❌ 后端镜像构建失败: {stderr}")
        return False
    
    print("  ✅ 后端镜像构建成功")
    return True


def analyze_frontend_build() -> Dict:
    """分析前端构建结果"""
    build_dir = project_root / "frontend" / "build"
    
    if not build_dir.exists():
        return {"error": "构建目录不存在"}
    
    # 计算总大小
    total_size = 0
    file_count = 0
    
    for file_path in build_dir.rglob("*"):
        if file_path.is_file():
            total_size += file_path.stat().st_size
            file_count += 1
    
    # 分析静态资源
    static_dir = build_dir / "static"
    static_size = 0
    static_files = 0
    
    if static_dir.exists():
        for file_path in static_dir.rglob("*"):
            if file_path.is_file():
                static_size += file_path.stat().st_size
                static_files += 1
    
    return {
        "total_size": total_size,
        "total_size_mb": total_size / (1024 * 1024),
        "file_count": file_count,
        "static_size": static_size,
        "static_size_mb": static_size / (1024 * 1024),
        "static_files": static_files
    }


def check_build_contents() -> Dict:
    """检查构建内容"""
    build_dir = project_root / "frontend" / "build"
    
    # 检查是否有图片文件
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico']:
        image_files.extend(list(build_dir.rglob(f"*{ext}")))
    
    # 检查examples目录
    examples_dir = build_dir / "examples"
    examples_files = []
    if examples_dir.exists():
        examples_files = list(examples_dir.rglob("*"))
    
    return {
        "image_files": [str(f.relative_to(build_dir)) for f in image_files],
        "examples_files": [str(f.relative_to(build_dir)) for f in examples_files if f.is_file()],
        "has_examples_dir": examples_dir.exists()
    }


def main():
    """主函数"""
    print("=" * 60)
    print("Docker镜像构建和大小比较")
    print("=" * 60)
    
    # 1. 获取当前镜像大小
    print("1. 获取当前镜像大小...")
    current_sizes = get_current_image_sizes()
    print(f"  前端镜像: {current_sizes.get('frontend', '未找到')}")
    print(f"  后端镜像: {current_sizes.get('backend', '未找到')}")
    
    # 2. 分析前端构建
    print("\n2. 分析前端构建...")
    build_analysis = analyze_frontend_build()
    if "error" in build_analysis:
        print(f"  ❌ {build_analysis['error']}")
    else:
        print(f"  📦 构建大小: {build_analysis['total_size_mb']:.2f}MB")
        print(f"  📄 文件数量: {build_analysis['file_count']}")
        print(f"  🎨 静态资源: {build_analysis['static_size_mb']:.2f}MB ({build_analysis['static_files']} 文件)")
    
    # 3. 检查构建内容
    print("\n3. 检查构建内容...")
    build_contents = check_build_contents()
    print(f"  🖼️  图片文件: {len(build_contents['image_files'])} 个")
    if build_contents['image_files']:
        for img in build_contents['image_files'][:5]:
            print(f"    - {img}")
        if len(build_contents['image_files']) > 5:
            print(f"    ... 还有 {len(build_contents['image_files']) - 5} 个")
    
    print(f"  📁 examples目录: {'存在' if build_contents['has_examples_dir'] else '不存在'}")
    if build_contents['examples_files']:
        print(f"    包含 {len(build_contents['examples_files'])} 个文件")
    
    # 4. 重新构建镜像
    print("\n4. 重新构建镜像...")
    
    # 构建前端镜像
    frontend_success = build_frontend_image()
    
    # 构建后端镜像
    backend_success = build_backend_image()
    
    # 5. 获取新的镜像大小
    if frontend_success or backend_success:
        print("\n5. 获取新的镜像大小...")
        new_sizes = get_current_image_sizes()
        
        print(f"\n📊 镜像大小对比:")
        print(f"  前端镜像:")
        print(f"    之前: {current_sizes.get('frontend', '未知')}")
        print(f"    现在: {new_sizes.get('frontend', '未知')}")
        
        print(f"  后端镜像:")
        print(f"    之前: {current_sizes.get('backend', '未知')}")
        print(f"    现在: {new_sizes.get('backend', '未知')}")
    
    # 6. 生成报告
    report = {
        "timestamp": time.time(),
        "current_sizes": current_sizes,
        "build_analysis": build_analysis,
        "build_contents": build_contents,
        "build_success": {
            "frontend": frontend_success,
            "backend": backend_success
        }
    }
    
    if frontend_success or backend_success:
        report["new_sizes"] = get_current_image_sizes()
    
    # 保存报告
    report_file = project_root / "docker_build_comparison_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 详细报告已保存: {report_file}")
    
    print("\n" + "=" * 60)
    if frontend_success and backend_success:
        print("🎉 所有镜像构建成功!")
    elif frontend_success or backend_success:
        print("⚠️  部分镜像构建成功")
    else:
        print("❌ 镜像构建失败")
    print("=" * 60)


if __name__ == "__main__":
    main()
