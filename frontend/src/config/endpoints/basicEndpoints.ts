import { ApiEndpoint } from '../apiEndpoints';

// 基础功能API端点 (3个)
export const basicEndpoints: ApiEndpoint[] = [
  // 水印
  {
    method: 'POST',
    path: '/api/v1/watermark',
    urlPath: '/api/v1/watermark-by-url',
    description: '为图片添加文字水印，支持自定义字体、颜色、大小、位置等属性',
    category: '基础功能',
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
        description: '水印文字内容'
      },
      {
        name: 'font_size',
        type: 'number',
        required: false,
        description: '字体大小',
        defaultValue: 32,
        min: 8,
        max: 200
      },
      {
        name: 'font_color',
        type: 'color',
        required: false,
        description: '字体颜色',
        defaultValue: '#FFFFFF'
      },
      {
        name: 'position',
        type: 'select',
        required: false,
        description: '水印位置',
        defaultValue: 'bottom-right',
        options: ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']
      }
    ]
  },
  // 尺寸调整
  {
    method: 'POST',
    path: '/api/v1/resize',
    urlPath: '/api/v1/resize-by-url',
    description: '调整图片尺寸，支持按像素、百分比或保持比例缩放',
    category: '基础功能',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'width',
        type: 'number',
        required: false,
        description: '目标宽度（像素）',
        min: 1,
        max: 8000
      },
      {
        name: 'height',
        type: 'number',
        required: false,
        description: '目标高度（像素）',
        min: 1,
        max: 8000
      },
      {
        name: 'scale',
        type: 'number',
        required: false,
        description: '缩放比例（0.1-10.0）',
        min: 0.1,
        max: 10.0
      },
      {
        name: 'keep_aspect_ratio',
        type: 'boolean',
        required: false,
        description: '保持宽高比',
        defaultValue: true
      }
    ]
  },
  // 滤镜
  {
    method: 'POST',
    path: '/api/v1/filter',
    urlPath: '/api/v1/filter-by-url',
    description: '应用各种图像滤镜效果，包括模糊、锐化、浮雕等',
    category: '基础功能',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'filter_type',
        type: 'select',
        required: true,
        description: '滤镜类型',
        options: ['blur', 'sharpen', 'emboss', 'edge_enhance', 'smooth', 'contour']
      },
      {
        name: 'intensity',
        type: 'number',
        required: false,
        description: '滤镜强度',
        defaultValue: 1.0,
        min: 0.1,
        max: 3.0
      }
    ]
  }
];
