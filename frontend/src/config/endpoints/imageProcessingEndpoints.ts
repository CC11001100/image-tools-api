import { ApiEndpoint } from '../apiEndpoints';

// 图像处理API端点 (6个)
export const imageProcessingEndpoints: ApiEndpoint[] = [
  // 艺术滤镜
  {
    method: 'POST',
    path: '/api/v1/art-filter',
    urlPath: '/api/v1/art-filter-by-url',
    description: '应用艺术风格滤镜，创造独特的视觉效果',
    category: '艺术滤镜',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'style',
        type: 'select',
        required: true,
        description: '艺术风格',
        options: ['oil_painting', 'watercolor', 'sketch', 'cartoon', 'vintage', 'noir']
      },
      {
        name: 'intensity',
        type: 'number',
        required: false,
        description: '效果强度',
        defaultValue: 0.8,
        min: 0.1,
        max: 1.0
      }
    ]
  },
  // 色彩调整
  {
    method: 'POST',
    path: '/api/v1/color',
    urlPath: '/api/v1/color-by-url',
    description: '调整图片的色彩属性，包括亮度、对比度、饱和度等',
    category: '色彩调整',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'brightness',
        type: 'number',
        required: false,
        description: '亮度调整',
        defaultValue: 0,
        min: -100,
        max: 100
      },
      {
        name: 'contrast',
        type: 'number',
        required: false,
        description: '对比度调整',
        defaultValue: 0,
        min: -100,
        max: 100
      },
      {
        name: 'saturation',
        type: 'number',
        required: false,
        description: '饱和度调整',
        defaultValue: 0,
        min: -100,
        max: 100
      },
      {
        name: 'hue',
        type: 'number',
        required: false,
        description: '色相调整',
        defaultValue: 0,
        min: -180,
        max: 180
      }
    ]
  },
  // 增强效果
  {
    method: 'POST',
    path: '/api/v1/enhance',
    urlPath: '/api/v1/enhance-by-url',
    description: '图像增强处理，提升图片质量和视觉效果',
    category: '增强效果',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'enhance_type',
        type: 'select',
        required: true,
        description: '增强类型',
        options: ['auto_enhance', 'denoise', 'sharpen', 'detail_enhance', 'hdr']
      },
      {
        name: 'strength',
        type: 'number',
        required: false,
        description: '增强强度',
        defaultValue: 0.5,
        min: 0.1,
        max: 1.0
      }
    ]
  },
  // 噪点处理
  {
    method: 'POST',
    path: '/api/v1/noise',
    urlPath: '/api/v1/noise-by-url',
    description: '噪点处理，包括降噪和添加噪点效果',
    category: '噪点处理',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'operation',
        type: 'select',
        required: true,
        description: '操作类型',
        options: ['denoise', 'add_noise']
      },
      {
        name: 'intensity',
        type: 'number',
        required: false,
        description: '处理强度',
        defaultValue: 0.5,
        min: 0.1,
        max: 1.0
      },
      {
        name: 'noise_type',
        type: 'select',
        required: false,
        description: '噪点类型（添加噪点时使用）',
        options: ['gaussian', 'salt_pepper', 'uniform'],
        defaultValue: 'gaussian'
      }
    ]
  },
  // 马赛克
  {
    method: 'POST',
    path: '/api/v1/pixelate',
    urlPath: '/api/v1/pixelate-by-url',
    description: '马赛克效果，创建像素化的视觉效果',
    category: '马赛克',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'pixel_size',
        type: 'number',
        required: false,
        description: '像素块大小',
        defaultValue: 10,
        min: 2,
        max: 50
      },
      {
        name: 'region',
        type: 'select',
        required: false,
        description: '应用区域',
        options: ['full', 'center', 'custom'],
        defaultValue: 'full'
      }
    ]
  },
  // 透视校正
  {
    method: 'POST',
    path: '/api/v1/perspective',
    urlPath: '/api/v1/perspective-by-url',
    description: '透视校正，修正图片的透视变形',
    category: '透视校正',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'correction_type',
        type: 'select',
        required: true,
        description: '校正类型',
        options: ['auto', 'manual', 'document']
      },
      {
        name: 'strength',
        type: 'number',
        required: false,
        description: '校正强度',
        defaultValue: 1.0,
        min: 0.1,
        max: 2.0
      }
    ]
  }
];
