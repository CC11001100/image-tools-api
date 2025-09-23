import { EffectExample } from '../../types/api';

export const noiseExamples: EffectExample[] = [
  {
    title: '高斯噪点',
    description: '添加高斯噪点，模拟传感器噪点效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/noise/original-gaussian.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/noise/noise-gaussian.jpg',
    parameters: [
      { label: '噪点类型', value: '高斯' },
      { label: '强度', value: '15%' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/noise',
      noise_type: 'gaussian',
      intensity: 15,
      quality: 90
    }
  },
  {
    title: '椒盐噪点',
    description: '添加椒盐噪点，产生黑白斑点效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/noise/original-salt_pepper.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/noise/noise-salt_pepper.jpg',
    parameters: [
      { label: '噪点类型', value: '椒盐' },
      { label: '强度', value: '8%' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/noise',
      noise_type: 'salt_and_pepper',
      intensity: 8,
      quality: 90
    }
  },
  {
    title: '泊松噪点',
    description: '添加泊松噪点，模拟光子噪声效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/noise/original-poisson.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/noise/noise-poisson.jpg',
    parameters: [
      { label: '噪点类型', value: '泊松' },
      { label: '强度', value: '12%' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/noise',
      noise_type: 'poisson',
      intensity: 12,
      quality: 90
    }
  }
];
