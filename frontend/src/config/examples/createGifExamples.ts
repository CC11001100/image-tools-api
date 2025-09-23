import { EffectExample } from '../../types/api';

export const createGifExamples: EffectExample[] = [
  {
    title: '标准GIF创建',
    description: '将多张图片合成为标准GIF动画',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/create-gif/frame-standard-1.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/create-gif/create-gif-standard.gif',
    parameters: [
      { label: '帧间隔', value: '500ms' },
      { label: '循环', value: '无限' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/gif/create',
      duration: 500,
      loop: 0,
      optimize: true
    }
  },
  {
    title: '快速GIF创建',
    description: '创建快速播放的GIF动画',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/create-gif/frame-fast-1.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/create-gif/create-gif-fast.gif',
    parameters: [
      { label: '帧间隔', value: '200ms' },
      { label: '循环', value: '无限' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/gif/create',
      duration: 200,
      loop: 0,
      optimize: true
    }
  },
  {
    title: '慢速GIF创建',
    description: '创建慢速播放的GIF动画',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/create-gif/frame-slow-1.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/create-gif/create-gif-slow.gif',
    parameters: [
      { label: '帧间隔', value: '1000ms' },
      { label: '循环', value: '无限' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/gif/create',
      duration: 1000,
      loop: 0,
      optimize: true
    }
  }
];
