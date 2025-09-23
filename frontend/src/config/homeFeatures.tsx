import React from 'react';
import {
  TextFields as WatermarkIcon,
  ZoomIn as ResizeIcon,
  FilterVintage as FilterIcon,
  Palette as ArtFilterIcon,
  CropFree as CropIcon,
  RotateRight as RotateIcon,
  CameraAlt as PerspectiveIcon,
  AspectRatio as CanvasIcon,
  ColorLens as ColorIcon,
  AutoFixHigh as EnhanceIcon,
  Grain as NoiseIcon,
  GridOn as PixelateIcon,
  Layers as BlendIcon,
  ViewModule as StitchIcon,
  Transform as FormatIcon,
  AddPhotoAlternate as OverlayIcon,
  BlurOn as MaskIcon,
  Gif as GifIcon,
  TextFormat as AdvancedTextIcon,
  Create as AnnotationIcon,
} from '@mui/icons-material';

export interface Feature {
  title: string;
  description: string;
  link: string;
  icon: React.ReactElement;
  color: string;
}

export interface FeatureGroup {
  title: string;
  features: Feature[];
}

export const featureGroups: FeatureGroup[] = [
  {
    title: '基础编辑',
    features: [
      {
        title: '调整尺寸',
        description: '调整图片尺寸，支持按比例缩放或固定尺寸',
        link: '/resize',
        icon: <ResizeIcon sx={{ fontSize: 40 }} />,
        color: '#4caf50',
      },
      {
        title: '图片裁剪',
        description: '裁剪图片到指定区域，支持矩形、圆形和智能居中裁剪',
        link: '/crop',
        icon: <CropIcon sx={{ fontSize: 40 }} />,
        color: '#9c27b0',
      },
      {
        title: '旋转翻转',
        description: '旋转或翻转图片，支持自定义角度旋转和镜像翻转',
        link: '/transform',
        icon: <RotateIcon sx={{ fontSize: 40 }} />,
        color: '#673ab7',
      },
      {
        title: '画布调整',
        description: '调整图片画布大小，添加边框或留白，修改画布比例',
        link: '/canvas',
        icon: <CanvasIcon sx={{ fontSize: 40 }} />,
        color: '#607d8b',
      },
      {
        title: '透视校正',
        description: '修正拍摄角度导致的透视变形，支持手动和自动校正',
        link: '/perspective',
        icon: <PerspectiveIcon sx={{ fontSize: 40 }} />,
        color: '#795548',
      },
    ],
  },
  {
    title: '滤镜效果',
    features: [
      {
        title: '基础滤镜',
        description: '应用各种基础滤镜如灰度、褐色、模糊、锐化等效果',
        link: '/filter',
        icon: <FilterIcon sx={{ fontSize: 40 }} />,
        color: '#ff9800',
      },
      {
        title: '艺术滤镜',
        description: '为图片添加艺术效果，如油画、水彩、素描等风格',
        link: '/art-filter',
        icon: <ArtFilterIcon sx={{ fontSize: 40 }} />,
        color: '#e91e63',
      },
      {
        title: '色彩调整',
        description: '专业的色彩调整工具，支持色相饱和度、色彩平衡等',
        link: '/color',
        icon: <ColorIcon sx={{ fontSize: 40 }} />,
        color: '#f44336',
      },
      {
        title: '图片增强',
        description: '高级模糊和锐化效果，提供专业的图像增强功能',
        link: '/enhance',
        icon: <EnhanceIcon sx={{ fontSize: 40 }} />,
        color: '#3f51b5',
      },
      {
        title: '图片噪点',
        description: '添加或降低图片噪点，创建复古效果或清理图片',
        link: '/noise',
        icon: <NoiseIcon sx={{ fontSize: 40 }} />,
        color: '#009688',
      },
      {
        title: '马赛克',
        description: '支持全图或局部马赛克效果，适用于隐私保护',
        link: '/pixelate',
        icon: <PixelateIcon sx={{ fontSize: 40 }} />,
        color: '#ff5722',
      },
    ],
  },
  {
    title: '文字与标注',
    features: [
      {
        title: '添加水印',
        description: '为图片添加自定义文字水印，可调整位置、透明度、颜色等',
        link: '/watermark',
        icon: <WatermarkIcon sx={{ fontSize: 40 }} />,
        color: '#2196f3',
      },
      {
        title: '文字添加',
        description: '添加文字到图片，支持多种字体、颜色、位置、旋转、描边、阴影等丰富效果，支持多行文字和自动换行',
        link: '/text',
        icon: <AdvancedTextIcon sx={{ fontSize: 40 }} />,
        color: '#ba68c8',
      },
      {
        title: '图片标注',
        description: '添加箭头、形状、高亮等标注，支持隐私保护模糊',
        link: '/annotation',
        icon: <AnnotationIcon sx={{ fontSize: 40 }} />,
        color: '#ff8a65',
      },
    ],
  },
  {
    title: '图像合成',
    features: [
      {
        title: '图层混合',
        description: '支持多种图层混合模式，实现专业的图像合成效果',
        link: '/blend',
        icon: <BlendIcon sx={{ fontSize: 40 }} />,
        color: '#cddc39',
      },
      {
        title: '图片拼接',
        description: '支持多张图片的水平、垂直和网格拼接',
        link: '/stitch',
        icon: <StitchIcon sx={{ fontSize: 40 }} />,
        color: '#ffc107',
      },
      {
        title: '图片叠加',
        description: '添加Logo、图片水印或边框到您的图片上',
        link: '/overlay',
        icon: <OverlayIcon sx={{ fontSize: 40 }} />,
        color: '#ff6b6b',
      },
      {
        title: '遮罩效果',
        description: '使用图层遮罩、剪贴遮罩和渐变遮罩处理图片',
        link: '/mask',
        icon: <MaskIcon sx={{ fontSize: 40 }} />,
        color: '#4ecdc4',
      },
    ],
  },
  {
    title: '高级功能',
    features: [

      {
        title: 'GIF处理',
        description: '创建、编辑和优化GIF动图，支持帧提取和文字动画',
        link: '/gif',
        icon: <GifIcon sx={{ fontSize: 40 }} />,
        color: '#f06292',
      },
      {
        title: '格式转换',
        description: '支持常见图片格式互转，包括JPEG、PNG、WebP等',
        link: '/format',
        icon: <FormatIcon sx={{ fontSize: 40 }} />,
        color: '#8bc34a',
      },
    ],
  },
]; 