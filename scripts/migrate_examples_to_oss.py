#!/usr/bin/env python3
"""
示例图片迁移到OSS脚本
将本地示例图片迁移到阿里云OSS，并更新配置文件
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.services.oss_client import oss_client
from app.services.example_migration_service import migration_service


def main():
    """主函数"""
    print("=" * 60)
    print("示例图片迁移到阿里云OSS")
    print("=" * 60)
    
    # 1. 检查OSS连接
    print("\n1. 检查OSS连接...")
    try:
        buckets = oss_client.list_buckets()
        print(f"✓ OSS连接成功，找到 {len(buckets)} 个存储桶:")
        for bucket in buckets:
            print(f"  - {bucket}")
        
        if oss_client.bucket_name not in buckets:
            print(f"✗ 目标存储桶 '{oss_client.bucket_name}' 不存在")
            return
        else:
            print(f"✓ 目标存储桶 '{oss_client.bucket_name}' 存在")
            
    except Exception as e:
        print(f"✗ OSS连接失败: {str(e)}")
        return
    
    # 2. 扫描本地示例图片
    print("\n2. 扫描本地示例图片...")
    local_files = migration_service.scan_local_examples()
    if not local_files:
        print("✗ 没有找到本地示例图片")
        return
    
    print(f"✓ 找到 {len(local_files)} 个示例图片:")
    for file_info in local_files:
        size_mb = file_info["size"] / (1024 * 1024)
        print(f"  - {file_info['relative_path']} ({size_mb:.2f}MB)")
    
    # 3. 确认迁移
    print(f"\n3. 确认迁移操作...")
    print(f"即将将 {len(local_files)} 个文件上传到OSS存储桶: {oss_client.bucket_name}")
    print(f"存储路径前缀: {oss_client.examples_prefix}")
    
    confirm = input("是否继续? (y/N): ").strip().lower()
    if confirm != 'y':
        print("迁移已取消")
        return
    
    # 4. 执行迁移
    print("\n4. 执行迁移...")
    try:
        report = migration_service.migrate_examples()
        
        if report["success"]:
            print("\n✓ 迁移成功完成!")
            print(f"  - 备份位置: {report['backup_location']}")
            print(f"  - 上传成功: {report['uploaded_files']} 个文件")
            print(f"  - 上传失败: {report['failed_files']} 个文件")
            print(f"  - 更新配置: {report['updated_configs']} 个文件")
            
            if report['failed_uploads']:
                print(f"\n失败的文件:")
                for failed_file in report['failed_uploads']:
                    print(f"  - {failed_file}")
            
            print(f"\n更新的配置文件:")
            for config_file in report['updated_config_files']:
                print(f"  - {config_file}")
            
            # 保存迁移报告
            report_file = project_root / "migration_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n迁移报告已保存到: {report_file}")
            
        else:
            print(f"\n✗ 迁移失败: {report.get('error', '未知错误')}")
            
    except Exception as e:
        print(f"\n✗ 迁移过程中发生异常: {str(e)}")
        return
    
    # 5. 验证迁移结果
    print("\n5. 验证迁移结果...")
    try:
        oss_files = oss_client.list_files()
        print(f"✓ OSS中现有 {len(oss_files)} 个示例文件:")
        for oss_file in oss_files[:10]:  # 只显示前10个
            print(f"  - {oss_file}")
        if len(oss_files) > 10:
            print(f"  ... 还有 {len(oss_files) - 10} 个文件")
            
    except Exception as e:
        print(f"✗ 验证OSS文件失败: {str(e)}")
    
    print("\n" + "=" * 60)
    print("迁移完成!")
    print("请重新编译前端项目以使配置更改生效")
    print("=" * 60)


if __name__ == "__main__":
    main()
