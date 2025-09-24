import { ApiEndpoint } from '../../types/api';

export const cropEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/crop',
  urlPath: '/api/v1/crop-by-url',
  description: '裁剪图片',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'x',
      type: 'number',
      description: '裁剪起始点X坐标',
      required: false,
      min: 0,
      defaultValue: 0
    },
    {
      name: 'y',
      type: 'number',
      description: '裁剪起始点Y坐标',
      required: false,
      min: 0,
      defaultValue: 0
    },
    {
      name: 'width',
      type: 'number',
      description: '裁剪宽度',
      required: false,
      min: 1
    },
    {
      name: 'height',
      type: 'number',
      description: '裁剪高度',
      required: false,
      min: 1
    },
    {
      name: 'mode',
      type: 'select',
      description: '裁剪模式',
      required: false,
      options: ['rectangle', 'circle', 'ellipse'],
      defaultValue: 'rectangle'
    },
    {
      name: 'aspectRatio',
      type: 'select',
      description: '宽高比',
      required: false,
      options: ['free', '1:1', '4:3', '16:9', '3:4', '9:16'],
      defaultValue: 'free'
    }
  ]
}; 