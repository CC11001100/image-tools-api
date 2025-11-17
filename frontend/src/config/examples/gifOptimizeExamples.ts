import { EffectExample } from '../../types/api';

export const gifOptimizeExamples: EffectExample[] = [
  {
    title: '网页优化',
    description: '适合网页展示的GIF优化设置，平衡文件大小和质量',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-web.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/optimized-web.gif',
    parameters: [
      { label: '最大颜色数', value: '128' },
      { label: '缩放比例', value: '80%' },
      { label: '输出质量', value: '85%' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif-optimize',
      max_colors: 128,
      resize_factor: 0.8,
      quality: 85,
    }
  },
  {
    title: '社交媒体',
    description: '适合社交媒体分享的GIF优化，文件小加载快',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-social.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/optimized-social.gif',
    parameters: [
      { label: '最大颜色数', value: '64' },
      { label: '缩放比例', value: '70%' },
      { label: '输出质量', value: '75%' },
      { label: '目标帧率', value: '12fps' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif-optimize',
      max_colors: 64,
      resize_factor: 0.7,
      quality: 75,
      target_fps: 12,
    }
  },
  {
    title: '高质量保留',
    description: '保持高质量的同时适度优化文件大小',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-quality.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/optimized-quality.gif',
    parameters: [
      { label: '最大颜色数', value: '256' },
      { label: '缩放比例', value: '100%' },
      { label: '输出质量', value: '95%' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif-optimize',
      max_colors: 256,
      resize_factor: 1.0,
      quality: 95,
    }
  },
  {
    title: '极限压缩',
    description: '最大程度压缩文件大小，适合带宽有限的场景',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-extreme.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/optimized-extreme.gif',
    parameters: [
      { label: '最大颜色数', value: '32' },
      { label: '缩放比例', value: '50%' },
      { label: '输出质量', value: '60%' },
      { label: '目标帧率', value: '8fps' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif-optimize',
      max_colors: 32,
      resize_factor: 0.5,
      quality: 60,
      target_fps: 8,
    }
  },
  {
    title: '流畅动画',
    description: '保持动画流畅度，适度优化文件大小',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-smooth.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/optimized-smooth.gif',
    parameters: [
      { label: '最大颜色数', value: '128' },
      { label: '缩放比例', value: '90%' },
      { label: '输出质量', value: '90%' },
      { label: '目标帧率', value: '20fps' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif-optimize',
      max_colors: 128,
      resize_factor: 0.9,
      quality: 90,
      target_fps: 20,
    }
  },
  {
    title: '移动端优化',
    description: '针对移动设备优化，考虑屏幕尺寸和网络条件',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-mobile.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/optimized-mobile.gif',
    parameters: [
      { label: '最大颜色数', value: '96' },
      { label: '缩放比例', value: '60%' },
      { label: '输出质量', value: '80%' },
      { label: '目标帧率', value: '15fps' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif-optimize',
      max_colors: 96,
      resize_factor: 0.6,
      quality: 80,
      target_fps: 15,
    }
  }
]; 