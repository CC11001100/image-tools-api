"""叠加服务基础工具类"""
from PIL import Image
from typing import Tuple


class OverlayBase:
    """叠加服务基础工具类"""
    
    @staticmethod
    def calculate_position(
        base_size: Tuple[int, int],
        overlay_size: Tuple[int, int],
        position: str,
        padding: int
    ) -> Tuple[int, int]:
        """计算叠加位置"""
        base_width, base_height = base_size
        overlay_width, overlay_height = overlay_size
        
        positions = {
            "top-left": (padding, padding),
            "top-right": (base_width - overlay_width - padding, padding),
            "bottom-left": (padding, base_height - overlay_height - padding),
            "bottom-right": (
                base_width - overlay_width - padding,
                base_height - overlay_height - padding
            ),
            "center": (
                (base_width - overlay_width) // 2,
                (base_height - overlay_height) // 2
            )
        }
        
        return positions.get(position, positions["bottom-right"])
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def interpolate_color(
        color1: Tuple[int, int, int], 
        color2: Tuple[int, int, int], 
        ratio: float
    ) -> Tuple[int, int, int]:
        """在两个颜色之间插值"""
        return tuple(
            int(color1[i] + (color2[i] - color1[i]) * ratio)
            for i in range(3)
        ) 