from PIL import Image
import io
import numpy as np
import cv2
from typing import Optional
from ...utils.logger import logger


class AdvancedBlur:
    """高级模糊效果"""
    
    @staticmethod
    def apply_lens_blur(image_bytes: bytes, radius: float = 5.0, sides: int = 6) -> bytes:
        """
        镜头模糊（散景效果）
        
        Args:
            image_bytes: 输入图片字节数据
            radius: 模糊半径
            sides: 光圈叶片数（影响散景形状）
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"镜头模糊: radius={radius}, sides={sides}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            
            # 创建多边形核（模拟光圈形状）
            kernel_size = int(radius * 2) + 1
            kernel = np.zeros((kernel_size, kernel_size))
            
            center = kernel_size // 2
            
            # 生成正多边形顶点
            angles = np.linspace(0, 2 * np.pi, sides, endpoint=False)
            vertices = []
            for angle in angles:
                x = center + radius * np.cos(angle)
                y = center + radius * np.sin(angle)
                vertices.append([int(x), int(y)])
            
            # 填充多边形
            vertices = np.array(vertices, dtype=np.int32)
            cv2.fillPoly(kernel, [vertices], 1)
            
            # 归一化核
            kernel = kernel / np.sum(kernel)
            
            # 应用卷积
            if len(img_array.shape) == 3:
                result = np.zeros_like(img_array)
                for c in range(3):
                    result[:, :, c] = cv2.filter2D(img_array[:, :, c], -1, kernel)
            else:
                result = cv2.filter2D(img_array, -1, kernel)
            
            result_img = Image.fromarray(result.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"镜头模糊失败: {str(e)}")
            raise
    
    @staticmethod
    def apply_zoom_blur(image_bytes: bytes, center_x: Optional[int] = None, 
                       center_y: Optional[int] = None, strength: float = 5.0) -> bytes:
        """
        缩放模糊（放射状模糊）
        
        Args:
            image_bytes: 输入图片字节数据
            center_x: 模糊中心X坐标
            center_y: 模糊中心Y坐标
            strength: 模糊强度
            
        Returns:
            处理后的图片字节数据
        """
        logger.info(f"缩放模糊: center=({center_x}, {center_y}), strength={strength}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img, dtype=np.float32)
            height, width = img_array.shape[:2]
            
            # 设置默认中心点
            if center_x is None:
                center_x = width // 2
            if center_y is None:
                center_y = height // 2
            
            # 创建结果数组
            result = np.zeros_like(img_array)
            
            # 计算每个像素的缩放模糊
            y_coords, x_coords = np.ogrid[:height, :width]
            
            # 计算到中心的距离
            dx = x_coords - center_x
            dy = y_coords - center_y
            distance = np.sqrt(dx**2 + dy**2)
            
            # 归一化距离
            max_distance = np.sqrt(width**2 + height**2) / 2
            normalized_distance = distance / max_distance
            
            # 计算模糊步数
            blur_steps = int(strength)
            
            for step in range(blur_steps):
                # 计算缩放因子
                scale = 1.0 - (step / blur_steps) * normalized_distance * 0.1
                
                # 创建变换矩阵
                M = cv2.getRotationMatrix2D((center_x, center_y), 0, scale)
                
                # 应用变换
                if len(img_array.shape) == 3:
                    transformed = cv2.warpAffine(img_array, M, (width, height))
                else:
                    transformed = cv2.warpAffine(img_array, M, (width, height))
                
                result += transformed
            
            # 平均化结果
            result = result / blur_steps
            
            # 限制像素值范围
            result = np.clip(result, 0, 255)
            
            result_img = Image.fromarray(result.astype('uint8'))
            
            output = io.BytesIO()
            result_img.save(output, format='JPEG', quality=90)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"缩放模糊失败: {str(e)}")
            raise
