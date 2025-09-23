import { ApiEndpoint } from '../../types/api';

export const stitchEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/stitch',
  urlPath: '/api/v1/stitch-by-url-test',
  description: '图片拼接',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'layout',
      type: 'select',
      description: '拼接布局',
      required: false,
      options: ['horizontal', 'vertical', 'grid'],
      defaultValue: 'horizontal'
    },
    {
      name: 'spacing',
      type: 'number',
      description: '图片间距（像素）',
      required: false,
      min: 0,
      max: 100,
      defaultValue: 0
    },
    {
      name: 'backgroundColor',
      type: 'color',
      description: '背景颜色',
      required: false,
      defaultValue: '#FFFFFF'
    },
    {
      name: 'gridColumns',
      type: 'number',
      description: '网格布局的列数',
      required: false,
      min: 1,
      max: 10,
      defaultValue: 2
    }
  ]
}; 