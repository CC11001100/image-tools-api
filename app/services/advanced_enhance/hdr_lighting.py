from PIL import Image
import io
import numpy as np
import cv2
from typing import Optional
from ...utils.logger import logger


class HDRLighting:
    """HDR和光影处理"""
    
    @staticmethod
    def apply_hdr_enhance(image_bytes: bytes, gamma: float = 2.2, exposure: float = 1.0) -> bytes:
        """
        HDR增强
        
        Args:
            image_bytes: 输入图片字节数据
            gamma: 伽马值
            exposure: 曝光补偿
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"HDR增强: gamma={gamma}, exposure={exposure}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32) / 255.0
            
            # 应用曝光补偿
            img_array = img_array * exposure
            
            # 色调映射（Reinhard算子）
            luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2] if len(img_array.shape) == 3 else img_array
            
            # 计算平均亮度
            avg_luminance = np.mean(luminance)
            
            # 应用Reinhard色调映射
            mapped_luminance = luminance / (1 + luminance / avg_luminance)
            
            # 重新分配到RGB通道
            if len(img_array.shape) == 3:
                scale_factor = mapped_luminance / (luminance + 1e-6)
                for c in range(3):
                    img_array[:, :, c] *= scale_factor
            else:
                img_array = mapped_luminance
            
            # 伽马校正
            img_array = np.power(img_array, 1.0 / gamma)
            
            # 转换回0-255范围
            img_array = np.clip(img_array * 255, 0, 255)
            
            result_img = Image.fromarray(img_array.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"HDR增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_shadow_highlight(image_bytes: bytes, shadow_amount: float = 0.5, 
                              highlight_amount: float = 0.5, color_correction: float = 0.2) -> bytes:
        """
        阴影高光调整
        
        Args:
            image_bytes: 输入图片字节数据
            shadow_amount: 阴影调整量
            highlight_amount: 高光调整量
            color_correction: 颜色校正强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"阴影高光调整: shadow={shadow_amount}, highlight={highlight_amount}, color={color_correction}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 计算亮度
            if len(img_array.shape) == 3:
                luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
            else:
                luminance = img_array.copy()
            
            # 归一化亮度
            normalized_lum = luminance / 255.0
            
            # 创建阴影和高光掩模
            shadow_mask = 1.0 - normalized_lum
            highlight_mask = normalized_lum
            
            # 应用S曲线调整
            shadow_adjustment = shadow_amount * shadow_mask
            highlight_adjustment = -highlight_amount * highlight_mask
            
            # 计算总调整
            total_adjustment = shadow_adjustment + highlight_adjustment
            
            # 应用调整
            if len(img_array.shape) == 3:
                for c in range(3):
                    img_array[:, :, c] += total_adjustment * 255
                    
                # 颜色校正
                if color_correction > 0:
                    # 增强饱和度
                    hsv = cv2.cvtColor(img_array.astype('uint8'), cv2.COLOR_RGB2HSV).astype(np.float32)
                    hsv[:, :, 1] *= (1 + color_correction)
                    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
                    img_array = cv2.cvtColor(hsv.astype('uint8'), cv2.COLOR_HSV2RGB).astype(np.float32)
            else:
                img_array += total_adjustment * 255
            
            # 限制像素值范围
            img_array = np.clip(img_array, 0, 255)
            
            result_img = Image.fromarray(img_array.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"阴影高光调整失败: {str(e)}")
            raise
