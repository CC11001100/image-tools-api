import { ApiEndpoint } from '../../types/api';

export const resizeEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/resize',
  urlPath: '/api/v1/resize-by-url',
  description: '调整图片尺寸',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'width',
      type: 'number',
      description: '目标宽度（像素）',
      required: false,
      min: 1,
      max: 10000
    },
    {
      name: 'height',
      type: 'number',
      description: '目标高度（像素）',
      required: false,
      min: 1,
      max: 10000
    },
    {
      name: 'mode',
      type: 'select',
      description: '调整模式',
      required: false,
      options: ['fit', 'fill', 'stretch'],
      defaultValue: 'fit'
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量',
      required: false,
      min: 1,
      max: 100,
      defaultValue: 90
    },
    {
      name: 'keepAspectRatio',
      type: 'boolean',
      description: '保持宽高比',
      required: false,
      defaultValue: true
    },
    {
      name: 'compressionLevel',
      type: 'number',
      description: '压缩级别',
      required: false,
      min: 0,
      max: 9,
      defaultValue: 6
    }
  ]
}; 