from PIL import Image, ImageFilter
import io
import numpy as np
import cv2
from typing import Optional
from ...utils.logger import logger


class ArtisticEffects:
    """艺术效果"""
    
    @staticmethod
    def apply_glow_enhance(image_bytes: bytes, radius: int = 20, intensity: float = 1.0) -> bytes:
        """
        发光增强效果
        
        Args:
            image_bytes: 输入图片字节数据
            radius: 发光半径
            intensity: 发光强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"发光增强: radius={radius}, intensity={intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 创建发光效果
            blurred = cv2.GaussianBlur(img_array, (radius * 2 + 1, radius * 2 + 1), radius / 3)
            
            # 混合原图和模糊图
            glow_effect = img_array + intensity * blurred
            
            # 限制像素值范围
            glow_effect = np.clip(glow_effect, 0, 255)
            
            result_img = Image.fromarray(glow_effect.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"发光增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_dreamy_enhance(image_bytes: bytes, softness: float = 0.5, brightness: float = 0.2) -> bytes:
        """
        梦幻增强效果
        
        Args:
            image_bytes: 输入图片字节数据
            softness: 柔化程度
            brightness: 亮度增加
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"梦幻增强: softness={softness}, brightness={brightness}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 应用柔化效果
            blur_radius = int(softness * 10) + 1
            soft_img = cv2.GaussianBlur(img_array, (blur_radius, blur_radius), blur_radius / 3)
            
            # 混合原图和柔化图
            dreamy = img_array * (1 - softness) + soft_img * softness
            
            # 增加亮度
            dreamy += brightness * 255
            
            # 轻微的对比度降低
            dreamy = (dreamy - 128) * 0.8 + 128
            
            # 限制像素值范围
            dreamy = np.clip(dreamy, 0, 255)
            
            result_img = Image.fromarray(dreamy.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"梦幻增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_portrait_enhance(image_bytes: bytes, skin_smooth: float = 0.3, 
                              eye_enhance: float = 0.5, teeth_whiten: float = 0.3) -> bytes:
        """
        人像增强
        
        Args:
            image_bytes: 输入图片字节数据
            skin_smooth: 皮肤平滑程度
            eye_enhance: 眼部增强强度
            teeth_whiten: 牙齿美白强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"人像增强: skin_smooth={skin_smooth}, eye_enhance={eye_enhance}, teeth_whiten={teeth_whiten}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 皮肤平滑（双边滤波）
            if skin_smooth > 0:
                smooth_kernel = int(skin_smooth * 20) + 5
                smoothed = cv2.bilateralFilter(img_array.astype('uint8'), smooth_kernel, 
                                             skin_smooth * 100, skin_smooth * 100).astype(np.float32)
                img_array = img_array * (1 - skin_smooth) + smoothed * skin_smooth
            
            # 眼部增强（增加对比度和锐化）
            if eye_enhance > 0:
                # 简单的全局增强，实际应用中需要人脸检测
                enhanced = (img_array - 128) * (1 + eye_enhance * 0.3) + 128
                img_array = img_array * (1 - eye_enhance * 0.5) + enhanced * (eye_enhance * 0.5)
            
            # 牙齿美白（增加亮度，减少黄色）
            if teeth_whiten > 0:
                # 简单的全局处理，实际应用中需要牙齿检测
                if len(img_array.shape) == 3:
                    # 减少黄色调
                    img_array[:, :, 0] *= (1 + teeth_whiten * 0.1)  # 增加红色
                    img_array[:, :, 1] *= (1 - teeth_whiten * 0.1)  # 减少绿色
                    img_array[:, :, 2] *= (1 + teeth_whiten * 0.2)  # 增加蓝色
            
            # 限制像素值范围
            img_array = np.clip(img_array, 0, 255)
            
            result_img = Image.fromarray(img_array.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"人像增强失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_landscape_enhance(image_bytes: bytes, clarity: float = 0.8, 
                               vibrance: float = 0.6, sky_enhance: float = 0.4) -> bytes:
        """
        风景增强
        
        Args:
            image_bytes: 输入图片字节数据
            clarity: 清晰度增强
            vibrance: 自然饱和度
            sky_enhance: 天空增强
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"风景增强: clarity={clarity}, vibrance={vibrance}, sky_enhance={sky_enhance}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            
            # 清晰度增强（USM锐化）
            if clarity > 0:
                blurred = cv2.GaussianBlur(img_array, (0, 0), 1.0)
                high_freq = img_array - blurred
                img_array += clarity * high_freq
            
            # 自然饱和度增强
            if vibrance > 0 and len(img_array.shape) == 3:
                # 转换到HSV
                hsv = cv2.cvtColor(img_array.astype('uint8'), cv2.COLOR_RGB2HSV).astype(np.float32)
                
                # 计算当前饱和度
                current_sat = hsv[:, :, 1] / 255.0
                
                # 对低饱和度区域应用更强的增强
                vibrance_factor = 1 + vibrance * (1 - current_sat)
                hsv[:, :, 1] *= vibrance_factor
                hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
                
                img_array = cv2.cvtColor(hsv.astype('uint8'), cv2.COLOR_HSV2RGB).astype(np.float32)
            
            # 天空增强（增强蓝色通道）
            if sky_enhance > 0 and len(img_array.shape) == 3:
                # 检测蓝色区域（简单方法）
                blue_mask = (img_array[:, :, 2] > img_array[:, :, 0]) & (img_array[:, :, 2] > img_array[:, :, 1])
                img_array[:, :, 2] = np.where(blue_mask, 
                                            img_array[:, :, 2] * (1 + sky_enhance), 
                                            img_array[:, :, 2])
            
            # 限制像素值范围
            img_array = np.clip(img_array, 0, 255)
            
            result_img = Image.fromarray(img_array.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"风景增强失败: {str(e)}")
            raise
