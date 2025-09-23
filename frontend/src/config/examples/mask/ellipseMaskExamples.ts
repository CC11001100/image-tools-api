import { EffectExample } from '../../../types/api';

// 椭圆遮罩效果示例 (6种)
export const ellipseMaskExamples: EffectExample[] = [
  {
    title: '椭圆遮罩',
    description: '椭圆形遮罩效果，适合横向或纵向构图',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '椭圆' },
      { label: '羽化', value: '0' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/ellipse',
      mask_type: 'ellipse',
      feather: 0,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '椭圆轻度羽化',
    description: '椭圆遮罩配合轻度羽化，边缘自然过渡',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '椭圆' },
      { label: '羽化', value: '12' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/ellipse',
      mask_type: 'ellipse',
      feather: 12,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '椭圆羽化',
    description: '椭圆遮罩配合中度羽化，柔和边缘效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '椭圆' },
      { label: '羽化', value: '30' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/ellipse',
      mask_type: 'ellipse',
      feather: 30,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '椭圆重度羽化',
    description: '椭圆遮罩配合重度羽化，极其柔和的边缘',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '椭圆' },
      { label: '羽化', value: '60' },
      { label: '反转', value: '否' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/ellipse',
      mask_type: 'ellipse',
      feather: 60,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '椭圆反转遮罩',
    description: '反转椭圆遮罩，保留外部区域',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '椭圆' },
      { label: '羽化', value: '18' },
      { label: '反转', value: '是' },
      { label: '背景色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/mask/ellipse',
      mask_type: 'ellipse',
      feather: 18,
      invert: true,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '半透明椭圆',
    description: '半透明椭圆遮罩，创造朦胧艺术效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '椭圆' },
      { label: '羽化', value: '25' },
      { label: '反转', value: '否' },
      { label: '透明度', value: '60%' }
    ],
    apiParams: {
      endpoint: '/mask/ellipse',
      mask_type: 'ellipse',
      feather: 25,
      invert: false,
      background_color: '#000000',
      opacity: 60,
      quality: 90
    }
  }
];
