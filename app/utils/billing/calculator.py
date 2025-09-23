"""核心计费计算器"""
import math
from typing import Dict, Any
from .constants import BillingType, BillingConstants


class BillingCalculator:
    """计费计算器"""
    
    @classmethod
    def calculate_file_size_tokens(cls, size_bytes: int, token_per_mb: int) -> int:
        """
        计算文件大小对应的token费用
        
        Args:
            size_bytes: 文件大小（字节）
            token_per_mb: 每MB的token费用
            
        Returns:
            计算出的token费用
        """
        if size_bytes <= 0:
            return 0
            
        # 最小计费单位1KB，不足1KB按1KB计算
        size_kb = max(BillingConstants.MIN_BILLING_UNIT_KB, math.ceil(size_bytes / 1024))
        
        # 转换为MB（保留小数精度）
        size_mb = size_kb / 1024.0
        
        # 计算token费用（向上取整）
        tokens = math.ceil(token_per_mb * size_mb)
        
        return tokens
    
    @classmethod
    def calculate_download_cost(cls, download_size_bytes: int) -> int:
        """
        计算下载费用
        
        Args:
            download_size_bytes: 下载文件大小（字节）
            
        Returns:
            下载费用（Token）
        """
        return cls.calculate_file_size_tokens(download_size_bytes, BillingConstants.DOWNLOAD_COST_PER_MB)
    
    @classmethod
    def calculate_upload_cost(cls, upload_size_bytes: int) -> int:
        """
        计算上传费用
        
        Args:
            upload_size_bytes: 上传文件大小（字节）
            
        Returns:
            上传费用（Token）
        """
        return cls.calculate_file_size_tokens(upload_size_bytes, BillingConstants.UPLOAD_COST_PER_MB)
    
    @classmethod
    def calculate_operation_cost(
        cls,
        billing_type: BillingType,
        primary_file_size: int = 0,
        secondary_file_size: int = 0,
        download_size: int = 0,
        result_size: int = 0
    ) -> Dict[str, Any]:
        """
        计算各种操作的总费用（通用方法）

        Args:
            billing_type: 计费类型
            primary_file_size: 主文件大小（字节）
            secondary_file_size: 辅助文件大小（字节）
            download_size: 下载文件大小（字节）
            result_size: 结果文件大小（字节）

        Returns:
            费用详情字典
        """
        from .utils import BillingUtils  # 避免循环导入
        
        base_cost = BillingConstants.BASE_COST
        download_cost = 0
        primary_cost = 0
        secondary_cost = 0
        result_cost = 0

        # 根据计费类型计算各项费用
        if billing_type == BillingType.UPLOAD_ONLY:
            # 类型A: 仅文件上传
            primary_cost = cls.calculate_upload_cost(primary_file_size) if primary_file_size > 0 else 0
            result_cost = cls.calculate_upload_cost(result_size) if result_size > 0 else 0

        elif billing_type == BillingType.URL_DOWNLOAD:
            # 类型B: URL下载 + 结果上传
            download_cost = cls.calculate_download_cost(download_size) if download_size > 0 else 0
            result_cost = cls.calculate_upload_cost(result_size) if result_size > 0 else 0

        elif billing_type == BillingType.DUAL_UPLOAD:
            # 类型C: 双文件上传 + 结果上传
            primary_cost = cls.calculate_upload_cost(primary_file_size) if primary_file_size > 0 else 0
            secondary_cost = cls.calculate_upload_cost(secondary_file_size) if secondary_file_size > 0 else 0
            result_cost = cls.calculate_upload_cost(result_size) if result_size > 0 else 0

        elif billing_type == BillingType.MIXED_MODE:
            # 类型D: URL下载 + 文件上传 + 结果上传
            download_cost = cls.calculate_download_cost(download_size) if download_size > 0 else 0
            primary_cost = cls.calculate_upload_cost(primary_file_size) if primary_file_size > 0 else 0
            result_cost = cls.calculate_upload_cost(result_size) if result_size > 0 else 0

        total_cost = base_cost + download_cost + primary_cost + secondary_cost + result_cost

        return {
            "base_cost": base_cost,
            "download_cost": download_cost,
            "primary_cost": primary_cost,
            "secondary_cost": secondary_cost,
            "result_cost": result_cost,
            "total_cost": total_cost,
            "billing_type": billing_type.value,
            "breakdown": BillingUtils._generate_breakdown(
                base_cost, download_cost, primary_cost, secondary_cost, result_cost,
                download_size, primary_file_size, secondary_file_size, result_size
            )
        }

    @classmethod
    def calculate_resize_cost(cls, upload_size_bytes: int = 0, download_size_bytes: int = 0) -> Dict[str, Any]:
        """
        计算resize操作的总费用（保持向后兼容）

        Args:
            upload_size_bytes: 上传文件大小（字节）
            download_size_bytes: 下载文件大小（字节，仅resize-by-url需要）

        Returns:
            费用详情字典
        """
        if download_size_bytes > 0:
            # URL下载模式
            return cls.calculate_operation_cost(
                BillingType.URL_DOWNLOAD,
                download_size=download_size_bytes,
                result_size=upload_size_bytes
            )
        else:
            # 仅上传模式
            return cls.calculate_operation_cost(
                BillingType.UPLOAD_ONLY,
                primary_file_size=upload_size_bytes,
                result_size=upload_size_bytes
            )
