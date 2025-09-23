import { EffectExample } from '../../types/api';

// Resize 效果示例 - 使用新的原图和效果图
export const resizeExamples: EffectExample[] = [
  {
    title: '等比缩放 - 800px',
    description: '将图片宽度调整为800像素，保持原始比例',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-original-resize-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-800px.jpg',
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 800, height: 1422 }
    },
    parameters: [
      { label: '宽度', value: '800px' },
      { label: '保持比例', value: '是' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/resize',
      width: 800,
      maintain_aspect: true,
      quality: 90
    }
  },
  {
    title: '等比缩放 - 600px',
    description: '将图片宽度调整为600像素，保持原始比例',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-original-resize-600px.jpg',
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-600px.jpg",
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 600, height: 1066 }
    },
    parameters: [
      { label: '宽度', value: '600px' },
      { label: '保持比例', value: '是' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/resize',
      width: 600,
      maintain_aspect: true,
      quality: 90
    }
  },
  {
    title: '等比缩放 - 400px',
    description: '将图片宽度调整为400像素，保持原始比例，适用于缩略图、头像或移动端显示',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-original-resize-400px.jpg',
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-400px.jpg",
    parameters: [
      { label: '宽度', value: '400px' },
      { label: '保持比例', value: '是' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 400, height: 711 }
    },
    apiParams: {
      endpoint: '/api/v1/resize',
      width: 400,
      maintain_aspect: true,
      quality: 90
    }
  },
  {
    title: '固定尺寸 - 400x300',
    description: '将图片调整为固定尺寸400x300像素，不保持宽高比，可能会导致图片变形',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-original-resize-fixed-400x300.jpg',
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-fixed-400x300.jpg",
    parameters: [
      { label: '宽度', value: '400px' },
      { label: '高度', value: '300px' },
      { label: '保持比例', value: '否' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 400, height: 300 }
    },
    apiParams: {
      endpoint: '/api/v1/resize',
      width: 400,
      height: 300,
      maintain_aspect: false,
      quality: 90
    }
  },
  {
    title: '等比缩放 - 1000px',
    description: '将图片宽度调整为1000像素，保持原始比例，适用于高分辨率显示',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-original-resize-1000px.jpg',
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-1000px.jpg",
    parameters: [
      { label: '宽度', value: '1000px' },
      { label: '保持比例', value: '是' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 1000, height: 1777 }
    },
    apiParams: {
      endpoint: '/api/v1/resize',
      width: 1000,
      maintain_aspect: true,
      quality: 90
    }
  },
  {
    title: '高质量缩放 - 600px',
    description: '使用100%质量的高质量缩放，保持最佳图像细节，适用于专业用途',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-original-resize-hq-600px.jpg',
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/resize-hq-600px.jpg",
    parameters: [
      { label: '宽度', value: '600px' },
      { label: '保持比例', value: '是' },
      { label: '质量', value: '100' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 600, height: 1066 }
    },
    apiParams: {
      endpoint: '/api/v1/resize',
      width: 600,
      maintain_aspect: true,
      quality: 100
    }
  }
];



// 增强效果示例
