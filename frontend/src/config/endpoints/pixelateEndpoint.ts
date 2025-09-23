import { ApiEndpoint } from '../../types/api';

export const pixelateEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/pixelate',
  urlPath: '/api/pixelate-by-url',
  description: '像素化处理',
  category: 'effect',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'blockSize',
      type: 'number',
      description: '像素块大小',
      required: false,
      min: 1,
      max: 100,
      defaultValue: 10
    },
    {
      name: 'region',
      type: 'string',
      description: '处理区域坐标，格式：x,y,width,height',
      required: false
    },
    {
      name: 'mode',
      type: 'select',
      description: '像素化模式',
      required: false,
      options: ['normal', 'mosaic', 'blur'],
      defaultValue: 'normal'
    }
  ]
}; 