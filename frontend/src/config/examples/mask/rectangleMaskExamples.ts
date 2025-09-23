import { EffectExample } from '../../../types/api';

// 矩形遮罩效果示例 (5种)
export const rectangleMaskExamples: EffectExample[] = [
  {
    title: '矩形遮罩',
    description: '标准矩形遮罩效果，适合规整构图',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '矩形' },
      { label: '羽化', value: '0' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/rectangle',
      mask_type: 'rectangle',
      feather: 0,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '矩形轻度羽化',
    description: '矩形遮罩配合轻度羽化，边缘稍微柔化',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '矩形' },
      { label: '羽化', value: '8' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/rectangle',
      mask_type: 'rectangle',
      feather: 8,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '矩形中度羽化',
    description: '矩形遮罩配合中度羽化，边缘平滑过渡',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '矩形' },
      { label: '羽化', value: '20' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/rectangle',
      mask_type: 'rectangle',
      feather: 20,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '矩形反转遮罩',
    description: '反转矩形遮罩，保留外部区域，隐藏中心矩形',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '矩形' },
      { label: '羽化', value: '15' },
      { label: '反转', value: '是' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/rectangle',
      mask_type: 'rectangle',
      feather: 15,
      invert: true,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '黑色背景矩形',
    description: '矩形遮罩配合纯黑背景，强调主体区域',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '矩形' },
      { label: '羽化', value: '3' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '纯黑' }
    ],
    apiParams: {
      endpoint: '/mask/rectangle',
      mask_type: 'rectangle',
      feather: 3,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  }
];
