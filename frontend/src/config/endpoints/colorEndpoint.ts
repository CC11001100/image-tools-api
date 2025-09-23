import { ApiEndpoint } from '../../types/api';

export const colorEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/color',
  urlPath: '/api/v1/color-by-url',
  description: '专业的色彩调整工具，支持色相饱和度、色彩平衡、色阶等多种调整方式。',
  category: '色彩调整',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'adjustment_type',
      type: 'select',
      required: true,
      description: '调整类型',
      options: ['hsl', 'balance', 'levels', 'temperature', 'duotone'],
      defaultValue: 'hsl',
    },
    {
      name: 'hue_shift',
      type: 'number',
      required: false,
      description: '色相偏移（-180到180）',
      min: -180,
      max: 180,
      defaultValue: 0,
    },
    {
      name: 'saturation_scale',
      type: 'number',
      required: false,
      description: '饱和度缩放（0到2）',
      min: 0,
      max: 2,
      defaultValue: 1.0,
    },
    {
      name: 'lightness_scale',
      type: 'number',
      required: false,
      description: '亮度缩放（0到2）',
      min: 0,
      max: 2,
      defaultValue: 1.0,
    },
    {
      name: 'quality',
      type: 'number',
      required: false,
      description: '输出质量（10-100）',
      defaultValue: 90,
      min: 10,
      max: 100,
    },
  ],
};

export const colorDefaultSettings = {
  adjustment_type: 'hsl',
  hue_shift: 0,
  saturation_scale: 1.0,
  lightness_scale: 1.0,
  quality: 90,
};

export const colorAdjustmentTypes = [
  {
    type: 'hsl',
    path: '/api/v1/color/hsl',
    name: '色相/饱和度/亮度',
    description: '调整图片的色相、饱和度和亮度',
  },
  {
    type: 'balance',
    path: '/api/v1/color/balance',
    name: '色彩平衡',
    description: '调整阴影、中间调和高光的色彩平衡',
  },
  {
    type: 'levels',
    path: '/api/v1/color/levels',
    name: '色阶',
    description: '调整图片的黑场、白场和中间调',
  },
  {
    type: 'temperature',
    path: '/api/v1/color/temperature',
    name: '色温色调',
    description: '调整图片的色温（冷暖）和色调',
  },
  {
    type: 'duotone',
    path: '/api/v1/color/duotone',
    name: '双色调',
    description: '创建双色调艺术效果',
  },
]; 