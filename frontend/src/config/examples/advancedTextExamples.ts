import { EffectExample } from '../../types/api';

export const advancedTextExamples: EffectExample[] = [
  {
    title: '3D 深度文字',
    description: '创建具有深度感的3D文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/advanced-text/text-3d-depth.png',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/advanced-text/text-3d-depth.png',
    parameters: [
      { label: '文字内容', value: 'DEPTH' },
      { label: '字体', value: 'Impact' },
      { label: '深度', value: '20px' },
      { label: '颜色', value: '#FF5733' }
    ],
    apiParams: {
      endpoint: '/api/advanced-text',
      text: 'DEPTH',
      font: 'Impact',
      depth: 20,
      color: '#FF5733'
    }
  },
  {
    title: '极光文字',
    description: '创建具有极光效果的梦幻文字',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/advanced-text/text-aurora.png',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/advanced-text/text-aurora.png',
    parameters: [
      { label: '文字内容', value: 'AURORA' },
      { label: '字体', value: 'Arial' },
      { label: '发光强度', value: '15' },
      { label: '颜色', value: '#4CAF50' }
    ],
    apiParams: {
      endpoint: '/api/advanced-text',
      text: 'AURORA',
      font: 'Arial',
      glowIntensity: 15,
      color: '#4CAF50'
    }
  },
  {
    title: '金属质感文字',
    description: '创建具有金属光泽的立体文字',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/advanced-text/text-metallic.png',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/advanced-text/text-metallic.png',
    parameters: [
      { label: '文字内容', value: 'METAL' },
      { label: '字体', value: 'Helvetica' },
      { label: '光泽度', value: '80%' },
      { label: '颜色', value: '#C0C0C0' }
    ],
    apiParams: {
      endpoint: '/api/advanced-text',
      text: 'METAL',
      font: 'Helvetica',
      shininess: 80,
      color: '#C0C0C0'
    }
  }
]; 