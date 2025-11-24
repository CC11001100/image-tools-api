import { EffectExample } from '../../types/api';

// 图片信息查询示例 - 展示实际的API返回结果
// 注意：此功能不处理图片，只读取信息，parameters展示的是查询结果的关键字段
export const imageInfoExamples: EffectExample[] = [
  {
    title: 'GIF动画 - 基础信息',
    description: '4帧循环GIF动画，展示完整的动画信息查询结果',
    originalImage: '/examples/gif/basic-animation.gif',
    processedImage: '/examples/gif/basic-animation.gif', // 保持一致，因为不处理图片
    parameters: [
      { label: 'format', value: 'GIF' },
      { label: 'width × height', value: '400 × 300' },
      { label: 'size', value: '299.37 KB' },
      { label: 'mode', value: 'P (Palette)' },
      { label: 'frame_count', value: '4' },
      { label: 'is_animated', value: 'true' },
      { label: 'duration', value: '300ms' },
      { label: 'loop', value: '0 (无限)' },
      { label: 'aspect_ratio', value: '1.33' },
      { label: 'megapixels', value: '0.12' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画 - 高帧率',
    description: '5帧高帧率GIF，100ms快速切换效果',
    originalImage: '/examples/gif/high-fps.gif',
    processedImage: '/examples/gif/high-fps.gif',
    parameters: [
      { label: 'format', value: 'GIF' },
      { label: 'frame_count', value: '5' },
      { label: 'is_animated', value: 'true' },
      { label: 'duration', value: '100ms' },
      { label: 'color_space', value: 'Palette (8-bit)' },
      { label: 'loop', value: '0 (无限)' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画 - 慢速切换',
    description: '3帧慢速GIF，600ms缓慢切换，适合幻灯片',
    originalImage: '/examples/gif/slow-animation.gif',
    processedImage: '/examples/gif/slow-animation.gif',
    parameters: [
      { label: 'format', value: 'GIF' },
      { label: 'frame_count', value: '3' },
      { label: 'is_animated', value: 'true' },
      { label: 'duration', value: '600ms' },
      { label: 'loop', value: '0 (无限)' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画 - 快速动画',
    description: '3帧快速GIF，150ms高速切换效果',
    originalImage: '/examples/gif/fast-animation.gif',
    processedImage: '/examples/gif/fast-animation.gif',
    parameters: [
      { label: 'format', value: 'GIF' },
      { label: 'frame_count', value: '3' },
      { label: 'is_animated', value: 'true' },
      { label: 'duration', value: '150ms' },
      { label: 'loop', value: '0 (无限)' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画 - 简单切换',
    description: '2帧简单切换，500ms中速播放',
    originalImage: '/examples/gif/simple-switch.gif',
    processedImage: '/examples/gif/simple-switch.gif',
    parameters: [
      { label: 'format', value: 'GIF' },
      { label: 'frame_count', value: '2' },
      { label: 'is_animated', value: 'true' },
      { label: 'duration', value: '500ms' },
      { label: 'loop', value: '0 (无限)' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
  {
    title: 'GIF动画 - 有限循环',
    description: '2帧GIF，循环3次后停止',
    originalImage: '/examples/gif/loop-animation.gif',
    processedImage: '/examples/gif/loop-animation.gif',
    parameters: [
      { label: 'format', value: 'GIF' },
      { label: 'frame_count', value: '2' },
      { label: 'is_animated', value: 'true' },
      { label: 'duration', value: '400ms' },
      { label: 'loop', value: '3 (有限循环)' },
    ],
    apiParams: {
      endpoint: '/api/v1/image-info',
    }
  },
];
