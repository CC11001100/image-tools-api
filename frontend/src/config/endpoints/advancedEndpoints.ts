import { ApiEndpoint } from '../apiEndpoints';

// 高级功能API端点 (7个)
export const advancedEndpoints: ApiEndpoint[] = [
  // 文字处理
  {
    method: 'POST',
    path: '/api/v1/text',
    urlPath: '/api/v1/text-by-url',
    description: '在图片上添加文字，支持多种字体效果和样式',
    category: '文字处理',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'text',
        type: 'string',
        required: true,
        description: '要添加的文字内容'
      },
      {
        name: 'font_size',
        type: 'number',
        required: false,
        description: '字体大小',
        defaultValue: 48,
        min: 8,
        max: 200
      },
      {
        name: 'font_color',
        type: 'color',
        required: false,
        description: '字体颜色',
        defaultValue: '#000000'
      },
      {
        name: 'position',
        type: 'select',
        required: false,
        description: '文字位置',
        options: ['center', 'top-left', 'top-center', 'top-right', 'center-left', 'center-right', 'bottom-left', 'bottom-center', 'bottom-right'],
        defaultValue: 'center'
      },
      {
        name: 'font_style',
        type: 'select',
        required: false,
        description: '字体样式',
        options: ['normal', 'bold', 'italic', 'shadow', 'outline'],
        defaultValue: 'normal'
      }
    ]
  },
  // 图层混合
  {
    method: 'POST',
    path: '/api/v1/blend',
    urlPath: '/api/v1/blend-by-url',
    description: '图层混合，将两张图片按指定模式混合',
    category: '图层混合',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'overlay_image',
        type: 'file',
        required: true,
        description: '叠加图片'
      },
      {
        name: 'blend_mode',
        type: 'select',
        required: false,
        description: '混合模式',
        options: ['normal', 'multiply', 'screen', 'overlay', 'soft_light', 'hard_light'],
        defaultValue: 'normal'
      },
      {
        name: 'opacity',
        type: 'number',
        required: false,
        description: '叠加图片透明度',
        defaultValue: 0.5,
        min: 0.0,
        max: 1.0
      }
    ]
  },
  // 图片拼接
  {
    method: 'POST',
    path: '/api/v1/stitch',
    urlPath: '/api/v1/stitch-by-url',
    description: '图片拼接，将多张图片拼接成一张',
    category: '图片拼接',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'images',
        type: 'file',
        required: true,
        description: '要拼接的图片列表'
      },
      {
        name: 'direction',
        type: 'select',
        required: false,
        description: '拼接方向',
        options: ['horizontal', 'vertical', 'grid'],
        defaultValue: 'horizontal'
      },
      {
        name: 'spacing',
        type: 'number',
        required: false,
        description: '图片间距',
        defaultValue: 0,
        min: 0,
        max: 100
      },
      {
        name: 'background_color',
        type: 'color',
        required: false,
        description: '背景颜色',
        defaultValue: '#FFFFFF'
      }
    ]
  },
  // 格式转换
  {
    method: 'POST',
    path: '/api/v1/format',
    urlPath: '/api/v1/format-by-url',
    description: '图片格式转换，支持多种常见图片格式',
    category: '格式转换',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/*',
    parameters: [
      {
        name: 'output_format',
        type: 'select',
        required: true,
        description: '输出格式',
        options: ['jpeg', 'png', 'webp', 'bmp', 'tiff']
      },
      {
        name: 'quality',
        type: 'number',
        required: false,
        description: '图片质量（JPEG/WebP）',
        defaultValue: 90,
        min: 1,
        max: 100
      }
    ]
  },
  // 图片叠加
  {
    method: 'POST',
    path: '/api/v1/overlay',
    urlPath: '/api/v1/overlay-by-url',
    description: '图片叠加，在基础图片上叠加另一张图片',
    category: '图片叠加',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'overlay_image',
        type: 'file',
        required: true,
        description: '叠加图片'
      },
      {
        name: 'position',
        type: 'select',
        required: false,
        description: '叠加位置',
        options: ['center', 'top-left', 'top-right', 'bottom-left', 'bottom-right'],
        defaultValue: 'center'
      },
      {
        name: 'scale',
        type: 'number',
        required: false,
        description: '叠加图片缩放比例',
        defaultValue: 1.0,
        min: 0.1,
        max: 2.0
      }
    ]
  },
  // 蒙版处理
  {
    method: 'POST',
    path: '/api/v1/mask',
    urlPath: '/api/v1/mask-by-url',
    description: '蒙版处理，使用蒙版对图片进行选择性处理',
    category: '蒙版处理',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'mask_type',
        type: 'select',
        required: true,
        description: '蒙版类型',
        options: ['circle', 'rectangle', 'ellipse', 'custom']
      },
      {
        name: 'feather',
        type: 'number',
        required: false,
        description: '羽化程度',
        defaultValue: 0,
        min: 0,
        max: 100
      },
      {
        name: 'invert',
        type: 'boolean',
        required: false,
        description: '反转蒙版',
        defaultValue: false
      }
    ]
  },
  // GIF处理
  {
    method: 'POST',
    path: '/api/v1/gif',
    urlPath: '/api/v1/gif-by-url',
    description: 'GIF动图处理，包括帧提取、速度调整等',
    category: 'GIF处理',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/gif',
    parameters: [
      {
        name: 'operation',
        type: 'select',
        required: true,
        description: '操作类型',
        options: ['extract_frames', 'adjust_speed', 'resize', 'optimize']
      },
      {
        name: 'speed_factor',
        type: 'number',
        required: false,
        description: '速度倍数（调整速度时使用）',
        defaultValue: 1.0,
        min: 0.1,
        max: 5.0
      },
      {
        name: 'frame_skip',
        type: 'number',
        required: false,
        description: '跳帧数量（优化时使用）',
        defaultValue: 0,
        min: 0,
        max: 10
      }
    ]
  }
];
