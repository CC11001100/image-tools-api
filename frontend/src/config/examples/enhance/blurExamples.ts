import { EffectExample } from '../../../types/api';

// 模糊效果算法示例 (8种)
export const blurExamples: EffectExample[] = [
  {
    title: '动态模糊',
    description: '模拟运动物体的模糊效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '动态模糊' },
      { label: '强度', value: '2.0' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/motion',
      effect_type: 'motion_blur',
      intensity: 2.0,
      quality: 90
    }
  },
  {
    title: '径向模糊',
    description: '从中心向外的径向模糊效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '径向模糊' },
      { label: '强度', value: '1.8' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/radial',
      effect_type: 'radial_blur',
      intensity: 1.8,
      quality: 90
    }
  },
  {
    title: '表面模糊',
    description: '保持边缘清晰的表面模糊',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '表面模糊' },
      { label: '强度', value: '1.5' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/surface',
      effect_type: 'surface_blur',
      intensity: 1.5,
      quality: 90
    }
  },
  {
    title: '高斯模糊',
    description: '经典的高斯模糊效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '高斯模糊' },
      { label: '强度', value: '1.3' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/gaussian',
      effect_type: 'gaussian_blur',
      intensity: 1.3,
      quality: 90
    }
  },
  {
    title: '镜头模糊',
    description: '模拟镜头景深模糊效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '镜头模糊' },
      { label: '强度', value: '1.6' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/lens',
      effect_type: 'lens_blur',
      intensity: 1.6,
      quality: 90
    }
  },
  {
    title: '缩放模糊',
    description: '模拟缩放时的模糊效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '缩放模糊' },
      { label: '强度', value: '1.4' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/zoom',
      effect_type: 'zoom_blur',
      intensity: 1.4,
      quality: 90
    }
  },
  {
    title: '智能模糊',
    description: '保护边缘的智能模糊算法',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '智能模糊' },
      { label: '强度', value: '1.2' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/smart',
      effect_type: 'smart_blur',
      intensity: 1.2,
      quality: 90
    }
  },
  {
    title: '旋转模糊',
    description: '围绕中心点的旋转模糊效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '算法', value: '旋转模糊' },
      { label: '强度', value: '1.7' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/enhance/spin',
      effect_type: 'spin_blur',
      intensity: 1.7,
      quality: 90
    }
  }
];
