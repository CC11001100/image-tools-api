import { ApiEndpoint } from '../../types/api';

export const formatEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/format',
  urlPath: '/api/format-by-url',
  description: '图片格式转换',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/*',
  parameters: [
    {
      name: 'format',
      type: 'select',
      description: '目标格式',
      required: true,
      options: ['jpeg', 'png', 'webp', 'gif'],
      defaultValue: 'jpeg'
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量（仅适用于JPEG和WebP）',
      required: false,
      min: 1,
      max: 100,
      defaultValue: 90
    },
    {
      name: 'compressionLevel',
      type: 'number',
      description: 'PNG压缩级别',
      required: false,
      min: 0,
      max: 9,
      defaultValue: 6
    },
    {
      name: 'lossless',
      type: 'boolean',
      description: 'WebP无损模式',
      required: false,
      defaultValue: false
    }
  ]
}; 