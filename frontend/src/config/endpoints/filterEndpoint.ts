import { ApiEndpoint } from '../../types/api';

export const filterEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/filter',
  urlPath: '/api/v1/filter-by-url',
  description: '对图片应用基础滤镜效果，如灰度、褐色、模糊、锐化等。支持强度调节，可以创建不同程度的效果。',
  category: '基础滤镜',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'filter_type',
      type: 'select',
      description: '滤镜类型',
      required: true,
      defaultValue: 'grayscale',
      options: [
        // 基础滤镜
        'grayscale', 'sepia', 'blur', 'sharpen', 'brightness', 'contrast',
        // 色彩效果
        'saturate', 'desaturate', 'warm', 'cool', 'vintage', 'hueshift', 'gamma', 'levels',
        // 艺术效果
        'emboss', 'posterize', 'solarize', 'invert', 'edge_enhance', 'smooth', 'detail',
        // 黑白效果
        'monochrome', 'dramatic_bw', 'infrared', 'high_contrast_bw',
        // 复古和胶片效果
        'film_grain', 'retro', 'polaroid', 'lomo', 'analog', 'crossprocess',
        // 特殊效果
        'dream', 'glow', 'soft_focus', 'noise', 'vignette', 'mosaic',
        // 滤镜效果
        'find_edges', 'contour', 'edge_enhance_more', 'smooth_more', 'unsharp_mask',
        // 创意效果
        'pencil', 'sketch', 'cartoon', 'hdr', 'cyberpunk', 'noir', 'faded', 'pastel'
      ],
    },
    {
      name: 'intensity',
      type: 'number',
      description: '效果强度，范围0.1-2.0',
      required: false,
      defaultValue: 1.0,
      min: 0.1,
      max: 2.0,
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量',
      required: false,
      defaultValue: 90,
      min: 10,
      max: 100,
    },
  ],
}; 