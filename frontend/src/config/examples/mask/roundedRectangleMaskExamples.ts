import { EffectExample } from '../../../types/api';

// 圆角矩形遮罩效果示例 (4种)
export const roundedRectangleMaskExamples: EffectExample[] = [
  {
    title: '圆角矩形',
    description: '圆角矩形遮罩，兼具矩形规整和圆形柔和',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆角矩形' },
      { label: '圆角半径', value: '20' },
      { label: '羽化', value: '0' },
      { label: '反转', value: '否' }
    ],
    apiParams: {
      endpoint: '/mask/rounded_rectangle',
      mask_type: 'rounded_rectangle',
      corner_radius: 20,
      feather: 0,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '圆角矩形轻度羽化',
    description: '圆角矩形遮罩配合轻度羽化，边缘自然',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆角矩形' },
      { label: '圆角半径', value: '25' },
      { label: '羽化', value: '10' },
      { label: '反转', value: '否' }
    ],
    apiParams: {
      endpoint: '/mask/rounded_rectangle',
      mask_type: 'rounded_rectangle',
      corner_radius: 25,
      feather: 10,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '圆角矩形重度羽化',
    description: '圆角矩形遮罩配合重度羽化，极其柔和',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆角矩形' },
      { label: '圆角半径', value: '30' },
      { label: '羽化', value: '40' },
      { label: '反转', value: '否' }
    ],
    apiParams: {
      endpoint: '/mask/rounded_rectangle',
      mask_type: 'rounded_rectangle',
      corner_radius: 30,
      feather: 40,
      invert: false,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '圆角矩形反转',
    description: '反转圆角矩形遮罩，保留外部区域',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '类型', value: '圆角矩形' },
      { label: '圆角半径', value: '35' },
      { label: '羽化', value: '15' },
      { label: '反转', value: '是' }
    ],
    apiParams: {
      endpoint: '/mask/rounded_rectangle',
      mask_type: 'rounded_rectangle',
      corner_radius: 35,
      feather: 15,
      invert: true,
      background_color: '#000000',
      opacity: 100,
      quality: 90
    }
  }
];
