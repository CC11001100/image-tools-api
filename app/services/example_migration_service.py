"""
示例图片迁移服务
将本地示例图片迁移到阿里云OSS
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .oss_client import oss_client
from ..utils.logger import logger


class ExampleMigrationService:
    """示例图片迁移服务"""
    
    def __init__(self):
        self.oss_client = oss_client
        self.local_examples_dir = Path("public/examples")
        self.backup_dir = Path("public/examples_backup")
        
        # 需要更新的配置文件路径
        self.config_files = [
            "frontend/src/config/constants.ts",
            "frontend/src/config/sampleImageUrls.ts",
            "frontend/src/config/examples/stitchShowcaseExamples.ts",
            "frontend/src/config/examples/resizeExamples.ts",
            "frontend/src/config/examples/watermarkExamples.ts",
            "frontend/src/config/examples/enhanceExamples.ts",
            "frontend/src/config/examples/maskExamples.ts",
            "frontend/src/config/examples/overlayExamples.ts",
            "frontend/src/config/examples/noiseExamples.ts",
            "frontend/src/config/examples/annotationExamples.ts",
        ]
    
    def scan_local_examples(self) -> List[Dict[str, str]]:
        """
        扫描本地示例图片
        
        Returns:
            包含文件信息的字典列表
        """
        files = []
        
        if not self.local_examples_dir.exists():
            logger.warning(f"本地示例目录不存在: {self.local_examples_dir}")
            return files
        
        for file_path in self.local_examples_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
                # 计算相对路径
                relative_path = file_path.relative_to(self.local_examples_dir)
                
                files.append({
                    "local_path": str(file_path),
                    "relative_path": str(relative_path),
                    "object_key": str(relative_path).replace("\\", "/"),  # 确保使用正斜杠
                    "size": file_path.stat().st_size,
                    "name": file_path.name
                })
        
        logger.info(f"扫描到 {len(files)} 个示例图片文件")
        return files
    
    def upload_examples_to_oss(self) -> Tuple[List[Dict], List[Dict]]:
        """
        上传示例图片到OSS
        
        Returns:
            (成功列表, 失败列表) 的元组
        """
        files = self.scan_local_examples()
        success_files = []
        failed_files = []
        
        logger.info(f"开始上传 {len(files)} 个示例图片到OSS...")
        
        for file_info in files:
            try:
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
                    logger.info(f"✓ 上传成功: {file_info['relative_path']} -> {url}")
                else:
                    failed_files.append(file_info)
                    logger.error(f"✗ 上传失败: {file_info['relative_path']}")
                    
            except Exception as e:
                file_info["error"] = str(e)
                failed_files.append(file_info)
                logger.error(f"✗ 上传异常: {file_info['relative_path']} - {str(e)}")
        
        logger.info(f"上传完成: 成功 {len(success_files)} 个，失败 {len(failed_files)} 个")
        return success_files, failed_files
    
    def backup_local_examples(self) -> bool:
        """
        备份本地示例图片
        
        Returns:
            备份成功返回True，失败返回False
        """
        try:
            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)
            
            shutil.copytree(self.local_examples_dir, self.backup_dir)
            logger.info(f"本地示例图片已备份到: {self.backup_dir}")
            return True
        except Exception as e:
            logger.error(f"备份本地示例图片失败: {str(e)}")
            return False
    
    def update_config_files(self, url_mapping: Dict[str, str]) -> List[str]:
        """
        更新配置文件中的图片URL
        
        Args:
            url_mapping: 本地路径到OSS URL的映射
            
        Returns:
            更新成功的文件列表
        """
        updated_files = []
        
        for config_file in self.config_files:
            if self._update_single_config_file(config_file, url_mapping):
                updated_files.append(config_file)
        
        return updated_files
    
    def _update_single_config_file(self, file_path: str, url_mapping: Dict[str, str]) -> bool:
        """
        更新单个配置文件
        
        Args:
            file_path: 配置文件路径
            url_mapping: URL映射
            
        Returns:
            更新成功返回True，失败返回False
        """
        try:
            if not os.path.exists(file_path):
                logger.warning(f"配置文件不存在: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 替换所有本地路径为OSS URL
            for local_path, oss_url in url_mapping.items():
                # 处理不同的路径格式
                patterns = [
                    f'"/examples/{local_path}"',
                    f"'/examples/{local_path}'",
                    f'`/examples/{local_path}`',
                    f'"/examples/{local_path.replace("/", "/")}"',
                    f"'/examples/{local_path.replace("/", "/")}'",
                ]
                
                for pattern in patterns:
                    if pattern in content:
                        content = content.replace(pattern, f'"{oss_url}"')
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"✓ 配置文件已更新: {file_path}")
                return True
            else:
                logger.info(f"- 配置文件无需更新: {file_path}")
                return True
                
        except Exception as e:
            logger.error(f"✗ 更新配置文件失败: {file_path} - {str(e)}")
            return False
    
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
            '.mp4': 'video/mp4'
        }
        return content_type_map.get(ext, 'image/jpeg')
    
    def migrate_examples(self) -> Dict[str, any]:
        """
        执行完整的示例图片迁移流程
        
        Returns:
            迁移结果报告
        """
        logger.info("开始示例图片迁移流程...")
        
        # 1. 备份本地文件
        backup_success = self.backup_local_examples()
        if not backup_success:
            return {"success": False, "error": "备份本地文件失败"}
        
        # 2. 上传到OSS
        success_files, failed_files = self.upload_examples_to_oss()
        
        if not success_files:
            return {"success": False, "error": "没有文件上传成功"}
        
        # 3. 生成URL映射
        url_mapping = {}
        for file_info in success_files:
            url_mapping[file_info["object_key"]] = file_info["oss_url"]
        
        # 4. 更新配置文件
        updated_configs = self.update_config_files(url_mapping)
        
        # 5. 生成报告
        report = {
            "success": True,
            "backup_location": str(self.backup_dir),
            "uploaded_files": len(success_files),
            "failed_files": len(failed_files),
            "updated_configs": len(updated_configs),
            "url_mapping": url_mapping,
            "failed_uploads": [f["relative_path"] for f in failed_files],
            "updated_config_files": updated_configs
        }
        
        logger.info("示例图片迁移完成!")
        return report


# 全局实例
migration_service = ExampleMigrationService()
