#!/usr/bin/env python3
"""
迁移所有静态文件到OSS
包括前端public目录下的所有图片文件
"""

import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Tuple

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import oss_client


class AllStaticFilesMigration:
    """全量静态文件迁移服务"""
    
    def __init__(self):
        self.oss_client = oss_client
        self.frontend_public_dir = Path("frontend/public")
        self.public_dir = Path("public")
        
        # 支持的图片格式
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico'}
        
        # 排除的目录
        self.exclude_dirs = {'node_modules', '__pycache__', '.git', 'build'}
        
    def scan_all_static_files(self) -> List[Dict[str, str]]:
        """
        扫描所有静态文件
        
        Returns:
            包含文件信息的字典列表
        """
        files = []
        
        # 扫描 frontend/public 目录
        if self.frontend_public_dir.exists():
            files.extend(self._scan_directory(self.frontend_public_dir, "frontend/public"))
        
        # 扫描 public 目录（排除已备份的）
        if self.public_dir.exists():
            for item in self.public_dir.iterdir():
                if item.name != "examples_backup":
                    if item.is_file() and item.suffix.lower() in self.image_extensions:
                        files.append(self._create_file_info(item, "public"))
                    elif item.is_dir():
                        files.extend(self._scan_directory(item, "public"))
        
        print(f"扫描到 {len(files)} 个静态文件")
        return files
    
    def _scan_directory(self, directory: Path, base_prefix: str) -> List[Dict[str, str]]:
        """
        递归扫描目录
        
        Args:
            directory: 要扫描的目录
            base_prefix: 基础前缀
            
        Returns:
            文件信息列表
        """
        files = []
        
        for item in directory.rglob("*"):
            # 跳过排除的目录
            if any(exclude_dir in item.parts for exclude_dir in self.exclude_dirs):
                continue
                
            if item.is_file() and item.suffix.lower() in self.image_extensions:
                files.append(self._create_file_info(item, base_prefix))
        
        return files
    
    def _create_file_info(self, file_path: Path, base_prefix: str) -> Dict[str, str]:
        """
        创建文件信息字典

        Args:
            file_path: 文件路径
            base_prefix: 基础前缀

        Returns:
            文件信息字典
        """
        # 确保文件路径是绝对路径
        if not file_path.is_absolute():
            file_path = project_root / file_path

        # 计算相对于项目根目录的路径
        relative_to_project = file_path.relative_to(project_root)
        
        # 计算OSS对象键（移除base_prefix）
        if base_prefix == "frontend/public":
            # frontend/public/examples/xxx -> examples/xxx
            relative_parts = relative_to_project.parts[2:]  # 移除 'frontend', 'public'
        elif base_prefix == "public":
            # public/examples/xxx -> examples/xxx  
            relative_parts = relative_to_project.parts[1:]  # 移除 'public'
        else:
            relative_parts = relative_to_project.parts
        
        object_key = "/".join(relative_parts)
        
        return {
            "local_path": str(file_path),
            "relative_path": str(relative_to_project),
            "object_key": object_key,
            "size": file_path.stat().st_size,
            "name": file_path.name,
            "base_prefix": base_prefix
        }
    
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
        
        print(f"\n上传完成: 成功 {len(success_files)} 个，失败 {len(failed_files)} 个")
        return success_files, failed_files
    
    def _get_content_type(self, filename: str) -> str:
        """
        根据文件名获取MIME类型
        
        Args:
            filename: 文件名
            
        Returns:
            MIME类型
        """
        ext = Path(filename).suffix.lower()
        content_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.bmp': 'image/bmp',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon'
        }
        return content_type_map.get(ext, 'image/jpeg')
    
    def generate_url_mapping(self, success_files: List[Dict]) -> Dict[str, str]:
        """
        生成URL映射
        
        Args:
            success_files: 成功上传的文件列表
            
        Returns:
            本地路径到OSS URL的映射
        """
        url_mapping = {}
        
        for file_info in success_files:
            # 生成多种可能的本地路径格式
            object_key = file_info["object_key"]
            oss_url = file_info["oss_url"]
            
            # 添加不同的路径格式到映射
            url_mapping[object_key] = oss_url
            url_mapping[f"/{object_key}"] = oss_url
            url_mapping[f"/examples/{object_key}"] = oss_url if not object_key.startswith("examples/") else oss_url
            
            # 如果是examples目录下的文件，添加简化路径
            if object_key.startswith("examples/"):
                simple_path = object_key[9:]  # 移除 "examples/" 前缀
                url_mapping[simple_path] = oss_url
        
        return url_mapping


def main():
    """主函数"""
    print("=" * 60)
    print("全量静态文件迁移到阿里云OSS")
    print("=" * 60)
    
    migration = AllStaticFilesMigration()
    
    # 1. 扫描所有静态文件
    print("\n1. 扫描所有静态文件...")
    files = migration.scan_all_static_files()
    
    if not files:
        print("没有找到静态文件")
        return
    
    # 显示文件统计
    total_size = sum(f["size"] for f in files)
    print(f"找到 {len(files)} 个静态文件，总大小: {total_size / (1024*1024):.2f}MB")
    
    # 按目录分组显示
    by_dir = {}
    for f in files:
        base = f["base_prefix"]
        if base not in by_dir:
            by_dir[base] = []
        by_dir[base].append(f)
    
    for base, file_list in by_dir.items():
        size = sum(f["size"] for f in file_list)
        print(f"  {base}: {len(file_list)} 个文件 ({size / (1024*1024):.2f}MB)")
    
    # 2. 确认上传
    print(f"\n2. 确认上传...")
    confirm = input("是否继续上传所有静态文件到OSS? (y/N): ").strip().lower()
    if confirm != 'y':
        print("上传已取消")
        return
    
    # 3. 执行上传
    print(f"\n3. 执行上传...")
    success_files, failed_files = migration.upload_files_to_oss(files)
    
    # 4. 生成报告
    print(f"\n4. 生成报告...")
    url_mapping = migration.generate_url_mapping(success_files)
    
    report = {
        "success": len(failed_files) == 0,
        "total_files": len(files),
        "uploaded_files": len(success_files),
        "failed_files": len(failed_files),
        "total_size_mb": total_size / (1024*1024),
        "url_mapping": url_mapping,
        "failed_uploads": [f["relative_path"] for f in failed_files],
        "success_uploads": [f["relative_path"] for f in success_files]
    }
    
    # 保存报告
    report_file = project_root / "all_static_migration_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"迁移报告已保存到: {report_file}")
    
    if failed_files:
        print(f"\n失败的文件:")
        for failed_file in failed_files:
            print(f"  - {failed_file['relative_path']}")
    
    print("\n" + "=" * 60)
    print("全量静态文件迁移完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
