import { FilterOption } from './api';

export interface TransformSettings {
  transform_type: 'rotate' | 'flip' | 'skew';
  angle?: number;
  flip_direction?: 'horizontal' | 'vertical' | 'both';
  skew_x?: number;
  skew_y?: number;
  quality?: number;
}

export interface ColorSettings {
  adjustment_type: 'hsl' | 'balance' | 'levels' | 'temperature' | 'duotone';
  quality: number;
  // HSL 调整参数
  hue_shift?: number;
  saturation_scale?: number;
  lightness_scale?: number;
  // 色彩平衡参数
  shadows_cyan_red?: number;
  shadows_magenta_green?: number;
  shadows_yellow_blue?: number;
  // 色阶参数
  black_point?: number;
  white_point?: number;
  gamma?: number;
  // 色温和色调参数
  temperature?: number;
  tint?: number;
  // 双色调参数
  highlight_color?: string;
  shadow_color?: string;
}

export interface BlendSettings {
  mode: string;
  opacity: number;
  mask?: string;
  position?: {
    x: number;
    y: number;
  };
  scale?: number;
  rotation?: number;
}

export interface BlendOption {
  id: string;
  name: string;
  description: string;
  category: string;
  preview?: string;
}

export interface WatermarkSettings {
  watermark_text?: string;
  position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center';
  opacity: number;
  font_size?: number;
  font_color?: string;
  font_family?: string;
  quality: number;
}

export interface ResizeSettings {
  width: number;
  height: number;
  maintain_aspect: boolean;
  resize_mode: 'stretch' | 'fit' | 'fill' | 'crop';
  quality: number;
}

export interface CropSettings {
  crop_type: 'rectangle' | 'circle' | 'ellipse' | 'smart' | 'content-aware' | 'custom';
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  smart_focus?: 'center' | 'face' | 'object';
  quality: number;
}

export interface FilterSettings {
  filter_type: string;
  intensity: number;
  quality: number;
}

export interface EnhanceSettings {
  enhance_type: 'sharpen' | 'denoise' | 'upscale' | 'detail' | 'clarity';
  intensity: number;
  quality: number;
}

export interface NoiseSettings {
  noise_type: 'gaussian' | 'uniform' | 'salt_pepper' | 'poisson';
  intensity: number;
  quality: number;
}

export interface PixelateSettings {
  block_size: number;
  quality: number;
}

export interface MaskSettings {
  mask_type: 'circle' | 'rectangle' | 'ellipse' | 'custom' | 'gradient';
  feather?: number;
  invert?: boolean;
  quality: number;
}

export interface OverlaySettings {
  overlay_type: 'text' | 'image' | 'shape' | 'watermark';
  text?: string;
  position: string;
  opacity: number;
  quality: number;
}

export interface AnnotationSettings {
  annotation_type: 'arrow' | 'rectangle' | 'circle' | 'text' | 'highlight';
  position: string;
  color?: string;
  text?: string;
  quality: number;
}

export interface ArtFilterSettings {
  filter_type: string;
  intensity: number;
  quality: number;
}

export interface StitchSettings {
  stitch_type: 'horizontal' | 'vertical' | 'grid' | 'custom';
  alignment?: 'start' | 'center' | 'end';
  spacing?: number;
  background_color?: string;
  resize_mode?: 'fit_largest' | 'fit_smallest' | 'no_resize';
  quality: number;
}

export interface CanvasSettings {
  canvas_type: 'expand' | 'crop' | 'fit' | 'fill';
  width?: number;
  height?: number;
  background_color?: string;
  position?: 'center' | 'top' | 'bottom' | 'left' | 'right';
  quality: number;
}

export interface PerspectiveSettings {
  auto_document?: boolean;
  points?: string;
  width?: number;
  height?: number;
  quality: number;
}

export interface GifSettings {
  gif_type: 'fade' | 'slide' | 'zoom' | 'rotate';
  duration?: number;
  loop?: boolean;
  quality: number;
}

export interface AdvancedTextSettings {
  text: string;
  style_type: 'gradient' | '3d' | 'shadow' | 'outline' | 'glow';
  font_size: number;
  font_family?: string;
  position: 'center' | 'top' | 'bottom' | 'left' | 'right';
  colors?: string[];
  effects?: {
    shadow?: boolean;
    glow?: boolean;
    outline?: boolean;
    gradient?: boolean;
  };
  quality: number;
}
