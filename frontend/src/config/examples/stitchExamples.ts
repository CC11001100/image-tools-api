import { EffectExample, MultiImageEffectExample } from '../../types/api';

// 多图拼接示例（完整数据）
export const stitchMultiImageExamples: MultiImageEffectExample[] = [
  {
    title: '水平拼接',
    description: '将多张图片水平排列拼接成一张长图',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-horizontal.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-horizontal.jpg'
    ],
    originalImageLabels: ['图片1', '图片2'],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-horizontal.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '间距', value: '10px' },
      { label: '图片尺寸', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'horizontal',
      spacing: 10,
      quality: 90
    }
  },
  {
    title: '垂直拼接',
    description: '将多张图片垂直排列拼接成一张高图',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-vertical.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-vertical.jpg'
    ],
    originalImageLabels: ['图片1', '图片2'],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-vertical.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '间距', value: '5px' },
      { label: '图片尺寸', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'vertical',
      spacing: 5,
      quality: 90
    }
  },
  {
    title: '网格拼接',
    description: '将四张图片排列成2x2网格布局',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-grid.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-grid.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original3-grid.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original4-grid.jpg'
    ],
    originalImageLabels: ['图片1', '图片2', '图片3', '图片4'],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-grid.jpg',
    parameters: [
      { label: '方向', value: 'grid' },
      { label: '间距', value: '8px' },
      { label: '图片尺寸', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'grid',
      spacing: 8,
      quality: 90
    }
  },
  {
    title: '自由拼接',
    description: '自定义位置和间距的灵活拼接方式',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-free.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-free.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original3-free.jpg'
    ],
    originalImageLabels: ['图片1', '图片2', '图片3'],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-free.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '间距', value: '15px' },
      { label: '图片尺寸', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'horizontal',
      spacing: 15,
      quality: 90
    }
  },
  {
    title: '背景拼接',
    description: '带背景色的图片拼接，增强视觉效果',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-background.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-background.jpg'
    ],
    originalImageLabels: ['图片1', '图片2'],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-background.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '间距', value: '20px' },
      { label: '图片尺寸', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'horizontal',
      spacing: 20,
      quality: 90
    }
  },
  {
    title: '间距拼接',
    description: '带间隔的图片拼接，营造层次感',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-spacing.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original2-spacing.jpg'
    ],
    originalImageLabels: ['图片1', '图片2'],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-spacing.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '间距', value: '30px' },
      { label: '图片尺寸', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'vertical',
      spacing: 30,
      quality: 90
    }
  }
];

// 转换为标准EffectExample格式（用于兼容现有组件）
export const stitchExamples: EffectExample[] = stitchMultiImageExamples.map(example => ({
  ...example,
  originalImage: example.originalImages[0], // 使用第一张图片作为代表
  // 更新参数说明，显示多张图片信息
  parameters: [
    ...example.parameters,
    { label: '原图数量', value: `${example.originalImages.length}张` }
  ]
}));
