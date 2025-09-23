import { EffectExample } from '../../../types/api';

// 锐化增强算法示例 (6种)
export const sharpenExamples: EffectExample[] = [
  {
    title: 'USM锐化',
    description: 'Unsharp Mask锐化，专业级细节增强',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: 'USM锐化' },
      { label: '强度', value: '1.5' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/usm',
      effect_type: 'usm_sharpen',
      intensity: 1.5,
      quality: 90
    }
  },
  {
    title: '智能锐化',
    description: '自适应的智能锐化算法，避免噪点放大',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '智能锐化' },
      { label: '强度', value: '1.3' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/smart',
      effect_type: 'smart_sharpen',
      intensity: 1.3,
      quality: 90
    }
  },
  {
    title: '边缘锐化',
    description: '只对边缘进行选择性锐化处理',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '边缘锐化' },
      { label: '强度', value: '1.8' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/edge',
      effect_type: 'edge_sharpen',
      intensity: 1.8,
      quality: 90
    }
  },
  {
    title: '高通锐化',
    description: '使用高通滤波器进行锐化',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '高通锐化' },
      { label: '强度', value: '1.4' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/high_pass',
      effect_type: 'high_pass_sharpen',
      intensity: 1.4,
      quality: 90
    }
  },
  {
    title: '卷积锐化',
    description: '使用卷积核进行锐化处理',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '卷积锐化' },
      { label: '强度', value: '1.6' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/convolution',
      effect_type: 'convolution_sharpen',
      intensity: 1.6,
      quality: 90
    }
  },
  {
    title: '选择性锐化',
    description: '选择性锐化，保护平滑区域',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '选择性锐化' },
      { label: '强度', value: '1.7' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/selective',
      effect_type: 'selective_sharpen',
      intensity: 1.7,
      quality: 90
    }
  }
];
