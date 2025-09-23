import { ApiEndpoint } from '../../types/api';

export const enhanceEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/enhance',
  urlPath: '/api/enhance-by-url',
  description: '图片增强',
  category: 'enhance',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'brightness',
      type: 'number',
      description: '亮度调整',
      required: false,
      min: -100,
      max: 100,
      defaultValue: 0
    },
    {
      name: 'contrast',
      type: 'number',
      description: '对比度调整',
      required: false,
      min: -100,
      max: 100,
      defaultValue: 0
    },
    {
      name: 'saturation',
      type: 'number',
      description: '饱和度调整',
      required: false,
      min: -100,
      max: 100,
      defaultValue: 0
    },
    {
      name: 'sharpness',
      type: 'number',
      description: '锐化程度',
      required: false,
      min: 0,
      max: 100,
      defaultValue: 0
    },
    {
      name: 'denoise',
      type: 'number',
      description: '降噪强度',
      required: false,
      min: 0,
      max: 100,
      defaultValue: 0
    },
    {
      name: 'mode',
      type: 'select',
      description: '增强模式',
      required: false,
      options: ['auto', 'manual', 'hdr'],
      defaultValue: 'manual'
    }
  ]
}; 