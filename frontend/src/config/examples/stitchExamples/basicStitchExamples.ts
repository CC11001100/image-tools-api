import { StitchExample } from '../../../components/StitchShowcase';

// 基础拼接示例 - 水平、垂直、网格基本排列
export const basicStitchExamples: StitchExample[] = [
  {
    title: '水平拼接',
    description: '将两张图片水平排列拼接',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg"
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '间距', value: '10px' },
      { label: '对齐', value: 'middle' }
    ],
    apiParams: {
      stitch_type: 'horizontal',
      alignment: 'center',
      spacing: 10,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '垂直拼接',
    description: '将两张图片垂直排列拼接',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '间距', value: '15px' },
      { label: '对齐', value: 'center' }
    ],
    apiParams: {
      stitch_type: 'vertical',
      alignment: 'center',
      spacing: 15,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '网格拼接',
    description: '四张图片排列成2x2网格',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '布局', value: 'grid' },
      { label: '列数', value: '2' },
      { label: '间距', value: '8px' }
    ],
    apiParams: {
      stitch_type: 'grid',
      grid_columns: 2,
      spacing: 8,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  }
];
