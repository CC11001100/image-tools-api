import { EffectExample } from '../../types/api';

// 图像增强效果示例
export const enhanceExamples: EffectExample[] = [
  {
    title: '锐化增强',
    description: '增强图像锐度，提升细节清晰度',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/original-sharpen.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/enhance-sharpen.jpg",
    parameters: [
      { label: '效果类型', value: '锐化' },
      { label: '强度', value: '1.5' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/enhance',
      effect_type: 'sharpen',
      intensity: 1.5,
      quality: 90
    }
  },
  {
    title: '模糊效果',
    description: '添加高斯模糊效果，柔化图像',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/original-blur.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/enhance-blur.jpg",
    parameters: [
      { label: '效果类型', value: '模糊' },
      { label: '强度', value: '2.0' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/enhance',
      effect_type: 'blur',
      intensity: 2.0,
      quality: 90
    }
  },
  {
    title: '细节增强',
    description: '增强图像细节和纹理信息',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/original-detail.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/enhance-detail.jpg",
    parameters: [
      { label: '效果类型', value: '细节增强' },
      { label: '强度', value: '2.0' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/enhance',
      effect_type: 'detail',
      intensity: 2.0,
      quality: 90
    }
  },
  {
    title: '边缘增强',
    description: '增强图像边缘信息，突出轮廓',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/original-edge-enhance.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/enhance-edge-enhance.jpg",
    parameters: [
      { label: '效果类型', value: '边缘增强' },
      { label: '强度', value: '1.5' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/enhance',
      effect_type: 'edge_enhance',
      intensity: 1.5,
      quality: 90
    }
  },
  {
    title: '平滑处理',
    description: '平滑图像表面，减少噪点',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/original-smooth.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/enhance-smooth.jpg",
    parameters: [
      { label: '效果类型', value: '平滑' },
      { label: '强度', value: '2.0' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/enhance',
      effect_type: 'smooth',
      intensity: 2.0,
      quality: 90
    }
  },
  {
    title: '浮雕效果',
    description: '创建浮雕立体效果',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/original-emboss.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/enhance/enhance-emboss.jpg",
    parameters: [
      { label: '效果类型', value: '浮雕' },
      { label: '强度', value: '1.0' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/enhance',
      effect_type: 'emboss',
      intensity: 1.0,
      quality: 90
    }
  }
];
