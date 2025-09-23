import { EffectExample } from '../../../types/api';

// 降噪处理算法示例 (6种)
export const denoiseExamples: EffectExample[] = [
  {
    title: '高斯降噪',
    description: '使用高斯滤波器进行降噪',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '高斯降噪' },
      { label: '强度', value: '1.0' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/gaussian_denoise',
      effect_type: 'gaussian_denoise',
      intensity: 1.0,
      quality: 90
    }
  },
  {
    title: '双边降噪',
    description: '保持边缘的双边滤波降噪',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '双边降噪' },
      { label: '强度', value: '1.2' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/bilateral_denoise',
      effect_type: 'bilateral_denoise',
      intensity: 1.2,
      quality: 90
    }
  },
  {
    title: '自适应降噪',
    description: '根据噪声分布自适应降噪',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '自适应降噪' },
      { label: '强度', value: '1.3' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/adaptive_denoise',
      effect_type: 'adaptive_denoise',
      intensity: 1.3,
      quality: 90
    }
  },
  {
    title: '维纳降噪',
    description: '基于维纳滤波的降噪算法',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '维纳降噪' },
      { label: '强度', value: '1.4' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/wiener_denoise',
      effect_type: 'wiener_denoise',
      intensity: 1.4,
      quality: 90
    }
  },
  {
    title: '形态学降噪',
    description: '使用形态学运算进行降噪',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '形态学降噪' },
      { label: '强度', value: '1.1' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/morphological_denoise',
      effect_type: 'morphological_denoise',
      intensity: 1.1,
      quality: 90
    }
  },
  {
    title: '选择性降噪',
    description: '选择性降噪，保护细节',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '选择性降噪' },
      { label: '强度', value: '1.2' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/selective_denoise',
      effect_type: 'selective_denoise',
      intensity: 1.2,
      quality: 90
    }
  }
];
