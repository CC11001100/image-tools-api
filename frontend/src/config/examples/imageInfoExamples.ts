import { EffectExample } from '../../types/api';

export const imageInfoExamples: EffectExample[] = [
  {
    title: '基础动画GIF',
    description: '查看4帧GIF动画的完整信息',
    originalImage: '/examples/gif/basic-animation.gif',
    processedImage: '/examples/gif/basic-animation.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '尺寸', value: '400×300' },
      { label: '帧数', value: '4帧' },
      { label: '大小', value: '299 KB' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: '快速动画GIF',
    description: '查看高速动画GIF信息（150ms/帧）',
    originalImage: '/examples/gif/fast-animation.gif',
    processedImage: '/examples/gif/fast-animation.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '3帧' },
      { label: '持续时间', value: '150ms' },
      { label: '动画', value: '是' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: '慢速动画GIF',
    description: '查看慢速动画GIF信息（600ms/帧）',
    originalImage: '/examples/gif/slow-animation.gif',
    processedImage: '/examples/gif/slow-animation.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '3帧' },
      { label: '持续时间', value: '600ms' },
      { label: '循环', value: '无限' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: '循环动画GIF',
    description: '查看有限次循环的GIF信息',
    originalImage: '/examples/gif/loop-animation.gif',
    processedImage: '/examples/gif/loop-animation.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '2帧' },
      { label: '循环次数', value: '3次' },
      { label: '持续时间', value: '400ms' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: '高帧率GIF',
    description: '查看高帧率GIF动画信息（5帧）',
    originalImage: '/examples/gif/high-fps.gif',
    processedImage: '/examples/gif/high-fps.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '5帧' },
      { label: '持续时间', value: '100ms' },
      { label: '颜色模式', value: 'Palette' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: '简单切换GIF',
    description: '查看2帧简单切换GIF信息',
    originalImage: '/examples/gif/simple-switch.gif',
    processedImage: '/examples/gif/simple-switch.gif',
    parameters: [
      { label: '格式', value: 'GIF' },
      { label: '帧数', value: '2帧' },
      { label: '持续时间', value: '500ms' },
      { label: '循环', value: '无限' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
];
