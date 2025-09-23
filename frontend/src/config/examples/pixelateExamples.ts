import { EffectExample } from '../../types/api';

export const pixelateExamples: EffectExample[] = [
  {
    title: '像素化效果',
    description: '对整张图片应用10像素马赛克，像素化效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/original-pixelate.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/pixelate-pixelate.jpg',
    parameters: [
      { label: '像素大小', value: '10px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/pixelate',
      block_size: 10,
      quality: 90
    }
  },
  {
    title: '马赛克效果',
    description: '对整张图片应用20像素马赛克，马赛克效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/original-mosaic.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/pixelate-mosaic.jpg',
    parameters: [
      { label: '像素大小', value: '20px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/pixelate',
      block_size: 20,
      quality: 90
    }
  },
  {
    title: '复古像素',
    description: '对整张图片应用8像素马赛克，复古像素效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/original-retro.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/pixelate-retro.jpg',
    parameters: [
      { label: '像素大小', value: '8px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/pixelate',
      block_size: 8,
      quality: 90
    }
  },
  {
    title: '低分辨率',
    description: '对整张图片应用30像素马赛克，低分辨率效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/original-lowres.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/pixelate-lowres.jpg',
    parameters: [
      { label: '像素大小', value: '30px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/pixelate',
      block_size: 30,
      quality: 90
    }
  }
];
