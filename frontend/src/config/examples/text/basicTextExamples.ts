import { EffectExample } from '../../../types/api';

// 基础文字效果示例 (10种)
export const basicTextExamples: EffectExample[] = [
  {
    title: '基础文字 - 居中',
    description: '在图片中心添加文字，基础样式',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-1.jpg',
    parameters: [
      { label: '文字内容', value: 'Hello World' },
      { label: '字体', value: 'Arial' },
      { label: '大小', value: '48px' },
      { label: '颜色', value: '#FFFFFF' },
      { label: '位置', value: '居中' }
    ],
    apiParams: {
      endpoint: '/text/basic',
      text: 'Hello World',
      font_family: 'Arial',
      font_size: 48,
      font_color: '#FFFFFF',
      position: 'center',
      x_offset: 0,
      y_offset: 0,
      rotation: 0,
      opacity: 100,
      quality: 90
    }
  },
  {
    title: '多行文字',
    description: '支持换行的长文本',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-2.jpg',
    parameters: [
      { label: '文字内容', value: '多行文字\\n第二行文字' },
      { label: '字体大小', value: '36px' },
      { label: '行间距', value: '10px' },
      { label: '位置', value: '居中' }
    ],
    apiParams: {
      endpoint: '/text/multiline',
      text: '多行文字\n第二行文字',
      font_family: 'Arial',
      font_size: 36,
      font_color: '#FFFFFF',
      position: 'center',
      line_spacing: 10,
      opacity: 1.0,
      quality: 90
    }
  },
  {
    title: '阴影效果',
    description: '为文字添加阴影效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-3.jpg',
    parameters: [
      { label: '文字内容', value: 'Shadow Text' },
      { label: '字体大小', value: '52px' },
      { label: '阴影偏移', value: '3px' },
      { label: '阴影颜色', value: '#000000' }
    ],
    apiParams: {
      endpoint: '/text/shadow',
      text: 'Shadow Text',
      font_family: 'Arial',
      font_size: 52,
      font_color: '#FFFFFF',
      shadow_offset_x: 3,
      shadow_offset_y: 3,
      shadow_color: '#000000',
      shadow_blur: 2,
      quality: 90
    }
  },
  {
    title: '描边文字',
    description: '为文字添加描边效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-4.jpg',
    parameters: [
      { label: '文字内容', value: 'Outline Text' },
      { label: '字体大小', value: '48px' },
      { label: '描边宽度', value: '2px' },
      { label: '描边颜色', value: '#000000' }
    ],
    apiParams: {
      endpoint: '/text/outline',
      text: 'Outline Text',
      font_family: 'Arial',
      font_size: 48,
      font_color: '#FFFFFF',
      outline_width: 2,
      outline_color: '#000000',
      quality: 90
    }
  },
  {
    title: '粗体效果',
    description: '粗体文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-5.jpg',
    parameters: [
      { label: '文字内容', value: 'Bold Text' },
      { label: '字体大小', value: '50px' },
      { label: '粗体程度', value: '700' },
      { label: '颜色', value: '#FF0000' }
    ],
    apiParams: {
      endpoint: '/text/bold',
      text: 'Bold Text',
      font_family: 'Arial',
      font_size: 50,
      font_weight: 700,
      font_color: '#FF0000',
      quality: 90
    }
  },
  {
    title: '优雅样式',
    description: '优雅的文字样式',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-6.jpg',
    parameters: [
      { label: '文字内容', value: 'Elegant' },
      { label: '字体', value: 'Times New Roman' },
      { label: '字体大小', value: '44px' },
      { label: '颜色', value: '#8B4513' }
    ],
    apiParams: {
      endpoint: '/text/elegant',
      text: 'Elegant',
      font_family: 'Times New Roman',
      font_size: 44,
      font_color: '#8B4513',
      font_style: 'italic',
      quality: 90
    }
  },
  {
    title: '旋转文字',
    description: '旋转角度的文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-7.jpg',
    parameters: [
      { label: '文字内容', value: 'Rotated' },
      { label: '字体大小', value: '46px' },
      { label: '旋转角度', value: '15°' },
      { label: '颜色', value: '#0066CC' }
    ],
    apiParams: {
      endpoint: '/text/rotate',
      text: 'Rotated',
      font_family: 'Arial',
      font_size: 46,
      font_color: '#0066CC',
      rotation: 15,
      quality: 90
    }
  },
  {
    title: '彩色文字',
    description: '多彩的文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-8.jpg',
    parameters: [
      { label: '文字内容', value: 'Colorful' },
      { label: '字体大小', value: '48px' },
      { label: '颜色模式', value: '彩虹' },
      { label: '饱和度', value: '100%' }
    ],
    apiParams: {
      endpoint: '/text/colorful',
      text: 'Colorful',
      font_family: 'Arial',
      font_size: 48,
      color_mode: 'rainbow',
      saturation: 100,
      quality: 90
    }
  },
  {
    title: '斜体效果',
    description: '斜体文字样式',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-9.jpg',
    parameters: [
      { label: '文字内容', value: 'Italic Style' },
      { label: '字体大小', value: '42px' },
      { label: '倾斜角度', value: '15°' },
      { label: '颜色', value: '#9932CC' }
    ],
    apiParams: {
      endpoint: '/text/italic',
      text: 'Italic Style',
      font_family: 'Arial',
      font_size: 42,
      font_style: 'italic',
      font_color: '#9932CC',
      quality: 90
    }
  },
  {
    title: '大号文字',
    description: '超大字体效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-10.jpg',
    parameters: [
      { label: '文字内容', value: 'BIG' },
      { label: '字体大小', value: '72px' },
      { label: '字重', value: '900' },
      { label: '颜色', value: '#FF6600' }
    ],
    apiParams: {
      endpoint: '/text/large',
      text: 'BIG',
      font_family: 'Arial',
      font_size: 72,
      font_weight: 900,
      font_color: '#FF6600',
      quality: 90
    }
  }
];
