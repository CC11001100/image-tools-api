"""计费工具函数"""
from typing import Dict, Any, Optional


class BillingUtils:
    """计费工具类"""
    
    @classmethod
    def _generate_breakdown(
        cls,
        base_cost: int,
        download_cost: int,
        primary_cost: int,
        secondary_cost: int,
        result_cost: int,
        download_size: int,
        primary_size: int,
        secondary_size: int,
        result_size: int
    ) -> Dict[str, Optional[str]]:
        """
        生成费用明细
        
        Args:
            base_cost: 基础费用
            download_cost: 下载费用
            primary_cost: 主文件费用
            secondary_cost: 辅助文件费用
            result_cost: 结果文件费用
            download_size: 下载文件大小
            primary_size: 主文件大小
            secondary_size: 辅助文件大小
            result_size: 结果文件大小
            
        Returns:
            费用明细字典
        """
        breakdown = {
            "base": f"{base_cost} Token (基础调用费用)"
        }

        if download_cost > 0:
            breakdown["download"] = f"{download_cost} Token (下载 {cls.format_size(download_size)})"

        if primary_cost > 0:
            breakdown["primary"] = f"{primary_cost} Token (主文件 {cls.format_size(primary_size)})"

        if secondary_cost > 0:
            breakdown["secondary"] = f"{secondary_cost} Token (辅助文件 {cls.format_size(secondary_size)})"

        if result_cost > 0:
            breakdown["result"] = f"{result_cost} Token (结果文件 {cls.format_size(result_size)})"

        return breakdown

    @classmethod
    def generate_billing_remark(
        cls,
        api_path: str,
        operation: str,
        billing_info: Dict[str, Any],
        additional_info: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成详细的计费备注

        Args:
            api_path: API路径
            operation: 操作类型（如"图片缩放"、"水印添加"等）
            billing_info: 计费信息字典
            additional_info: 额外信息

        Returns:
            详细的计费备注字符串
        """
        parts = [f"{operation}处理"]

        # 添加各项费用说明
        breakdown = billing_info.get("breakdown", {})
        cost_parts = []

        if "download" in breakdown and breakdown["download"]:
            cost_parts.append(breakdown["download"])

        if "primary" in breakdown and breakdown["primary"]:
            cost_parts.append(breakdown["primary"])

        if "secondary" in breakdown and breakdown["secondary"]:
            cost_parts.append(breakdown["secondary"])

        if "result" in breakdown and breakdown["result"]:
            cost_parts.append(breakdown["result"])

        # 添加基础费用
        if "base" in breakdown:
            cost_parts.append(breakdown["base"])

        # 添加额外信息
        if additional_info:
            for key, value in additional_info.items():
                if value:
                    parts.append(f"{key}: {value}")

        # 组合最终备注
        cost_summary = " + ".join(cost_parts)
        total_cost = billing_info.get("total_cost", 0)

        remark = f"{api_path} - {operation} - {cost_summary} = 总计{total_cost}Token"

        return remark

    @classmethod
    def format_size(cls, size_bytes: int) -> str:
        """
        格式化文件大小显示
        
        Args:
            size_bytes: 文件大小（字节）
            
        Returns:
            格式化的大小字符串
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
