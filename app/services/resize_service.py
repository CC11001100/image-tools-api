from PIL import Image
import io
from typing import Optional
from ..utils.logger import logger


class ResizeService:
    """图片尺寸调整服务"""
    
    @staticmethod
    def _calculate_dimensions(
        original_size: tuple,
        target_width: Optional[int],
        target_height: Optional[int],
        maintain_ratio: bool
    ) -> tuple:
        """计算目标尺寸"""
        original_width, original_height = original_size
        
        if target_width is None and target_height is None:
            return original_size
        
        if target_width is None:
            # 只指定高度
            new_height = target_height
            if maintain_ratio:
                new_width = int(original_width * (target_height / original_height))
            else:
                new_width = original_width
        elif target_height is None:
            # 只指定宽度
            new_width = target_width
            if maintain_ratio:
                new_height = int(original_height * (target_width / original_width))
            else:
                new_height = original_height
        else:
            # 都指定了
            if maintain_ratio:
                # 保持比例，取较小的缩放比例
                width_ratio = target_width / original_width
                height_ratio = target_height / original_height
                if width_ratio < height_ratio:
                    new_width = target_width
                    new_height = int(original_height * width_ratio)
                else:
                    new_height = target_height
                    new_width = int(original_width * height_ratio)
            else:
                new_width, new_height = target_width, target_height
        
        return (new_width, new_height)
    
    @staticmethod
    def resize_image(
        image_bytes: bytes,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_ratio: bool = True,
        quality: int = 90
    ) -> bytes:
        """
        调整图片大小
        
        Args:
            image_bytes: 输入图片的字节数据
            width: 目标宽度
            height: 目标高度
            maintain_ratio: 是否保持原始纵横比
            quality: 输出图像质量 (1-100)
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"调整图片大小: {width}x{height}, 保持比例: {maintain_ratio}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            original_size = img.size
            
            # 计算新尺寸
            new_size = ResizeService._calculate_dimensions(
                original_size, width, height, maintain_ratio
            )
            
            logger.info(f"原始尺寸: {original_size}, 目标尺寸: {new_size}")
            
            # 调整大小
            resized_img = img.resize(new_size, Image.LANCZOS)
            
            # 保存并返回
            output = io.BytesIO()
            format = img.format if img.format else "JPEG"
            resized_img.save(output, format=format, quality=quality)
            
            logger.info("图片大小调整成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"调整图片大小失败: {e}")
            raise 