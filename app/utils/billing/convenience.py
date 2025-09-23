"""便捷计费函数"""
from typing import Dict, Any
from .constants import BillingType
from .calculator import BillingCalculator
from .utils import BillingUtils


def calculate_resize_billing(upload_size_bytes: int = 0, download_size_bytes: int = 0) -> Dict[str, Any]:
    """
    计算resize操作计费的便捷函数（保持向后兼容）

    Args:
        upload_size_bytes: 上传文件大小（字节）
        download_size_bytes: 下载文件大小（字节）

    Returns:
        计费详情
    """
    # 这里需要实现原来的calculate_resize_cost方法
    if upload_size_bytes > 0 and download_size_bytes > 0:
        # 混合模式
        return BillingCalculator.calculate_operation_cost(
            BillingType.MIXED_MODE,
            primary_file_size=upload_size_bytes,
            download_size=download_size_bytes,
            result_size=max(upload_size_bytes, download_size_bytes)
        )
    elif upload_size_bytes > 0:
        # 仅上传
        return BillingCalculator.calculate_operation_cost(
            BillingType.UPLOAD_ONLY,
            primary_file_size=upload_size_bytes,
            result_size=upload_size_bytes
        )
    elif download_size_bytes > 0:
        # 仅下载
        return BillingCalculator.calculate_operation_cost(
            BillingType.URL_DOWNLOAD,
            download_size=download_size_bytes,
            result_size=download_size_bytes
        )
    else:
        # 默认情况
        return BillingCalculator.calculate_operation_cost(BillingType.UPLOAD_ONLY)


def calculate_upload_only_billing(primary_file_size: int, result_size: int = 0) -> Dict[str, Any]:
    """
    计算仅上传文件的计费（类型A）

    Args:
        primary_file_size: 主文件大小（字节）
        result_size: 结果文件大小（字节）

    Returns:
        计费详情
    """
    return BillingCalculator.calculate_operation_cost(
        BillingType.UPLOAD_ONLY,
        primary_file_size=primary_file_size,
        result_size=result_size or primary_file_size
    )


def calculate_url_download_billing(download_size: int, result_size: int = 0) -> Dict[str, Any]:
    """
    计算URL下载的计费（类型B）

    Args:
        download_size: 下载文件大小（字节）
        result_size: 结果文件大小（字节）

    Returns:
        计费详情
    """
    return BillingCalculator.calculate_operation_cost(
        BillingType.URL_DOWNLOAD,
        download_size=download_size,
        result_size=result_size or download_size
    )


def calculate_dual_upload_billing(primary_size: int, secondary_size: int, result_size: int = 0) -> Dict[str, Any]:
    """
    计算双文件上传的计费（类型C）

    Args:
        primary_size: 主文件大小（字节）
        secondary_size: 辅助文件大小（字节）
        result_size: 结果文件大小（字节）

    Returns:
        计费详情
    """
    return BillingCalculator.calculate_operation_cost(
        BillingType.DUAL_UPLOAD,
        primary_file_size=primary_size,
        secondary_file_size=secondary_size,
        result_size=result_size or max(primary_size, secondary_size)
    )


def calculate_mixed_mode_billing(download_size: int, upload_size: int, result_size: int = 0) -> Dict[str, Any]:
    """
    计算混合模式的计费（类型D）

    Args:
        download_size: 下载文件大小（字节）
        upload_size: 上传文件大小（字节）
        result_size: 结果文件大小（字节）

    Returns:
        计费详情
    """
    return BillingCalculator.calculate_operation_cost(
        BillingType.MIXED_MODE,
        primary_file_size=upload_size,
        download_size=download_size,
        result_size=result_size or max(download_size, upload_size)
    )


def estimate_operation_tokens(billing_type: BillingType, **kwargs) -> int:
    """
    估算操作需要的token数量

    Args:
        billing_type: 计费类型
        **kwargs: 文件大小参数

    Returns:
        预估token数量
    """
    billing_info = BillingCalculator.calculate_operation_cost(billing_type, **kwargs)
    return billing_info["total_cost"]


def generate_operation_remark(api_path: str, operation: str, billing_info: Dict[str, Any], **kwargs) -> str:
    """
    生成操作的详细备注

    Args:
        api_path: API路径
        operation: 操作类型
        billing_info: 计费信息
        **kwargs: 额外信息

    Returns:
        详细备注
    """
    return BillingUtils.generate_billing_remark(api_path, operation, billing_info, kwargs)
