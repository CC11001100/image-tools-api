import { ApiEndpoint } from '../../types/api';

export const gifExtractEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/extract-gif',
  urlPath: '/api/v1/extract-gif-by-url',
  description: 'GIF帧提取',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'application/zip',
  parameters: [
    {
      name: 'output_format',
      type: 'select',
      description: '输出格式',
      required: false,
      options: ['JPEG', 'PNG'],
      defaultValue: 'JPEG'
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量（仅JPEG）',
      required: false,
      min: 10,
      max: 100,
      defaultValue: 90
    },

    {
      name: 'start_frame',
      type: 'number',
      description: '起始帧',
      required: false,
      min: 0,
      defaultValue: 0
    },
    {
      name: 'end_frame',
      type: 'number',
      description: '结束帧',
      required: false,
      min: 0,
      defaultValue: null
    },
    {
      name: 'step',
      type: 'number',
      description: '帧间隔',
      required: false,
      min: 1,
      max: 10,
      defaultValue: 1
    }
  ]
};

export const gifCreateEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/create-gif',
  urlPath: '/api/v1/create-gif-by-url',
  description: 'GIF动画创建',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/gif',
  parameters: [
    {
      name: 'duration',
      type: 'number',
      description: '帧持续时间（毫秒）',
      required: false,
      min: 50,
      max: 2000,
      defaultValue: 500
    },
    {
      name: 'loop',
      type: 'number',
      description: '循环次数（0表示无限）',
      required: false,
      min: 0,
      max: 20,
      defaultValue: 0
    },
    {
      name: 'optimize',
      type: 'boolean',
      description: '启用优化',
      required: false,
      defaultValue: true
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量',
      required: false,
      min: 30,
      max: 100,
      defaultValue: 90
    }
  ]
};

export const gifOptimizeEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/gif',
  urlPath: '/api/v1/gif-by-url',
  description: 'GIF优化压缩',
  category: 'transform',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/gif',
  parameters: [
    {
      name: 'max_colors',
      type: 'number',
      description: '最大颜色数',
      required: false,
      min: 16,
      max: 256,
      defaultValue: 128
    },
    {
      name: 'resize_factor',
      type: 'number',
      description: '缩放比例',
      required: false,
      min: 0.1,
      max: 2.0,
      step: 0.1,
      defaultValue: 1.0
    },
    {
      name: 'target_fps',
      type: 'number',
      description: '目标帧率',
      required: false,
      min: 1,
      max: 30,
      defaultValue: null
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量',
      required: false,
      min: 10,
      max: 100,
      defaultValue: 90
    }
  ]
};

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