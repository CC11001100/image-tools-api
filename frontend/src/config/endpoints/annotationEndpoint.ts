import { ApiEndpoint } from '../../types/api';

export const annotationEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/annotation',
  urlPath: '/api/v1/annotation-by-url',
  description: '在图片上添加各种标注元素，支持矩形、圆形、箭头、文字等多种标注类型。',
  category: '图片标注',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'annotation_type',
      type: 'select',
      description: '标注类型',
      required: true,
      options: ['rectangle', 'circle', 'arrow', 'text', 'highlight'],
      defaultValue: 'rectangle',
    },
    {
      name: 'text',
      type: 'string',
      description: '文字内容（用于文字标注）',
      required: false,
    },
    {
      name: 'color',
      type: 'string',
      description: '标注颜色（十六进制格式）',
      required: false,
      defaultValue: '#FF0000',
    },
    {
      name: 'position',
      type: 'string',
      description: '位置信息（格式根据标注类型而定）',
      required: false,
      defaultValue: '100,100',
    },
    {
      name: 'size',
      type: 'number',
      description: '大小倍数',
      required: false,
      defaultValue: 1.0,
      min: 0.1,
      max: 5.0,
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