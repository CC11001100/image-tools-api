import { EffectExample } from '../../../types/api';

// 圆形遮罩效果示例 (7种)
export const circleMaskExamples: EffectExample[] = [
  {
    title: '圆形遮罩 - 标准',
    description: '标准圆形遮罩效果，适合突出中心主体',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆形' },
      { label: '羽化', value: '0' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/circle',
      mask_type: 'circle',
      feather: 0,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '圆形轻度羽化',
    description: '圆形遮罩配合轻度羽化，边缘柔和自然',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆形' },
      { label: '羽化', value: '10' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/circle',
      mask_type: 'circle',
      feather: 10,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '圆形中度羽化',
    description: '圆形遮罩配合中度羽化，边缘过渡更加平滑',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆形' },
      { label: '羽化', value: '25' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/circle',
      mask_type: 'circle',
      feather: 25,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '圆形重度羽化',
    description: '圆形遮罩配合重度羽化，边缘极其柔和',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆形' },
      { label: '羽化', value: '50' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/circle',
      mask_type: 'circle',
      feather: 50,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '圆形反转遮罩',
    description: '反转圆形遮罩，保留外部区域，隐藏中心',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆形' },
      { label: '羽化', value: '15' },
      { label: '反转', value: '是' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/circle',
      mask_type: 'circle',
      feather: 15,
      invert: true,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '半透明圆形',
    description: '半透明圆形遮罩，创造朦胧效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆形' },
      { label: '羽化', value: '20' },
      { label: '反转', value: '否' },
      { label: '透明度', value: '50%' }
    ],
    apiParams: {
      endpoint: '/mask/circle',
      mask_type: 'circle',
      feather: 20,
      invert: false,
      background_color: '#000000',
      opacity: 50,
      quality: 90
    }
  },
  {
    title: '黑色背景圆形',
    description: '圆形遮罩配合纯黑背景，突出主体',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆形' },
      { label: '羽化', value: '5' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '纯黑' }
    ],
    apiParams: {
      endpoint: '/mask/circle',
      mask_type: 'circle',
      feather: 5,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  }
];
