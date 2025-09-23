import { ApiEndpoint } from '../../types/api';

export const canvasEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/canvas',
  urlPath: '/api/v1/canvas-by-url',
  description: '画布处理，支持画布扩展、画布缩放、边框添加等功能。可以调整画布大小、添加背景色或边框。',
  category: '画布处理',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'canvas_type',
      type: 'select',
      required: true,
      description: '画布类型',
      options: ['expand', 'fit', 'border', 'background'],
      defaultValue: 'expand',
    },
    {
      name: 'width',
      type: 'number',
      required: false,
      description: '画布宽度',
      min: 1,
      max: 5000,
      defaultValue: 800,
    },
    {
      name: 'height',
      type: 'number',
      required: false,
      description: '画布高度',
      min: 1,
      max: 5000,
      defaultValue: 600,
    },
    {
      name: 'background_color',
      type: 'color',
      required: false,
      description: '背景颜色',
      defaultValue: '#FFFFFF',
    },
    {
      name: 'border_width',
      type: 'number',
      required: false,
      description: '边框宽度',
      min: 0,
      max: 100,
      defaultValue: 10,
    },
    {
      name: 'border_color',
      type: 'color',
      required: false,
      description: '边框颜色',
      defaultValue: '#000000',
    },
    {
      name: 'position',
      type: 'select',
      required: false,
      description: '图片位置',
      options: ['center', 'top-left', 'top-center', 'top-right', 'bottom-left', 'bottom-center', 'bottom-right'],
      defaultValue: 'center',
    },
    {
      name: 'quality',
      type: 'number',
      required: false,
      description: '输出质量（10-100）',
      defaultValue: 90,
      min: 10,
      max: 100,
    },
  ],
};

export const canvasDefaultSettings = {
  canvas_type: 'expand',
  width: 800,
  height: 600,
  background_color: '#FFFFFF',
  border_width: 10,
  border_color: '#000000',
  position: 'center',
  quality: 90,
}; 