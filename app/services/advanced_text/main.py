"""高级文字服务主模块"""
from PIL import Image
from typing import Tuple, Optional
from ...utils.logger import logger
from .basic_text import BasicTextService
from .gradient_text import GradientTextService
from .special_effects import SpecialEffectsTextService
from .base import AdvancedTextBase


class AdvancedTextService:
    """高级文字服务类"""
    
    # 委托给BasicTextService
    add_advanced_text = staticmethod(BasicTextService.add_advanced_text)
    
    # 委托给GradientTextService
    add_gradient_text = staticmethod(GradientTextService.add_gradient_text)
    
    # 委托给SpecialEffectsTextService
    add_curved_text = staticmethod(SpecialEffectsTextService.add_curved_text)
    add_3d_text = staticmethod(SpecialEffectsTextService.add_3d_text)
    
    # 从基础类导出工具方法（保持向后兼容）
    _hex_to_rgb = staticmethod(AdvancedTextBase.hex_to_rgb) 