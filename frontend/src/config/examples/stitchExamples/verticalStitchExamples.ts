import { StitchExample } from '../../../components/StitchShowcase';

// 垂直拼接变化示例 - 不同间距、对齐方式、多图排列
export const verticalStitchExamples: StitchExample[] = [
  {
    title: '垂直无间距',
    description: '垂直紧密拼接，无间隔',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '间距', value: '0px' },
      { label: '对齐', value: 'center' }
    ],
    apiParams: {
      stitch_type: 'vertical',
      alignment: 'center',
      spacing: 0,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '垂直左对齐',
    description: '垂直拼接，左侧对齐',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg"
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '间距', value: '10px' },
      { label: '对齐', value: 'left' }
    ],
    apiParams: {
      stitch_type: 'vertical',
      alignment: 'left',
      spacing: 10,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '垂直右对齐',
    description: '垂直拼接，右侧对齐',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '间距', value: '10px' },
      { label: '对齐', value: 'right' }
    ],
    apiParams: {
      stitch_type: 'vertical',
      alignment: 'right',
      spacing: 10,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '三图垂直排列',
    description: '三张图片垂直连续排列',
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '图片数', value: '3张' },
      { label: '间距', value: '15px' }
    ],
    apiParams: {
      stitch_type: 'vertical',
      alignment: 'center',
      spacing: 15,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  }
];
