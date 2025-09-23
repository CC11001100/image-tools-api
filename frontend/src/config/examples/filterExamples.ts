import { EffectExample } from '../../types/api';

// Filter 效果示例
export const filterExamples: EffectExample[] = [
  {
    title: '模糊效果',
    description: '为图像添加模糊效果，可用于背景虚化或隐私保护',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-original-blur.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-blur.jpg',
    parameters: [
      { label: '滤镜类型', value: '模糊' },
      { label: '强度', value: '150%' }
    ],
    apiParams: {
      endpoint: '/api/v1/filter',
      filter_type: 'blur',
      intensity: 1.5
    }
  },
  {
    title: '锐化效果',
    description: '增强图片的细节和边缘清晰度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-original-sharpen.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-sharpen.jpg',
    parameters: [
      { label: '滤镜类型', value: '锐化' },
      { label: '强度', value: '180%' }
    ],
    apiParams: {
      endpoint: '/api/v1/filter',
      filter_type: 'sharpen',
      intensity: 1.8
    }
  },
  {
    title: '浮雕效果',
    description: '创建立体浮雕效果，突出图像轮廓',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-original-emboss.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-emboss.jpg',
    parameters: [
      { label: '滤镜类型', value: '浮雕' },
      { label: '强度', value: '120%' }
    ],
    apiParams: {
      endpoint: '/api/v1/filter',
      filter_type: 'emboss',
      intensity: 1.2
    }
  },
  {
    title: '灰度效果',
    description: '将彩色图片转换为黑白灰度图',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-original-grayscale.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-grayscale.jpg',
    parameters: [
      { label: '滤镜类型', value: '灰度' },
      { label: '强度', value: '100%' }
    ],
    apiParams: {
      endpoint: '/api/v1/filter',
      filter_type: 'grayscale',
      intensity: 1.0
    }
  },
  {
    title: '复古效果',
    description: '添加复古怀旧色调，营造经典氛围',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-original-vintage.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-vintage.jpg',
    parameters: [
      { label: '滤镜类型', value: '复古' },
      { label: '强度', value: '130%' }
    ],
    apiParams: {
      endpoint: '/api/v1/filter',
      filter_type: 'vintage',
      intensity: 1.3
    }
  },
  {
    title: '亮度调整',
    description: '调整图片亮度，增强明暗对比效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-original-brightness.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-brightness.jpg',
    parameters: [
      { label: '滤镜类型', value: '亮度' },
      { label: '强度', value: '140%' }
    ],
    apiParams: {
      endpoint: '/api/v1/filter',
      filter_type: 'brightness',
      intensity: 1.4
    }
  }
];
