import { EffectExample } from '../../types/api';

export const transformExamples: EffectExample[] = [
  {
    title: '水平翻转',
    description: '将图片水平翻转，创建镜像效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-original-flip-horizontal.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-flip-horizontal.jpg',
    parameters: [
      { label: '类型', value: '水平翻转' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/transform',
      transform_type: 'flip-horizontal',
      quality: 90
    }
  },
  {
    title: '垂直翻转',
    description: '将图片垂直翻转，上下颠倒',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-original-flip-vertical.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-flip-vertical.jpg',
    parameters: [
      { label: '类型', value: '垂直翻转' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/transform',
      transform_type: 'flip-vertical',
      quality: 90
    }
  },
  {
    title: '顺时针旋转90°',
    description: '将图像顺时针旋转90度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-original-rotate-90-cw.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-rotate-90-cw.jpg',
    parameters: [
      { label: '操作', value: '旋转' },
      { label: '角度', value: '90°' },
      { label: '方向', value: '顺时针' }
    ],
    apiParams: {
      endpoint: '/api/v1/transform',
      transform_type: 'rotate-90-cw',
      quality: 90
    }
  },
  {
    title: '旋转180°',
    description: '将图片旋转180度，完全倒置',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-original-rotate-180.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-rotate-180.jpg',
    parameters: [
      { label: '操作', value: '旋转' },
      { label: '角度', value: '180°' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/transform',
      transform_type: 'rotate-180',
      quality: 90
    }
  },
  {
    title: '逆时针旋转90°',
    description: '将图片逆时针旋转90度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-original-rotate-270.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-rotate-270.jpg',
    parameters: [
      { label: '操作', value: '旋转' },
      { label: '角度', value: '270°' },
      { label: '方向', value: '逆时针' }
    ],
    apiParams: {
      endpoint: '/api/v1/transform',
      transform_type: 'rotate-90-ccw',
      quality: 90
    }
  },
  {
    title: '自定义角度旋转 - 45°',
    description: '将图像旋转45度，创造动感效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-original-rotate-45.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/transform/transform-rotate-45.jpg',
    parameters: [
      { label: '操作', value: '旋转' },
      { label: '角度', value: '45°' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/transform',
      transform_type: 'rotate',
      angle: 45,
      quality: 90
    }
  }
];
