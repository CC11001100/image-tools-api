import { EffectExample } from '../../types/api';

export const annotationExamples: EffectExample[] = [
  {
    title: '矩形标注',
    description: '添加矩形框标注，突出重点区域',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/annotation/original-rectangle.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/annotation/annotation-rectangle.jpg',
    parameters: [
      { label: '标注类型', value: '矩形' },
      { label: '颜色', value: '红色' },
      { label: '位置', value: '中心区域' }
    ],
    apiParams: {
      endpoint: '/api/v1/annotation',
      annotation_type: 'rectangle',
      color: '#FF0000',
      position: '200,300,600,700',
      quality: 90
    }
  },
  {
    title: '圆形标注',
    description: '添加圆形标注，标记重要位置',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/annotation/original-circle.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/annotation/annotation-circle.jpg',
    parameters: [
      { label: '标注类型', value: '圆形' },
      { label: '颜色', value: '绿色' },
      { label: '位置', value: '中心位置' }
    ],
    apiParams: {
      endpoint: '/api/v1/annotation',
      annotation_type: 'circle',
      color: '#00FF00',
      position: '400,600,200',
      quality: 90
    }
  },
  {
    title: '箭头标注',
    description: '添加箭头指向，引导视线',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/annotation/original-arrow.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/annotation/annotation-arrow.jpg',
    parameters: [
      { label: '标注类型', value: '箭头' },
      { label: '颜色', value: '蓝色' },
      { label: '方向', value: '指向目标' }
    ],
    apiParams: {
      endpoint: '/api/v1/annotation',
      annotation_type: 'arrow',
      color: '#0000FF',
      position: '300,400,500,600',
      quality: 90
    }
  },
  {
    title: '文字标注',
    description: '添加文字说明，支持自定义样式',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/annotation/original-text.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/annotation/annotation-text.jpg',
    parameters: [
      { label: '标注类型', value: '文字' },
      { label: '内容', value: '重要标注' },
      { label: '颜色', value: '白色' },
      { label: '字体大小', value: '24px' }
    ],
    apiParams: {
      endpoint: '/api/v1/annotation',
      annotation_type: 'text',
      text: '重要标注',
      color: '#FFFFFF',
      position: '400,500',
      quality: 90
    }
  }
];
