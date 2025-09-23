"""变换相关枚举"""
from enum import Enum


class CropType(str, Enum):
    """裁剪类型枚举"""
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"
    POLYGON = "polygon"
    SMART_CENTER = "smart_center"
    SMART_FACE = "smart_face"
    SMART_OBJECT = "smart_object"


class TransformType(str, Enum):
    """变换类型枚举"""
    ROTATE = "rotate"
    FLIP_HORIZONTAL = "flip_horizontal"
    FLIP_VERTICAL = "flip_vertical"
    SCALE = "scale"
    TRANSLATE = "translate"
    SKEW = "skew"
    PERSPECTIVE = "perspective"
    AFFINE = "affine"
