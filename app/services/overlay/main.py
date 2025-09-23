"""图片叠加服务主模块"""
from PIL import Image
from typing import Tuple, Optional
import io
import numpy as np
from ...utils.logger import logger
from .logo_watermark import LogoWatermarkService
from .border import BorderService
from .gradient import GradientEffectService


class OverlayService:
    """图片叠加服务类"""

    @staticmethod
    def add_overlay(
        image_bytes: bytes,
        overlay_type: str,
        opacity: float = 0.8,
        quality: int = 90,
        **kwargs
    ) -> bytes:
        """
        统一的图片叠加方法

        Args:
            image_bytes: 图片字节数据
            overlay_type: 叠加类型 ("gradient", "vignette", "pattern", "border")
            opacity: 透明度
            quality: 输出图像质量 (1-100)
            **kwargs: 其他参数

        Returns:
            处理后图片的字节数据
        """
        logger.info(f"开始图片叠加: type={overlay_type}, opacity={opacity}")

        try:
            # 加载图片
            image = Image.open(io.BytesIO(image_bytes))

            if overlay_type == "gradient":
                # 渐变叠加
                result = OverlayService.add_gradient_overlay(
                    image=image,
                    gradient_type=kwargs.get('gradient_type', 'linear'),
                    gradient_direction=kwargs.get('gradient_direction', 'to_bottom'),
                    start_color=kwargs.get('start_color', '#000000'),
                    end_color=kwargs.get('end_color', '#FFFFFF'),
                    start_opacity=kwargs.get('start_opacity', 0.0),
                    end_opacity=kwargs.get('end_opacity', opacity)
                )
            elif overlay_type == "vignette":
                # 暗角效果
                result = OverlayService.add_vignette_effect(
                    image=image,
                    intensity=opacity,
                    radius=kwargs.get('radius', 1.2)
                )
            elif overlay_type == "border":
                # 边框叠加
                result = OverlayService.add_border(
                    image=image,
                    border_width=kwargs.get('border_width', 10),
                    border_color=kwargs.get('border_color', (0, 0, 0)),
                    border_style=kwargs.get('border_style', 'solid')
                )
            else:
                # 默认使用渐变叠加
                logger.warning(f"未知的叠加类型: {overlay_type}，使用渐变叠加")
                result = OverlayService.add_gradient_overlay(
                    image=image,
                    gradient_type='linear',
                    gradient_direction='to_bottom',
                    start_color='#000000',
                    end_color='#FFFFFF',
                    start_opacity=0.0,
                    end_opacity=opacity
                )

            # 保存结果
            output = io.BytesIO()
            result.save(output, format='JPEG', quality=quality)
            logger.info(f"图片叠加成功")
            return output.getvalue()

        except Exception as e:
            logger.error(f"图片叠加失败: {e}")
            raise

    # 委托给LogoWatermarkService
    add_logo = staticmethod(LogoWatermarkService.add_logo)
    add_image_watermark = staticmethod(LogoWatermarkService.add_image_watermark)

    # 委托给BorderService
    add_border = staticmethod(BorderService.add_border)

    # 委托给GradientEffectService
    add_gradient_overlay = staticmethod(GradientEffectService.add_gradient_overlay)
    add_vignette_effect = staticmethod(GradientEffectService.add_vignette_effect)