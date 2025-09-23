import { StitchExample } from '../../../components/StitchShowcase';

// 网格布局拼接示例 - 不同网格配置
export const gridStitchExamples: StitchExample[] = [
  {
    title: '3x1 网格',
    description: '三张图片单行排列',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '布局', value: 'grid' },
      { label: '列数', value: '3' },
      { label: '间距', value: '10px' }
    ],
    apiParams: {
      stitch_type: 'grid',
      grid_columns: 3,
      spacing: 10,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '1x3 网格',
    description: '三张图片单列排列',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '布局', value: 'grid' },
      { label: '列数', value: '1' },
      { label: '间距', value: '8px' }
    ],
    apiParams: {
      stitch_type: 'grid',
      grid_columns: 1,
      spacing: 8,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '3x3 九宫格',
    description: '九张图片九宫格排列',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '布局', value: 'grid' },
      { label: '列数', value: '3' },
      { label: '间距', value: '6px' }
    ],
    apiParams: {
      stitch_type: 'grid',
      grid_columns: 3,
      spacing: 6,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  },
  {
    title: '4x2 网格',
    description: '八张图片4列2行排列',
    originalImages: [
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
      'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg'
    ],
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    parameters: [
      { label: '布局', value: 'grid' },
      { label: '列数', value: '4' },
      { label: '间距', value: '5px' }
    ],
    apiParams: {
      stitch_type: 'grid',
      grid_columns: 4,
      spacing: 5,
      background_color: '#FFFFFF',
      resize_mode: 'fit_smallest',
      quality: 90
    }
  }
];
