from PIL import Image
import io
from ..utils.logger import logger

# 导入所有滤镜模块
from .filters.basic_filters import BasicFilters
from .filters.color_filters import ColorFilters
from .filters.artistic_filters import ArtisticFilters
from .filters.blackwhite_filters import BlackwhiteFilters
from .filters.vintage_filters import VintageFilters
from .filters.special_filters import SpecialFilters
from .filters.edge_filters import EdgeFilters
from .filters.creative_filters import CreativeFilters


class FilterService:
    """基础滤镜服务 - 重构后的主入口"""

    @staticmethod
    def apply_filter(
        image_bytes: bytes,
        filter_type: str,
        intensity: float = 1.0
    ) -> bytes:
        """
        应用基础滤镜
        
        Args:
            image_bytes: 输入图片的字节数据
            filter_type: 滤镜类型
            intensity: 效果强度
            
        Returns:
            处理后图片的字节数据
        """
        logger.info(f"应用滤镜: {filter_type}, 强度: {intensity}")
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # 滤镜处理函数映射
            filter_map = {
            "grayscale": BasicFilters._apply_grayscale,
            "sepia": BasicFilters._apply_sepia,
            "blur": BasicFilters._apply_blur,
            "sharpen": BasicFilters._apply_sharpen,
            "brightness": BasicFilters._apply_brightness,
            "contrast": BasicFilters._apply_contrast,
            "saturate": ColorFilters._apply_saturate,
            "desaturate": ColorFilters._apply_desaturate,
            "warm": ColorFilters._apply_warm,
            "cool": ColorFilters._apply_cool,
            "vintage": ColorFilters._apply_vintage,
            "hueshift": ColorFilters._apply_hueshift,
            "gamma": ColorFilters._apply_gamma,
            "levels": ColorFilters._apply_levels,
            "emboss": ArtisticFilters._apply_emboss,
            "posterize": ArtisticFilters._apply_posterize,
            "solarize": ArtisticFilters._apply_solarize,
            "invert": ArtisticFilters._apply_invert,
            "edge_enhance": ArtisticFilters._apply_edge_enhance,
            "smooth": ArtisticFilters._apply_smooth,
            "detail": ArtisticFilters._apply_detail,
            "monochrome": BlackwhiteFilters._apply_monochrome,
            "dramatic_bw": BlackwhiteFilters._apply_dramatic_bw,
            "infrared": BlackwhiteFilters._apply_infrared,
            "high_contrast_bw": BlackwhiteFilters._apply_high_contrast_bw,
            "film_grain": VintageFilters._apply_film_grain,
            "retro": VintageFilters._apply_retro,
            "polaroid": VintageFilters._apply_polaroid,
            "lomo": VintageFilters._apply_lomo,
            "analog": VintageFilters._apply_analog,
            "crossprocess": VintageFilters._apply_crossprocess,
            "dream": SpecialFilters._apply_dream,
            "glow": SpecialFilters._apply_glow,
            "soft_focus": SpecialFilters._apply_soft_focus,
            "noise": SpecialFilters._apply_noise,
            "vignette": SpecialFilters._apply_vignette,
            "mosaic": SpecialFilters._apply_mosaic,
            "find_edges": EdgeFilters._apply_find_edges,
            "contour": EdgeFilters._apply_contour,
            "edge_enhance_more": EdgeFilters._apply_edge_enhance_more,
            "smooth_more": EdgeFilters._apply_smooth_more,
            "unsharp_mask": EdgeFilters._apply_unsharp_mask,
            "pencil": CreativeFilters._apply_pencil,
            "sketch": CreativeFilters._apply_sketch,
            "cartoon": CreativeFilters._apply_cartoon,
            "hdr": CreativeFilters._apply_hdr,
            "cyberpunk": CreativeFilters._apply_cyberpunk,
            "noir": CreativeFilters._apply_noir,
            "faded": CreativeFilters._apply_faded,
            "pastel": CreativeFilters._apply_pastel,
            }
            
            if filter_type not in filter_map:
                logger.warning(f"未知的滤镜类型: {filter_type}")
                filtered_img = img
            else:
                filtered_img = filter_map[filter_type](img, intensity)
            
            # 保存并返回
            output = io.BytesIO()
            save_format = img.format if img.format else "JPEG"
            filtered_img.save(output, format=save_format)
            
            logger.info("滤镜应用成功")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"应用滤镜失败: {e}")
            raise