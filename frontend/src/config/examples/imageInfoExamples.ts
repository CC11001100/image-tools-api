import { EffectExample } from '../../types/api';

// 图片信息查询示例 - 展示不同类型图片的信息获取能力
// 注意：此功能不处理图片，只读取信息，所以没有"处理后"的图片
export const imageInfoExamples: EffectExample[] = [
  {
    title: 'JPEG照片 - 风景图',
    description: '查看JPEG格式照片的详细信息，包括尺寸、大小、颜色模式等',
    originalImage: '/examples/sample-image-1.jpg',
    processedImage: '/examples/sample-image-1.jpg', // 图片信息查询不改变图片
    parameters: [
      { label: '格式', value: 'JPEG' },
      { label: '颜色模式', value: 'RGB' },
      { label: '用途', value: '照片、网页' },
      { label: '特点', value: '有损压缩' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'JPEG照片 - 人物图',
    description: '查看人物照片的详细信息，可能包含EXIF拍摄信息',
    originalImage: '/examples/sample-image-2.jpg',
    processedImage: '/examples/sample-image-2.jpg',
    parameters: [
      { label: '格式', value: 'JPEG' },
      { label: '颜色模式', value: 'RGB' },
      { label: 'EXIF', value: '可能包含' },
      { label: '用途', value: '照片存储' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'JPEG照片 - 建筑图',
    description: '查看建筑摄影的详细信息，了解图片的完整元数据',
    originalImage: '/examples/sample-image-3.jpg',
    processedImage: '/examples/sample-image-3.jpg',
    parameters: [
      { label: '格式', value: 'JPEG' },
      { label: '颜色模式', value: 'RGB' },
      { label: 'DPI', value: '可能包含' },
      { label: '用途', value: '商业摄影' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画 - 4帧循环',
    description: '查看GIF动画的完整信息：帧数、持续时间、循环次数等',
    originalImage: '/examples/gif/basic-animation.gif',
    processedImage: '/examples/gif/basic-animation.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '4帧' },
      { label: '动画', value: '是' },
      { label: '持续时间', value: '300ms' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画 - 高帧率',
    description: '查看高帧率GIF的动画信息，了解播放速度和帧数',
    originalImage: '/examples/gif/high-fps.gif',
    processedImage: '/examples/gif/high-fps.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '5帧' },
      { label: '持续时间', value: '100ms' },
      { label: '特点', value: '流畅动画' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画 - 慢速切换',
    description: '查看慢速GIF动画的信息，适合幻灯片效果',
    originalImage: '/examples/gif/slow-animation.gif',
    processedImage: '/examples/gif/slow-animation.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '3帧' },
      { label: '持续时间', value: '600ms' },
      { label: '特点', value: '缓慢切换' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
];
