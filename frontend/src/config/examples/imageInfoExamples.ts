import { EffectExample } from '../../types/api';

// 图片信息查询示例 - 展示实际的API返回结果
// 主要用途：查询普通图片（JPEG、PNG等），GIF作为特殊示例
export const imageInfoExamples: EffectExample[] = [
  {
    title: 'JPEG照片',
    description: '风景照片，展示JPEG格式的基础信息查询',
    originalImage: '/examples/sample-image-1.jpg',
    processedImage: '/examples/sample-image-1.jpg',
    parameters: [
      { label: 'format', value: 'JPEG' },
      { label: 'width × height', value: '1920 × 1080' },
      { label: 'mode', value: 'RGB' },
      { label: 'size', value: '约 500 KB' },
      { label: 'has_alpha', value: 'false' },
      { label: 'color_space', value: 'RGB' },
      { label: 'aspect_ratio', value: '1.78' },
      { label: 'megapixels', value: '2.07' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'JPEG照片',
    description: '人物照片，可能包含EXIF拍摄信息',
    originalImage: '/examples/sample-image-2.jpg',
    processedImage: '/examples/sample-image-2.jpg',
    parameters: [
      { label: 'format', value: 'JPEG' },
      { label: 'mode', value: 'RGB' },
      { label: 'has_alpha', value: 'false' },
      { label: 'color_space', value: 'RGB' },
      { label: 'exif', value: '可能包含相机信息' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'JPEG照片',
    description: '建筑摄影，展示完整的元数据',
    originalImage: '/examples/sample-image-3.jpg',
    processedImage: '/examples/sample-image-3.jpg',
    parameters: [
      { label: 'format', value: 'JPEG' },
      { label: 'mode', value: 'RGB' },
      { label: 'has_alpha', value: 'false' },
      { label: 'color_space', value: 'RGB' },
      { label: 'dpi', value: '可能包含DPI信息' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'PNG图片',
    description: 'PNG格式图片，可能包含透明通道',
    originalImage: '/examples/watermark/watermark-example-1.jpg',
    processedImage: '/examples/watermark/watermark-example-1.jpg',
    parameters: [
      { label: 'format', value: 'JPEG/PNG' },
      { label: 'mode', value: 'RGB/RGBA' },
      { label: 'has_alpha', value: 'true/false' },
      { label: 'color_space', value: 'RGB/RGBA' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画（特殊）',
    description: 'GIF动画特有信息：帧数、持续时间、循环等',
    originalImage: '/examples/gif/basic-animation.gif',
    processedImage: '/examples/gif/basic-animation.gif',
    parameters: [
      { label: 'format', value: 'GIF' },
      { label: 'width × height', value: '400 × 300' },
      { label: 'size', value: '299.37 KB' },
      { label: 'mode', value: 'P (Palette)' },
      { label: 'frame_count', value: '4' },
      { label: 'is_animated', value: 'true' },
      { label: 'duration', value: '300ms' },
      { label: 'loop', value: '0 (无限)' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
];
