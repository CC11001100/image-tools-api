"""混合控制器 - 统一混合接口"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.logger import logger
from .basic_blends import BasicBlends
from .advanced_blends import AdvancedBlends


class BlendController:
    """混合控制器"""
    
    @staticmethod
    def blend_images(
        base_image_bytes: bytes,
        blend_image_bytes: bytes,
        blend_mode: str = "normal",
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        统一的图片混合方法
        
        Args:
            base_image_bytes: 基础图片的字节数据
            blend_image_bytes: 混合图片的字节数据
            blend_mode: 混合模式
            opacity: 不透明度 (0.0-1.0)
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"开始图片混合: mode={blend_mode}, opacity={opacity}")
        
        try:
            if blend_mode == "normal":
                return BasicBlends.blend_normal(base_image_bytes, blend_image_bytes, opacity, (0, 0), quality)
            elif blend_mode == "multiply":
                return BasicBlends.blend_multiply(base_image_bytes, blend_image_bytes, opacity, quality)
            elif blend_mode == "screen":
                return BasicBlends.blend_screen(base_image_bytes, blend_image_bytes, opacity, quality)
            elif blend_mode == "overlay":
                return AdvancedBlends.blend_overlay(base_image_bytes, blend_image_bytes, opacity, quality)
            elif blend_mode == "color-dodge":
                return AdvancedBlends.blend_color_dodge(base_image_bytes, blend_image_bytes, opacity, quality)
            elif blend_mode == "color-burn":
                return AdvancedBlends.blend_color_burn(base_image_bytes, blend_image_bytes, opacity, quality)
            else:
                # 默认使用正常混合
                logger.warning(f"未知的混合模式: {blend_mode}，使用正常混合")
                return BasicBlends.blend_normal(base_image_bytes, blend_image_bytes, opacity, (0, 0), quality)
                
        except Exception as e:
            logger.error(f"图片混合失败: {e}")
            raise
