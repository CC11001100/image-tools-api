"""
计费工具函数 - 模块化版本
用于计算各种图像处理操作的Token费用
支持多种接口类型和详细的费用备注生成
"""

from typing import Dict, Any
from .billing import (
    BillingType,
    BillingConstants,
    BillingCalculator,
    BillingUtils,
    calculate_resize_billing,
    calculate_upload_only_billing,
    calculate_url_download_billing,
    calculate_dual_upload_billing,
    calculate_mixed_mode_billing,
    estimate_operation_tokens,
    generate_operation_remark
)

# 保持向后兼容的类和函数导出
class BillingCalculator(BillingCalculator):
    """计费计算器 - 向后兼容"""
    pass

# 便捷函数导出（保持向后兼容）
__all__ = [
    'BillingType',
    'BillingCalculator',
    'calculate_resize_billing',
    'calculate_upload_only_billing',
    'calculate_url_download_billing',
    'calculate_dual_upload_billing',
    'calculate_mixed_mode_billing',
    'estimate_operation_tokens',
    'generate_operation_remark'
]
