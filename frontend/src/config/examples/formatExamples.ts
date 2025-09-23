import { EffectExample } from '../../types/api';

export const formatExamples: EffectExample[] = [
  {
    title: 'JPEG格式转换',
    description: '将图片转换为JPEG格式，适合照片存储',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-jpeg.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-jpeg.jpg',
    parameters: [
      { label: '目标格式', value: 'JPEG' },
      { label: '质量', value: '90%' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      output_format: 'jpeg',
      quality: 90
    }
  },
  {
    title: 'PNG格式转换',
    description: '将图片转换为PNG格式，保持透明度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-png.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-png.png',
    parameters: [
      { label: '目标格式', value: 'PNG' },
      { label: '质量', value: '90%' },
      { label: '透明度', value: '保持' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      output_format: 'png',
      quality: 90
    }
  },
  {
    title: 'WebP格式转换',
    description: '将图片转换为WebP格式，更小文件体积',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-webp.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-webp.webp',
    parameters: [
      { label: '目标格式', value: 'WebP' },
      { label: '质量', value: '85%' },
      { label: '压缩', value: '优化' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      output_format: 'webp',
      quality: 85
    }
  },
  {
    title: '高质量JPEG',
    description: '转换为高质量JPEG格式',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-jpeg_hq.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-jpeg_hq.jpg',
    parameters: [
      { label: '目标格式', value: 'JPEG' },
      { label: '质量', value: '95%' },
      { label: '模式', value: '高质量' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      output_format: 'jpeg',
      quality: 95
    }
  },
  {
    title: '压缩JPEG',
    description: '转换为压缩JPEG格式，减小文件大小',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-jpeg_compressed.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-jpeg_compressed.jpg',
    parameters: [
      { label: '目标格式', value: 'JPEG' },
      { label: '质量', value: '70%' },
      { label: '模式', value: '压缩' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      output_format: 'jpeg',
      quality: 70
    }
  },
  {
    title: 'PNG格式转换',
    description: '将图片转换为PNG格式，支持透明度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-png.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-png.png',
    parameters: [
      { label: '目标格式', value: 'PNG' },
      { label: '质量', value: '100%' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      format: 'png',
      quality: 100,
      optimize: true
    }
  },
  {
    title: 'WebP格式转换',
    description: '将图片转换为WebP格式，现代高效格式',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-webp.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-webp.webp',
    parameters: [
      { label: '目标格式', value: 'WebP' },
      { label: '质量', value: '85%' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      format: 'webp',
      quality: 85,
      optimize: true
    }
  }
];
