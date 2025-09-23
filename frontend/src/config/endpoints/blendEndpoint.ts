import { ApiEndpoint } from '../../types/api';

export const blendEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/blend',
  urlPath: '/api/v1/blend-by-url',
  description: '将两张图片混合在一起，支持多种混合模式和位置调整。',
  category: '图层混合',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'blend_mode',
      type: 'select',
      required: false,
      description: '混合模式',
      options: ['normal', 'multiply', 'screen', 'overlay', 'color-dodge', 'color-burn'],
      defaultValue: 'normal',
    },
    {
      name: 'opacity',
      type: 'number',
      required: false,
      description: '不透明度',
      min: 0,
      max: 1,
      step: 0.05,
      defaultValue: 0.5,
    },
    {
      name: 'position',
      type: 'select',
      required: false,
      description: '位置',
      options: ['center', 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'custom'],
      defaultValue: 'center',
    },
    {
      name: 'scale',
      type: 'number',
      required: false,
      description: '缩放比例',
      min: 0.1,
      max: 5,
      step: 0.1,
      defaultValue: 1.0,
    },
    {
      name: 'quality',
      type: 'number',
      required: false,
      description: '输出质量',
      min: 10,
      max: 100,
      step: 5,
      defaultValue: 90,
    },
  ],
};

export const blendDefaultSettings = {
  blend_mode: 'normal',
  opacity: 0.5,
  position: 'center',
  x_offset: 0,
  y_offset: 0,
  scale: 1.0,
  quality: 90,
};

export const blendModes = [
  { value: 'normal', label: '正常' },
  { value: 'multiply', label: '正片叠底' },
  { value: 'screen', label: '滤色' },
  { value: 'overlay', label: '叠加' },
  { value: 'color-dodge', label: '颜色减淡' },
  { value: 'color-burn', label: '颜色加深' },
]; 