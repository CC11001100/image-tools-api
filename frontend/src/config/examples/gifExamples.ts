import { EffectExample } from '../../types/api';

export const gifExamples: EffectExample[] = [
  {
    title: 'GIF压缩优化',
    description: '压缩GIF文件大小，减少颜色数量',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-optimize.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/gif-optimize.gif',
    parameters: [
      { label: '最大颜色数', value: '64' },
      { label: '缩放比例', value: '0.8' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/gif',
      max_colors: 64,
      resize_factor: 0.8,
      optimize: true
    }
  },
  {
    title: 'GIF帧率调整',
    description: '调整GIF播放帧率，控制播放速度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-fps.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/gif-fps.gif',
    parameters: [
      { label: '目标帧率', value: '15 FPS' },
      { label: '优化', value: '启用' },
      { label: '质量', value: '高' }
    ],
    apiParams: {
      endpoint: '/api/v1/gif',
      target_fps: 15,
      optimize: true,
      quality: 90
    }
  },
  {
    title: 'GIF尺寸调整',
    description: '调整GIF尺寸，保持动画效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-resize.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/gif-resize.gif',
    parameters: [
      { label: '缩放比例', value: '0.6' },
      { label: '优化', value: '启用' },
      { label: '保持比例', value: '是' }
    ],
    apiParams: {
      endpoint: '/api/v1/gif',
      resize_factor: 0.6,
      optimize: true,
      maintain_aspect: true
    }
  }
];
