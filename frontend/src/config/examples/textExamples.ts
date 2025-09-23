import { EffectExample } from '../../types/api';

// Text 效果示例
export const textExamples: EffectExample[] = [
  {
    title: '简单文字',
    description: '在图片上添加简单的文字内容',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/original-simple.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-simple.jpg',
    parameters: [
      { label: '文字内容', value: 'Hello World' },
      { label: '字体大小', value: '48px' },
      { label: '颜色', value: '白色' }
    ],
    apiParams: {
      endpoint: '/api/v1/text',
      text: 'Hello World',
      font_size: 48,
      font_color: '#FFFFFF',
      position: 'center'
    }
  },
  {
    title: '标题文字',
    description: '添加大号标题文字',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/original-title.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-title.jpg',
    parameters: [
      { label: '文字内容', value: '美丽风景' },
      { label: '字体大小', value: '64px' },
      { label: '颜色', value: '金色' }
    ],
    apiParams: {
      endpoint: '/api/v1/text',
      text: '美丽风景',
      font_size: 64,
      font_color: '#FFD700',
      position: 'center'
    }
  },
  {
    title: '水印文字',
    description: '添加半透明水印文字',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/original-watermark.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-watermark.jpg',
    parameters: [
      { label: '文字内容', value: '© 2024 Photo' },
      { label: '字体大小', value: '32px' },
      { label: '位置', value: '右下角' }
    ],
    apiParams: {
      endpoint: '/api/v1/text',
      text: '© 2024 Photo',
      font_size: 32,
      font_color: '#FFFFFF',
      position: 'bottom-right'
    }
  },
  {
    title: '装饰文字',
    description: '添加装饰性文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/original-decorative.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-decorative.jpg',
    parameters: [
      { label: '文字内容', value: 'Nature' },
      { label: '字体大小', value: '56px' },
      { label: '颜色', value: '绿色' }
    ],
    apiParams: {
      endpoint: '/api/v1/text',
      text: 'Nature',
      font_size: 56,
      font_color: '#00FF00',
      position: 'center'
    }
  },
  {
    title: '阴影文字',
    description: '带有阴影效果的文字，增强可读性',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/original-shadow.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-shadow.jpg',
    parameters: [
      { label: '文字内容', value: 'Shadow Text' },
      { label: '字体大小', value: '52px' },
      { label: '阴影', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/text',
      text: 'Shadow Text',
      font_size: 52,
      color: '#FFFFFF',
      shadow: true,
      position: 'center'
    }
  },
  {
    title: '描边文字',
    description: '带有描边效果的文字，突出显示',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/original-stroke.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-stroke.jpg',
    parameters: [
      { label: '文字内容', value: 'Stroke Text' },
      { label: '字体大小', value: '50px' },
      { label: '描边', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/text',
      text: 'Stroke Text',
      font_size: 50,
      color: '#FFFFFF',
      stroke: true,
      stroke_color: '#000000',
      position: 'center'
    }
  }
];
