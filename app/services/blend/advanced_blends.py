"""高级混合模式功能"""
from PIL import Image
import numpy as np
import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.logger import logger


class AdvancedBlends:
    """高级混合模式功能"""
    
    @staticmethod
    def blend_overlay(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        叠加混合模式
        
        Args:
            base_bytes: 基础图层的字节数据
            overlay_bytes: 叠加图层的字节数据
            opacity: 效果强度 (0.0-1.0)
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"叠加混合: opacity={opacity}")
        
        try:
            base = Image.open(io.BytesIO(base_bytes)).convert('RGB')
            overlay = Image.open(io.BytesIO(overlay_bytes)).convert('RGB')
            
            # 调整大小以匹配
            if base.size != overlay.size:
                overlay = overlay.resize(base.size, Image.Resampling.LANCZOS)
            
            # 叠加公式: 
            # if base < 128: result = 2 * base * overlay / 255
            # else: result = 255 - 2 * (255 - base) * (255 - overlay) / 255
            base_array = np.array(base).astype(np.float32)
            overlay_array = np.array(overlay).astype(np.float32)
            
            result_array = np.zeros_like(base_array)
            
            # 暗部使用正片叠底
            dark_mask = base_array < 128
            result_array[dark_mask] = 2 * base_array[dark_mask] * overlay_array[dark_mask] / 255
            
            # 亮部使用滤色
            light_mask = ~dark_mask
            result_array[light_mask] = 255 - 2 * (255 - base_array[light_mask]) * (255 - overlay_array[light_mask]) / 255
            
            result_array = result_array.astype(np.uint8)
            
            # 应用不透明度
            if opacity < 1.0:
                result_array = (base_array * (1 - opacity) + result_array * opacity).astype(np.uint8)
            
            result = Image.fromarray(result_array)
            
            # 保存并返回
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=quality)
            
            logger.info("叠加混合成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"叠加混合失败: {e}")
            raise
    
    @staticmethod
    def blend_color_dodge(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        颜色减淡混合模式
        
        Args:
            base_bytes: 基础图层的字节数据
            overlay_bytes: 叠加图层的字节数据
            opacity: 效果强度 (0.0-1.0)
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"颜色减淡混合: opacity={opacity}")
        
        try:
            base = Image.open(io.BytesIO(base_bytes)).convert('RGB')
            overlay = Image.open(io.BytesIO(overlay_bytes)).convert('RGB')
            
            # 调整大小以匹配
            if base.size != overlay.size:
                overlay = overlay.resize(base.size, Image.Resampling.LANCZOS)
            
            # 颜色减淡公式: result = base / (1 - overlay/255)
            # 如果overlay = 255，结果为255
            base_array = np.array(base).astype(np.float32)
            overlay_array = np.array(overlay).astype(np.float32)
            
            # 避免除零
            denominator = 1 - overlay_array / 255
            denominator[denominator == 0] = 0.001
            
            result_array = base_array / denominator
            result_array = np.clip(result_array, 0, 255).astype(np.uint8)
            
            # 应用不透明度
            if opacity < 1.0:
                result_array = (base_array * (1 - opacity) + result_array * opacity).astype(np.uint8)
            
            result = Image.fromarray(result_array)
            
            # 保存并返回
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=quality)
            
            logger.info("颜色减淡混合成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"颜色减淡混合失败: {e}")
            raise

    @staticmethod
    def blend_color_burn(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        颜色加深混合模式

        Args:
            base_bytes: 基础图层的字节数据
            overlay_bytes: 叠加图层的字节数据
            opacity: 效果强度 (0.0-1.0)
            quality: 输出图像质量 (1-100)

        Returns:
            处理后图片的字节数据
        """
        logger.info(f"颜色加深混合: opacity={opacity}")

        try:
            base = Image.open(io.BytesIO(base_bytes)).convert('RGB')
            overlay = Image.open(io.BytesIO(overlay_bytes)).convert('RGB')

            # 调整大小以匹配
            if base.size != overlay.size:
                overlay = overlay.resize(base.size, Image.Resampling.LANCZOS)

            # 颜色加深公式: result = 1 - (1 - base) / overlay
            # 如果overlay = 0，结果为0
            base_array = np.array(base).astype(np.float32)
            overlay_array = np.array(overlay).astype(np.float32)

            # 避免除零
            overlay_normalized = overlay_array / 255
            overlay_normalized[overlay_normalized == 0] = 0.001

            result_array = 255 * (1 - (1 - base_array/255) / overlay_normalized)
            result_array = np.clip(result_array, 0, 255).astype(np.uint8)

            # 应用不透明度
            if opacity < 1.0:
                result_array = (base_array * (1 - opacity) + result_array * opacity).astype(np.uint8)

            result = Image.fromarray(result_array)

            # 保存并返回
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=quality)

            logger.info("颜色加深混合成功")
            return output.getvalue()

        except Exception as e:
            logger.error(f"颜色加深混合失败: {e}")
            raise
