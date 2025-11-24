import { EffectExample } from '../../types/api';

export const imageInfoExamples: EffectExample[] = [
  {
    title: 'JPEG照片',
    description: '查看JPEG格式照片的详细信息',
    originalImage: '/examples/crop/crop_sample_1.jpg',
    processedImage: '/examples/crop/crop_sample_1.jpg',
    parameters: [
      { label: '格式', value: 'JPEG' },
      { label: '尺寸', value: '800×600' },
      { label: '大小', value: '~150 KB' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'PNG图片',
    description: '查看PNG格式图片信息，包括透明通道',
    originalImage: '/examples/filter/blur_sample_1.jpg',
    processedImage: '/examples/filter/blur_sample_1.jpg',
    parameters: [
      { label: '格式', value: 'PNG' },
      { label: '透明通道', value: '支持' },
      { label: '颜色模式', value: 'RGBA' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画',
    description: '查看GIF动画的帧数、持续时间等信息',
    originalImage: '/examples/gif/basic-animation.gif',
    processedImage: '/examples/gif/basic-animation.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '4帧' },
      { label: '动画', value: '是' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: '高分辨率图片',
    description: '查看大尺寸图片的详细参数',
    originalImage: '/examples/crop/crop_sample_2.jpg',
    processedImage: '/examples/crop/crop_sample_2.jpg',
    parameters: [
      { label: '百万像素', value: '~2MP' },
      { label: '宽高比', value: '16:9' },
      { label: 'DPI', value: '72×72' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: '小尺寸图片',
    description: '查看缩略图等小尺寸图片信息',
    originalImage: '/examples/crop/crop_sample_3.jpg',
    processedImage: '/examples/crop/crop_sample_3.jpg',
    parameters: [
      { label: '格式', value: 'JPEG' },
      { label: '尺寸', value: '小于1MB' },
      { label: '颜色', value: 'RGB' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF静态图',
    description: '区分静态GIF和动画GIF',
    originalImage: '/examples/gif/simple-switch.gif',
    processedImage: '/examples/gif/simple-switch.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '2帧' },
      { label: '循环', value: '无限' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
];
