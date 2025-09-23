import { ApiEndpoint } from '../../types/api';

export const transformEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/transform',
  urlPath: '/api/v1/transform-by-url',
  description: '图片变换',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'rotation',
      type: 'number',
      description: '旋转角度',
      required: false,
      min: -360,
      max: 360,
      defaultValue: 0
    },
    {
      name: 'flipHorizontal',
      type: 'boolean',
      description: '水平翻转',
      required: false,
      defaultValue: false
    },
    {
      name: 'flipVertical',
      type: 'boolean',
      description: '垂直翻转',
      required: false,
      defaultValue: false
    },
    {
      name: 'skewX',
      type: 'number',
      description: '水平倾斜角度',
      required: false,
      min: -90,
      max: 90,
      defaultValue: 0
    },
    {
      name: 'skewY',
      type: 'number',
      description: '垂直倾斜角度',
      required: false,
      min: -90,
      max: 90,
      defaultValue: 0
    }
  ]
}; 