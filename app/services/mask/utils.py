"""遮罩工具函数"""
from typing import Tuple


class MaskUtils:
    """遮罩工具类"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        将十六进制颜色转换为RGB
        
        Args:
            hex_color: 十六进制颜色字符串 (如 "#FF0000")
            
        Returns:
            RGB元组
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            raise ValueError("无效的十六进制颜色格式")
        
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
