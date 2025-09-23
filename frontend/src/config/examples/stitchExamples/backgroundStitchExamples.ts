import { StitchExample } from '../../../components/StitchShowcase';

// 背景色变化拼接示例 - 不同背景色效果
export const backgroundStitchExamples: StitchExample[] = [
  {
    title: '黑色背景拼接',
    description: '深色背景的图片拼接',
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '背景色', value: '黑色' },
      { label: '间距', value: '20px' }
    ],
    apiParams: {
      stitch_type: 'horizontal',
      alignment: 'center',
      spacing: 20,
      background_color: '#000000',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '彩色背景拼接',
    description: '蓝色背景的图片拼接',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '背景色', value: '蓝色' },
      { label: '间距', value: '25px' }
    ],
    apiParams: {
      stitch_type: 'vertical',
      alignment: 'center',
      spacing: 25,
      background_color: '#0000FF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '灰色背景网格',
    description: '灰色背景的网格拼接',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '布局', value: 'grid' },
      { label: '背景色', value: '灰色' },
      { label: '间距', value: '15px' }
    ],
    apiParams: {
      stitch_type: 'grid',
      grid_columns: 2,
      spacing: 15,
      background_color: '#808080',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  }
];
