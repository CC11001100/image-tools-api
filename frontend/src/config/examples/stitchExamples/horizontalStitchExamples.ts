import { StitchExample } from '../../../components/StitchShowcase';

// 水平拼接变化示例 - 不同间距、对齐方式、多图排列
export const horizontalStitchExamples: StitchExample[] = [
  {
    title: '水平无间距',
    description: '水平紧密拼接，无间隔',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '间距', value: '0px' },
      { label: '对齐', value: 'middle' }
    ],
    apiParams: {
      stitch_type: 'horizontal',
      alignment: 'center',
      spacing: 0,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '水平大间距',
    description: '水平拼接，大间距分隔',
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '间距', value: '30px' },
      { label: '对齐', value: 'middle' }
    ],
    apiParams: {
      stitch_type: 'horizontal',
      alignment: 'center',
      spacing: 30,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '水平顶部对齐',
    description: '水平拼接，顶部对齐',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '间距', value: '15px' },
      { label: '对齐', value: 'top' }
    ],
    apiParams: {
      stitch_type: 'horizontal',
      alignment: 'top',
      spacing: 15,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '水平底部对齐',
    description: '水平拼接，底部对齐',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg"
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '间距', value: '15px' },
      { label: '对齐', value: 'bottom' }
    ],
    apiParams: {
      stitch_type: 'horizontal',
      alignment: 'bottom',
      spacing: 15,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '三图水平排列',
    description: '三张图片水平连续排列',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '图片数', value: '3张' },
      { label: '间距', value: '12px' }
    ],
    apiParams: {
      stitch_type: 'horizontal',
      alignment: 'center',
      spacing: 12,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  }
];
