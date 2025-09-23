#!/usr/bin/env python3
"""
迁移剩余的静态文件到OSS
包括screenshots、public/generated、测试文件等
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import oss_client


class RemainingStaticFilesMigration:
    """剩余静态文件迁移服务"""
    
    def __init__(self):
        self.oss_client = oss_client
        
        # 支持的图片格式
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico'}
        
        # 需要处理的文件和目录
        self.target_files = [
            "public/test_image.jpg",
            "watermark_test_output.jpg",
        ]
        
        self.target_directories = [
            "public/generated",
            "screenshots",
        ]
        
        # 排除的目录和文件
        self.exclude_patterns = {
            'backup',
            'node_modules', 
            '__pycache__', 
            '.git',
            'build',
            'venv',
            'test-results',  # Playwright测试结果
            'debug-api-docs.png'  # 调试文件
        }
        
    def scan_remaining_static_files(self) -> List[Dict[str, str]]:
        """
        扫描剩余的静态文件
        
        Returns:
            包含文件信息的字典列表
        """
        files = []
        
        # 扫描指定的单个文件
        for file_path in self.target_files:
            full_path = project_root / file_path
            if full_path.exists() and full_path.is_file():
                files.append(self._create_file_info(full_path))
        
        # 扫描指定的目录
        for dir_path in self.target_directories:
            full_dir = project_root / dir_path
            if full_dir.exists() and full_dir.is_dir():
                files.extend(self._scan_directory(full_dir))
        
        print(f"扫描到 {len(files)} 个剩余静态文件")
        return files
    
    def _scan_directory(self, directory: Path) -> List[Dict[str, str]]:
        """
        递归扫描目录
        
        Args:
            directory: 要扫描的目录
            
        Returns:
            文件信息列表
        """
        files = []
        
        for item in directory.rglob("*"):
            # 跳过排除的目录和文件
            if any(exclude in item.parts for exclude in self.exclude_patterns):
                continue
                
            if item.is_file() and item.suffix.lower() in self.image_extensions:
                files.append(self._create_file_info(item))
        
        return files
    
    def _create_file_info(self, file_path: Path) -> Dict[str, str]:
        """
        创建文件信息字典
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        # 计算相对于项目根目录的路径
        relative_to_project = file_path.relative_to(project_root)
        
        # 构建OSS对象键
        # 对于不同类型的文件使用不同的前缀
        if "screenshots" in str(file_path):
            object_key = f"screenshots/{file_path.name}"
        elif "generated" in str(file_path):
            object_key = f"generated/{file_path.name}"
        elif "test" in file_path.name.lower():
            object_key = f"test/{file_path.name}"
        else:
            object_key = f"misc/{file_path.name}"
        
        return {
            "local_path": str(file_path),
            "relative_path": str(relative_to_project),
            "object_key": object_key,
            "size": file_path.stat().st_size,
            "name": file_path.name,
            "category": self._get_file_category(file_path)
        }
    
    def _get_file_category(self, file_path: Path) -> str:
        """获取文件分类"""
        if "screenshots" in str(file_path):
            return "screenshots"
        elif "generated" in str(file_path):
            return "generated"
        elif "test" in file_path.name.lower():
            return "test"
        else:
            return "misc"
    
    def upload_files_to_oss(self, files: List[Dict[str, str]]) -> Tuple[List[Dict], List[Dict]]:
        """
        上传文件到OSS
        
        Args:
            files: 文件信息列表
            
        Returns:
            (成功列表, 失败列表) 的元组
        """
        success_files = []
        failed_files = []
        
        print(f"开始上传 {len(files)} 个静态文件到OSS...")
        
        for i, file_info in enumerate(files, 1):
            try:
                print(f"[{i}/{len(files)}] 上传: {file_info['relative_path']}")
                
                # 确定MIME类型
                content_type = self._get_content_type(file_info["name"])
                
                # 上传到OSS
                url = self.oss_client.upload_file(
                    file_path=file_info["local_path"],
                    object_key=file_info["object_key"],
                    content_type=content_type
                )
                
                if url:
                    file_info["oss_url"] = url
                    success_files.append(file_info)
                    print(f"  ✓ 成功: {url}")
                else:
                    failed_files.append(file_info)
                    print(f"  ✗ 失败")
                    
            except Exception as e:
                file_info["error"] = str(e)
                failed_files.append(file_info)
                print(f"  ✗ 异常: {str(e)}")
        
        return success_files, failed_files
    
    def _get_content_type(self, filename: str) -> str:
        """根据文件扩展名确定MIME类型"""
        ext = Path(filename).suffix.lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.bmp': 'image/bmp',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon'
        }
        return content_types.get(ext, 'image/jpeg')
    
    def update_references(self, success_files: List[Dict]) -> List[str]:
        """
        更新代码中的文件引用
        
        Args:
            success_files: 成功上传的文件列表
            
        Returns:
            更新的文件列表
        """
        updated_files = []
        
        # 创建本地路径到OSS URL的映射
        path_mapping = {}
        for file_info in success_files:
            local_path = file_info["relative_path"]
            oss_url = file_info["oss_url"]
            path_mapping[local_path] = oss_url
            
            # 也添加绝对路径映射
            if local_path.startswith("public/"):
                web_path = "/" + local_path[7:]  # 移除 "public/" 前缀
                path_mapping[web_path] = oss_url
        
        # 查找需要更新的文件
        search_patterns = [
            "frontend/src/**/*.ts",
            "frontend/src/**/*.tsx", 
            "frontend/src/**/*.js",
            "frontend/src/**/*.jsx",
            "*.md",
            "*.py",
            "*.html"
        ]
        
        files_to_check = []
        for pattern in search_patterns:
            files_to_check.extend(project_root.glob(pattern))
        
        # 更新文件引用
        for file_path in files_to_check:
            if self._update_file_references(file_path, path_mapping):
                updated_files.append(str(file_path.relative_to(project_root)))
        
        return updated_files
    
    def _update_file_references(self, file_path: Path, path_mapping: Dict[str, str]) -> bool:
        """
        更新单个文件中的引用
        
        Args:
            file_path: 文件路径
            path_mapping: 路径映射字典
            
        Returns:
            是否有更新
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 替换所有映射的路径
            for local_path, oss_url in path_mapping.items():
                # 处理不同的引用格式
                patterns = [
                    rf'["\']({re.escape(local_path)})["\']',
                    rf'["\']\./{re.escape(local_path)}["\']',
                    rf'["\']\.\./{re.escape(local_path)}["\']',
                ]
                
                for pattern in patterns:
                    content = re.sub(pattern, f'"{oss_url}"', content)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 已更新引用: {file_path.relative_to(project_root)}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ 更新引用失败: {file_path} - {str(e)}")
            return False
    
    def cleanup_local_files(self, success_files: List[Dict], backup: bool = True) -> bool:
        """
        清理本地文件
        
        Args:
            success_files: 成功上传的文件列表
            backup: 是否备份到backup目录
            
        Returns:
            是否成功
        """
        if backup:
            backup_dir = project_root / "backup" / "remaining-static-files"
            backup_dir.mkdir(parents=True, exist_ok=True)
        
        for file_info in success_files:
            try:
                local_path = Path(file_info["local_path"])
                
                if backup:
                    # 备份文件
                    backup_file = backup_dir / file_info["name"]
                    backup_file.write_bytes(local_path.read_bytes())
                    print(f"📦 已备份: {backup_file}")
                
                # 删除原文件
                local_path.unlink()
                print(f"🗑️  已删除: {local_path}")
                
            except Exception as e:
                print(f"❌ 清理文件失败: {file_info['local_path']} - {str(e)}")
                return False
        
        return True
    
    def generate_report(self, success_files: List[Dict], failed_files: List[Dict], 
                       updated_files: List[str]) -> Dict:
        """生成迁移报告"""
        return {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "total_files": len(success_files) + len(failed_files),
            "success_count": len(success_files),
            "failed_count": len(failed_files),
            "updated_references": len(updated_files),
            "success_files": success_files,
            "failed_files": failed_files,
            "updated_files": updated_files,
            "total_size": sum(f["size"] for f in success_files)
        }


def main():
    """主函数"""
    print("=" * 60)
    print("剩余静态文件迁移到阿里云OSS")
    print("=" * 60)
    
    migration = RemainingStaticFilesMigration()
    
    # 1. 扫描剩余静态文件
    print("\n1. 扫描剩余静态文件...")
    files = migration.scan_remaining_static_files()
    
    if not files:
        print("没有找到需要迁移的静态文件")
        return
    
    # 显示文件统计
    total_size = sum(f["size"] for f in files)
    print(f"找到 {len(files)} 个静态文件，总大小: {total_size / (1024*1024):.2f}MB")
    
    # 按分类显示
    by_category = {}
    for f in files:
        category = f["category"]
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(f)
    
    for category, file_list in by_category.items():
        size = sum(f["size"] for f in file_list)
        print(f"  {category}: {len(file_list)} 个文件 ({size / (1024*1024):.2f}MB)")
    
    # 2. 上传到OSS
    print("\n2. 上传文件到OSS...")
    success_files, failed_files = migration.upload_files_to_oss(files)
    
    print(f"\n上传结果:")
    print(f"  成功: {len(success_files)} 个文件")
    print(f"  失败: {len(failed_files)} 个文件")
    
    if failed_files:
        print("\n失败的文件:")
        for f in failed_files:
            print(f"  - {f['relative_path']}: {f.get('error', '未知错误')}")
    
    # 3. 更新引用
    print("\n3. 更新代码中的文件引用...")
    updated_files = migration.update_references(success_files)
    print(f"更新了 {len(updated_files)} 个文件中的引用")
    
    # 4. 生成报告
    report = migration.generate_report(success_files, failed_files, updated_files)
    
    # 保存报告
    report_file = project_root / "remaining_static_migration_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 迁移报告已保存: {report_file}")
    
    # 5. 询问是否清理本地文件
    if success_files:
        print(f"\n是否清理本地文件? (y/N): ", end="")
        response = input().strip().lower()
        if response == 'y':
            print("\n5. 清理本地文件...")
            if migration.cleanup_local_files(success_files, backup=True):
                print("✅ 本地文件清理完成")
            else:
                print("❌ 本地文件清理失败")
    
    print("\n" + "=" * 60)
    print("剩余静态文件迁移完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
