import { ApiEndpoint } from '../../types/api';

export const advancedTextEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/text',
  urlPath: '/api/v1/text-by-url',
  description: '高级文字效果处理',
  category: 'text',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/png',
  parameters: [
    {
      name: 'text',
      type: 'string',
      description: '要添加的文字内容',
      required: true
    },
    {
      name: 'font',
      type: 'select',
      description: '字体选择',
      required: false,
      options: ['Arial', 'Impact', 'Helvetica', 'Times New Roman'],
      defaultValue: 'Arial'
    },
    {
      name: 'color',
      type: 'color',
      description: '文字颜色',
      required: false,
      defaultValue: '#000000'
    },
    {
      name: 'depth',
      type: 'number',
      description: '3D深度效果（像素）',
      required: false,
      min: 0,
      max: 50,
      defaultValue: 0
    },
    {
      name: 'glowIntensity',
      type: 'number',
      description: '发光强度',
      required: false,
      min: 0,
      max: 100,
      defaultValue: 0
    },
    {
      name: 'shininess',
      type: 'number',
      description: '金属光泽度',
      required: false,
      min: 0,
      max: 100,
      defaultValue: 0
    }
  ]
}; 