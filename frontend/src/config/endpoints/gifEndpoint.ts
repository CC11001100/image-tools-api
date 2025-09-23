import { ApiEndpoint } from '../../types/api';

export const gifEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/gif',
  urlPath: '/api/v1/gif-by-url',
  description: 'GIF图片处理',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/gif',
  parameters: [
    {
      name: 'operation',
      type: 'select',
      description: 'GIF操作类型',
      required: true,
      options: ['extract_frames', 'create_gif', 'optimize'],
      defaultValue: 'extract_frames'
    },
    {
      name: 'frame_delay',
      type: 'number',
      description: '帧延迟（毫秒）',
      required: false,
      min: 10,
      max: 5000,
      defaultValue: 100
    },
    {
      name: 'loop_count',
      type: 'number',
      description: '循环次数（0表示无限循环）',
      required: false,
      min: 0,
      max: 100,
      defaultValue: 0
    },
    {
      name: 'optimize_level',
      type: 'select',
      description: '优化级别',
      required: false,
      options: ['low', 'medium', 'high'],
      defaultValue: 'medium'
    },
    {
      name: 'resize_width',
      type: 'number',
      description: '调整宽度',
      required: false,
      min: 10,
      max: 2000
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量',
      required: false,
      min: 10,
      max: 100,
      defaultValue: 85
    },
    {
      name: 'output_format',
      type: 'select',
      description: '提取帧时的输出格式',
      required: false,
      options: ['jpeg', 'png'],
      defaultValue: 'jpeg'
    }
  ]
}; 