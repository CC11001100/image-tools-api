import { EffectExample } from '../../../types/api';

// 心形遮罩效果示例 (4种)
export const heartMaskExamples: EffectExample[] = [
  {
    title: '心形遮罩',
    description: '浪漫心形遮罩效果，适合情感主题',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '心形' },
      { label: '羽化', value: '0' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/heart',
      mask_type: 'heart',
      feather: 0,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '心形羽化遮罩',
    description: '心形遮罩配合羽化效果，边缘柔和浪漫',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '心形' },
      { label: '羽化', value: '20' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/heart',
      mask_type: 'heart',
      feather: 20,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '心形反转遮罩',
    description: '反转心形遮罩，保留外部区域',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '心形' },
      { label: '羽化', value: '15' },
      { label: '反转', value: '是' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/heart',
      mask_type: 'heart',
      feather: 15,
      invert: true,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '彩色背景心形',
    description: '心形遮罩配合彩色背景，增强视觉效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '心形' },
      { label: '羽化', value: '10' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '粉红色' }
    ],
    apiParams: {
      endpoint: '/mask/heart',
      mask_type: 'heart',
      feather: 10,
      invert: false,
      background_color: '#FFB6C1',
      opacity: 100,
      quality: 90
    }
  }
];
