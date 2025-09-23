import { EffectExample } from '../../../types/api';

// 星形遮罩效果示例 (4种)
export const starMaskExamples: EffectExample[] = [
  {
    title: '星形遮罩',
    description: '五角星形遮罩效果，创造独特视觉焦点',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '星形' },
      { label: '角数', value: '5' },
      { label: '羽化', value: '0' },
      { label: '反转', value: '否' }
    ],
    apiParams: {
      endpoint: '/mask/star',
      mask_type: 'star',
      points: 5,
      feather: 0,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '星形羽化遮罩',
    description: '星形遮罩配合羽化效果，边缘柔和',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '星形' },
      { label: '角数', value: '5' },
      { label: '羽化', value: '18' },
      { label: '反转', value: '否' }
    ],
    apiParams: {
      endpoint: '/mask/star',
      mask_type: 'star',
      points: 5,
      feather: 18,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '星形反转遮罩',
    description: '反转星形遮罩，保留外部区域',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '星形' },
      { label: '角数', value: '5' },
      { label: '羽化', value: '12' },
      { label: '反转', value: '是' }
    ],
    apiParams: {
      endpoint: '/mask/star',
      mask_type: 'star',
      points: 5,
      feather: 12,
      invert: true,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '彩色背景星形',
    description: '星形遮罩配合彩色背景，增强装饰效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '星形' },
      { label: '角数', value: '5' },
      { label: '羽化', value: '8' },
      { label: '背景色', value: '金黄色' }
    ],
    apiParams: {
      endpoint: '/mask/star',
      mask_type: 'star',
      points: 5,
      feather: 8,
      invert: false,
      background_color: '#FFD700',
      opacity: 100,
      quality: 90
    }
  }
];
