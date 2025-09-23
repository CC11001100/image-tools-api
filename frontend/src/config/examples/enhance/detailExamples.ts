import { EffectExample } from '../../../types/api';

// 细节增强算法示例 (8种)
export const detailExamples: EffectExample[] = [
  {
    title: '细节增强',
    description: '增强图像细节和纹理',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '细节增强' },
      { label: '强度', value: '1.5' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/detail',
      effect_type: 'detail_enhance',
      intensity: 1.5,
      quality: 90
    }
  },
  {
    title: '结构增强',
    description: '增强图像的结构信息',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '结构增强' },
      { label: '强度', value: '1.3' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/structure',
      effect_type: 'structure_enhance',
      intensity: 1.3,
      quality: 90
    }
  },
  {
    title: '纹理增强',
    description: '突出表面纹理细节',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '纹理增强' },
      { label: '强度', value: '1.4' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/texture',
      effect_type: 'texture_enhance',
      intensity: 1.4,
      quality: 90
    }
  },
  {
    title: '微对比度',
    description: '增强局部微对比度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '微对比度' },
      { label: '强度', value: '1.2' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/micro_contrast',
      effect_type: 'micro_contrast',
      intensity: 1.2,
      quality: 90
    }
  },
  {
    title: '清晰度增强',
    description: '提升整体清晰度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '清晰度增强' },
      { label: '强度', value: '1.6' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/clarity',
      effect_type: 'clarity_enhance',
      intensity: 1.6,
      quality: 90
    }
  },
  {
    title: '锐度增强',
    description: '增强图像锐度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '锐度增强' },
      { label: '强度', value: '1.7' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/sharpness',
      effect_type: 'sharpness_enhance',
      intensity: 1.7,
      quality: 90
    }
  },
  {
    title: '局部对比度',
    description: '增强局部对比度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '局部对比度' },
      { label: '强度', value: '1.4' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/local_contrast',
      effect_type: 'local_contrast',
      intensity: 1.4,
      quality: 90
    }
  },
  {
    title: '自适应增强',
    description: '自适应的图像增强',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '自适应增强' },
      { label: '强度', value: '1.5' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/adaptive',
      effect_type: 'adaptive_enhance',
      intensity: 1.5,
      quality: 90
    }
  }
];
