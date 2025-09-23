import { EffectExample } from '../../../types/api';

// 其他增强算法示例 (边缘处理、纹理、高级、创意、专业等)
export const otherExamples: EffectExample[] = [
  // 边缘处理类
  {
    title: '边缘增强',
    description: '增强图像边缘信息',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '边缘增强' },
      { label: '强度', value: '1.5' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/edge_enhance',
      effect_type: 'edge_enhance',
      intensity: 1.5,
      quality: 90
    }
  },
  {
    title: 'HDR增强',
    description: '高动态范围图像增强',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: 'HDR增强' },
      { label: '强度', value: '2.0' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/hdr',
      effect_type: 'hdr_enhance',
      intensity: 2.0,
      quality: 90
    }
  },
  {
    title: '戏剧性增强',
    description: '增强图像的戏剧性效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '戏剧性增强' },
      { label: '强度', value: '1.8' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/dramatic',
      effect_type: 'dramatic_enhance',
      intensity: 1.8,
      quality: 90
    }
  },
  {
    title: '人像增强',
    description: '专门针对人像的增强算法',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '人像增强' },
      { label: '强度', value: '1.3' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/portrait',
      effect_type: 'portrait_enhance',
      intensity: 1.3,
      quality: 90
    }
  },
  {
    title: '风景增强',
    description: '专门针对风景的增强算法',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '风景增强' },
      { label: '强度', value: '1.6' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/landscape',
      effect_type: 'landscape_enhance',
      intensity: 1.6,
      quality: 90
    }
  },
  {
    title: '艺术增强',
    description: '艺术风格的图像增强',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '艺术增强' },
      { label: '强度', value: '2.2' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/artistic',
      effect_type: 'artistic_enhance',
      intensity: 2.2,
      quality: 90
    }
  }
];
