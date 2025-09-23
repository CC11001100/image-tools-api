import { ApiEndpoint } from '../../types/api';

export const perspectiveEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/perspective',
  urlPath: '/api/v1/perspective-by-url',
  description: '透视变换处理',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'mode',
      type: 'select',
      description: '透视变换模式',
      required: false,
      options: ['auto', 'manual'],
      defaultValue: 'auto'
    },
    {
      name: 'points',
      type: 'string',
      description: '手动模式下的四个角点坐标，格式：x1,y1,x2,y2,x3,y3,x4,y4',
      required: false
    }
  ]
}; 