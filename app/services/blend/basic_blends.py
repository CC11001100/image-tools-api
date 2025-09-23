"""基础混合模式功能"""
from PIL import Image
import numpy as np
import io
from typing import Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.logger import logger


class BasicBlends:
    """基础混合模式功能"""
    
    @staticmethod
    def blend_normal(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        position: Tuple[int, int] = (0, 0),
        quality: int = 90
    ) -> bytes:
        """
        正常混合模式
        
        Args:
            base_bytes: 基础图层的字节数据
            overlay_bytes: 叠加图层的字节数据
            opacity: 不透明度 (0.0-1.0)
            position: 叠加位置 (x, y)
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"正常混合: opacity={opacity}, position={position}")
        
        try:
            base = Image.open(io.BytesIO(base_bytes)).convert('RGBA')
            overlay = Image.open(io.BytesIO(overlay_bytes)).convert('RGBA')
            
            # 调整透明度
            if opacity < 1.0:
                overlay_array = np.array(overlay)
                overlay_array[:, :, 3] = (overlay_array[:, :, 3] * opacity).astype(np.uint8)
                overlay = Image.fromarray(overlay_array)
            
            # 创建结果图像
            result = base.copy()
            result.paste(overlay, position, overlay)
            
            # 保存并返回
            output = io.BytesIO()
            result.save(output, format="PNG", quality=quality)
            
            logger.info("正常混合成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"正常混合失败: {e}")
            raise
    
    @staticmethod
    def blend_multiply(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        正片叠底混合模式
        
        Args:
            base_bytes: 基础图层的字节数据
            overlay_bytes: 叠加图层的字节数据
            opacity: 效果强度 (0.0-1.0)
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"正片叠底混合: opacity={opacity}")
        
        try:
            base = Image.open(io.BytesIO(base_bytes)).convert('RGB')
            overlay = Image.open(io.BytesIO(overlay_bytes)).convert('RGB')
            
            # 调整大小以匹配
            if base.size != overlay.size:
                overlay = overlay.resize(base.size, Image.Resampling.LANCZOS)
            
            # 正片叠底公式: result = base * overlay / 255
            base_array = np.array(base).astype(np.float32)
            overlay_array = np.array(overlay).astype(np.float32)
            
            result_array = (base_array * overlay_array / 255).astype(np.uint8)
            
            # 应用不透明度
            if opacity < 1.0:
                result_array = (base_array * (1 - opacity) + result_array * opacity).astype(np.uint8)
            
            result = Image.fromarray(result_array)
            
            # 保存并返回
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=quality)
            
            logger.info("正片叠底混合成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"正片叠底混合失败: {e}")
            raise

    @staticmethod
    def blend_screen(
        base_bytes: bytes,
        overlay_bytes: bytes,
        opacity: float = 1.0,
        quality: int = 90
    ) -> bytes:
        """
        滤色混合模式

        Args:
            base_bytes: 基础图层的字节数据
            overlay_bytes: 叠加图层的字节数据
            opacity: 效果强度 (0.0-1.0)
            quality: 输出图像质量 (1-100)

        Returns:
            处理后图片的字节数据
        """
        logger.info(f"滤色混合: opacity={opacity}")

        try:
            base = Image.open(io.BytesIO(base_bytes)).convert('RGB')
            overlay = Image.open(io.BytesIO(overlay_bytes)).convert('RGB')

            # 调整大小以匹配
            if base.size != overlay.size:
                overlay = overlay.resize(base.size, Image.Resampling.LANCZOS)

            # 滤色公式: result = 255 - ((255 - base) * (255 - overlay) / 255)
            base_array = np.array(base).astype(np.float32)
            overlay_array = np.array(overlay).astype(np.float32)

            result_array = 255 - ((255 - base_array) * (255 - overlay_array) / 255)
            result_array = result_array.astype(np.uint8)

            # 应用不透明度
            if opacity < 1.0:
                result_array = (base_array * (1 - opacity) + result_array * opacity).astype(np.uint8)

            result = Image.fromarray(result_array)

            # 保存并返回
            output = io.BytesIO()
            result.save(output, format="JPEG", quality=quality)

            logger.info("滤色混合成功")
            return output.getvalue()

        except Exception as e:
            logger.error(f"滤色混合失败: {e}")
            raise
