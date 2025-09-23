import { ApiEndpoint } from '../../types/api';

export const maskEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/mask',
  urlPath: '/api/v1/mask-by-url-test',
  description: '为图片应用各种形状的遮罩效果。',
  category: '遮罩效果',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'mask_type',
      type: 'select',
      description: '遮罩类型',
      required: true,
      defaultValue: 'circle',
      options: ['circle', 'rectangle', 'ellipse', 'rounded_rectangle', 'heart', 'star'],
    },
    {
      name: 'feather',
      type: 'number',
      description: '羽化程度',
      required: false,
      defaultValue: 0,
      min: 0,
      max: 100,
    },
    {
      name: 'invert',
      type: 'boolean',
      description: '是否反转遮罩',
      required: false,
      defaultValue: false,
    },
    {
      name: 'background_color',
      type: 'string',
      description: '背景颜色（十六进制）',
      required: false,
      defaultValue: '#FFFFFF',
    },
    {
      name: 'opacity',
      type: 'number',
      description: '遮罩不透明度',
      required: false,
      defaultValue: 1.0,
      min: 0,
      max: 1,
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量',
      required: false,
      defaultValue: 90,
      min: 10,
      max: 100,
    },
  ],
}; 