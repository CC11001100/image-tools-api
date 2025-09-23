import { ApiEndpoint } from '../apiEndpoints';

// 几何变换API端点 (4个)
export const geometryEndpoints: ApiEndpoint[] = [
  // 矩形裁剪
  {
    method: 'POST',
    path: '/api/v1/crop/rectangle',
    urlPath: '/api/v1/crop/rectangle-by-url',
    description: '矩形裁剪，按指定的矩形区域裁剪图片',
    category: '几何变换',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'x',
        type: 'number',
        required: true,
        description: '裁剪区域左上角X坐标',
        min: 0
      },
      {
        name: 'y',
        type: 'number',
        required: true,
        description: '裁剪区域左上角Y坐标',
        min: 0
      },
      {
        name: 'width',
        type: 'number',
        required: true,
        description: '裁剪区域宽度',
        min: 1
      },
      {
        name: 'height',
        type: 'number',
        required: true,
        description: '裁剪区域高度',
        min: 1
      }
    ]
  },
  // 圆形裁剪
  {
    method: 'POST',
    path: '/api/v1/crop/circle',
    urlPath: '/api/v1/crop/circle-by-url',
    description: '圆形裁剪，按指定的圆形区域裁剪图片',
    category: '几何变换',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'center_x',
        type: 'number',
        required: true,
        description: '圆心X坐标',
        min: 0
      },
      {
        name: 'center_y',
        type: 'number',
        required: true,
        description: '圆心Y坐标',
        min: 0
      },
      {
        name: 'radius',
        type: 'number',
        required: true,
        description: '圆形半径',
        min: 1
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
  // 智能裁剪
  {
    method: 'POST',
    path: '/api/v1/crop/smart',
    urlPath: '/api/v1/crop/smart-by-url',
    description: '智能裁剪，自动识别主体并进行最佳裁剪',
    category: '几何变换',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'target_ratio',
        type: 'select',
        required: false,
        description: '目标宽高比',
        options: ['1:1', '4:3', '16:9', '3:2', 'auto'],
        defaultValue: 'auto'
      },
      {
        name: 'focus_point',
        type: 'select',
        required: false,
        description: '焦点类型',
        options: ['auto', 'face', 'center', 'object'],
        defaultValue: 'auto'
      }
    ]
  },
  // 画布调整
  {
    method: 'POST',
    path: '/api/v1/canvas',
    urlPath: '/api/v1/canvas-by-url',
    description: '调整画布大小，可以扩展或缩小画布并设置背景',
    category: '画布调整',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/jpeg',
    parameters: [
      {
        name: 'canvas_width',
        type: 'number',
        required: true,
        description: '画布宽度',
        min: 1,
        max: 8000
      },
      {
        name: 'canvas_height',
        type: 'number',
        required: true,
        description: '画布高度',
        min: 1,
        max: 8000
      },
      {
        name: 'position',
        type: 'select',
        required: false,
        description: '图片在画布中的位置',
        options: ['center', 'top-left', 'top-center', 'top-right', 'center-left', 'center-right', 'bottom-left', 'bottom-center', 'bottom-right'],
        defaultValue: 'center'
      },
      {
        name: 'background_color',
        type: 'color',
        required: false,
        description: '背景颜色',
        defaultValue: '#FFFFFF'
      }
    ]
  }
];
