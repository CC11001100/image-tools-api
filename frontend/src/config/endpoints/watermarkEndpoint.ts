import { ApiEndpoint } from '../../types/api';

export const watermarkEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/watermark',
  urlPath: '/api/v1/watermark-by-url-test',
  description: '添加水印',
  category: 'overlay',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'image/jpeg',
  parameters: [
    {
      name: 'text',
      type: 'string',
      description: '水印文字',
      required: false
    },
    {
      name: 'font',
      type: 'select',
      description: '字体',
      required: false,
      options: ['Arial', 'Times New Roman', 'Helvetica', 'Georgia'],
      defaultValue: 'Arial'
    },
    {
      name: 'fontSize',
      type: 'number',
      description: '字体大小',
      required: false,
      min: 8,
      max: 200,
      defaultValue: 24
    },
    {
      name: 'color',
      type: 'color',
      description: '水印颜色',
      required: false,
      defaultValue: '#000000'
    },
    {
      name: 'opacity',
      type: 'number',
      description: '透明度',
      required: false,
      min: 0,
      max: 1,
      defaultValue: 0.5
    },
    {
      name: 'position',
      type: 'select',
      description: '水印位置',
      required: false,
      options: ['center', 'topLeft', 'topRight', 'bottomLeft', 'bottomRight'],
      defaultValue: 'bottomRight'
    },
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
      name: 'margin',
      type: 'number',
      description: '边距（像素）',
      required: false,
      min: 0,
      max: 200,
      defaultValue: 20
    },
    {
      name: 'font_family',
      type: 'select',
      description: '字体系列',
      required: false,
      options: ['Arial', 'Times New Roman', 'Helvetica', 'Georgia'],
      defaultValue: 'Arial'
    },
    {
      name: 'stroke_width',
      type: 'number',
      description: '描边宽度（像素）',
      required: false,
      min: 0,
      max: 10,
      defaultValue: 0
    },
    {
      name: 'stroke_color',
      type: 'color',
      description: '描边颜色',
      required: false,
      defaultValue: '#000000'
    },
    {
      name: 'shadow_offset_x',
      type: 'number',
      description: '阴影X偏移（像素）',
      required: false,
      min: -20,
      max: 20,
      defaultValue: 0
    },
    {
      name: 'shadow_offset_y',
      type: 'number',
      description: '阴影Y偏移（像素）',
      required: false,
      min: -20,
      max: 20,
      defaultValue: 0
    },
    {
      name: 'shadow_color',
      type: 'color',
      description: '阴影颜色',
      required: false,
      defaultValue: '#000000'
    },
    {
      name: 'repeat_mode',
      type: 'select',
      description: '重复模式',
      required: false,
      options: ['none', 'tile', 'diagonal'],
      defaultValue: 'none'
    },
    {
      name: 'margin_x',
      type: 'number',
      description: '水平边距（像素）',
      required: false,
      min: 0,
      max: 200,
      defaultValue: 20
    },
    {
      name: 'margin_y',
      type: 'number',
      description: '垂直边距（像素）',
      required: false,
      min: 0,
      max: 200,
      defaultValue: 20
    },
    {
      name: 'quality',
      type: 'number',
      description: '输出质量（%）',
      required: false,
      min: 1,
      max: 100,
      defaultValue: 90
    }
  ]
}; 