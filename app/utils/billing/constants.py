"""计费常量和枚举定义"""
from enum import Enum


class BillingType(Enum):
    """计费类型枚举"""
    UPLOAD_ONLY = "upload_only"  # 仅上传文件
    URL_DOWNLOAD = "url_download"  # URL下载 + 上传结果
    DUAL_UPLOAD = "dual_upload"  # 双文件上传
    MIXED_MODE = "mixed_mode"  # 混合模式（URL下载 + 文件上传）


class BillingConstants:
    """计费常量"""
    
    # 费用常量
    BASE_COST = 100  # 基础调用费用 (Token)
    DOWNLOAD_COST_PER_MB = 100  # 下载费用 (Token/MB)
    UPLOAD_COST_PER_MB = 50  # 上传费用 (Token/MB)
    MIN_BILLING_UNIT_KB = 1  # 最小计费单位 (KB)
