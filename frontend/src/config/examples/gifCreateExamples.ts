import { EffectExample } from '../../types/api';

export const gifCreateExamples: EffectExample[] = [
  {
    title: '快速动画',
    description: '创建快速播放的GIF动画，适合展示动作序列',
    originalImage: '/examples/gif/fast-animation-frame-1.jpg',
    processedImage: '/examples/gif/fast-animation.gif',
    parameters: [
      { label: '帧持续时间', value: '100ms' },
      { label: '帧率', value: '10 FPS' },
      { label: '循环次数', value: '无限' },
      { label: '优化', value: '启用' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/create',
      duration: 100,
      loop: 0,
      optimize: true,
      quality: 85,
    }
  },
  {
    title: '流畅动画',
    description: '创建流畅的GIF动画，平衡速度和质量',
    originalImage: '/examples/gif/basic-animation-frame-1.jpg',
    processedImage: '/examples/gif/basic-animation.gif',
    parameters: [
      { label: '帧持续时间', value: '200ms' },
      { label: '帧率', value: '5 FPS' },
      { label: '循环次数', value: '无限' },
      { label: '质量', value: '90%' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/create',
      duration: 200,
      loop: 0,
      optimize: true,
      quality: 90,
    }
  },
  {
    title: '慢速展示',
    description: '创建慢速播放的GIF，适合详细展示过程',
    originalImage: '/examples/gif/slow-animation-frame-1.jpg',
    processedImage: '/examples/gif/slow-animation.gif',
    parameters: [
      { label: '帧持续时间', value: '800ms' },
      { label: '帧率', value: '1.25 FPS' },
      { label: '循环次数', value: '3次' },
      { label: '质量', value: '95%' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/create',
      duration: 800,
      loop: 3,
      optimize: false,
      quality: 95,
    }
  },
  {
    title: '高质量动画',
    description: '创建高质量GIF动画，保持最佳视觉效果',
    originalImage: '/examples/gif/high-fps-frame-1.jpg',
    processedImage: '/examples/gif/high-fps.gif',
    parameters: [
      { label: '帧持续时间', value: '300ms' },
      { label: '帧率', value: '3.33 FPS' },
      { label: '循环次数', value: '无限' },
      { label: '质量', value: '100%' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/create',
      duration: 300,
      loop: 0,
      optimize: false,
      quality: 100,
    }
  },
  {
    title: '压缩动画',
    description: '创建文件较小的GIF动画，适合网络传输',
    originalImage: '/examples/gif/simple-switch-frame-1.jpg',
    processedImage: '/examples/gif/simple-switch.gif',
    parameters: [
      { label: '帧持续时间', value: '250ms' },
      { label: '帧率', value: '4 FPS' },
      { label: '循环次数', value: '无限' },
      { label: '质量', value: '60%' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/create',
      duration: 250,
      loop: 0,
      optimize: true,
      quality: 60,
    }
  },
  {
    title: '循环展示',
    description: '创建有限循环的GIF动画，适合演示用途',
    originalImage: '/examples/gif/loop-animation-frame-1.jpg',
    processedImage: '/examples/gif/loop-animation.gif',
    parameters: [
      { label: '帧持续时间', value: '500ms' },
      { label: '帧率', value: '2 FPS' },
      { label: '循环次数', value: '5次' },
      { label: '质量', value: '85%' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/create',
      duration: 500,
      loop: 5,
      optimize: true,
      quality: 85,
    }
  }
]; 