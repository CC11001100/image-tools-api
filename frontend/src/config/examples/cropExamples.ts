import { EffectExample } from '../../types/api';

// Crop 效果示例 - 6个高质量示例
export const cropExamples: EffectExample[] = [
  {
    title: '中心裁剪 - 800x800',
    description: '从图片中心裁剪出正方形区域，保持主要内容居中',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-center-crop.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-center-crop.jpg',
    parameters: [
      { label: '裁剪类型', value: '中心裁剪' },
      { label: '尺寸', value: '800x800' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 800, height: 800 }
    },
    apiParams: {
      endpoint: '/api/v1/crop',
      crop_type: 'center',
      width: 800,
      height: 800,
      quality: 90
    }
  },
  {
    title: '正方形裁剪 - 600x600',
    description: '裁剪为正方形比例，适合头像制作和社交媒体',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-square-crop.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-square-crop.jpg',
    parameters: [
      { label: '裁剪类型', value: '正方形' },
      { label: '尺寸', value: '600x600' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 600, height: 600 }
    },
    apiParams: {
      endpoint: '/api/v1/crop',
      crop_type: 'center',
      width: 600,
      height: 600,
      quality: 90
    }
  },
  {
    title: '矩形裁剪 - 800x600',
    description: '自定义矩形区域裁剪，可以精确指定位置和大小',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-rectangle-crop.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-rectangle-crop.jpg',
    parameters: [
      { label: '裁剪类型', value: '矩形' },
      { label: '起始位置', value: 'x:140, y:360' },
      { label: '尺寸', value: '800x600' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 800, height: 600 }
    },
    apiParams: {
      endpoint: '/api/v1/crop',
      crop_type: 'rectangle',
      x: 140,
      y: 360,
      width: 800,
      height: 600,
      quality: 90
    }
  },
  {
    title: '16:9比例裁剪',
    description: '宽屏比例裁剪，适合电影和视频缩略图',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-ratio-16-9.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-ratio-16-9.jpg',
    parameters: [
      { label: '比例', value: '16:9' },
      { label: '尺寸', value: '1080x607' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 1080, height: 607 }
    },
    apiParams: {
      endpoint: '/api/v1/crop',
      crop_type: 'rectangle',
      x: 0,
      y: 420,
      width: 1080,
      height: 607,
      quality: 90
    }
  },
  {
    title: '4:3比例裁剪',
    description: '传统4:3比例裁剪，适合标准显示器和打印',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-ratio-4-3.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-ratio-4-3.jpg',
    parameters: [
      { label: '比例', value: '4:3' },
      { label: '尺寸', value: '900x675' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 900, height: 675 }
    },
    apiParams: {
      endpoint: '/api/v1/crop',
      crop_type: 'rectangle',
      x: 90,
      y: 360,
      width: 900,
      height: 675,
      quality: 90
    }
  },
  {
    title: '智能居中裁剪 - 700x700',
    description: '智能居中裁剪，自动保持图片主要内容在中心位置',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-smart-center.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-smart-center.jpg',
    parameters: [
      { label: '裁剪类型', value: '智能居中' },
      { label: '尺寸', value: '700x700' },
      { label: '质量', value: '90' }
    ],
    imageDimensions: {
      original: { width: 1080, height: 1920 },
      processed: { width: 700, height: 700 }
    },
    apiParams: {
      endpoint: '/api/v1/crop',
      crop_type: 'smart_center',
      width: 700,
      height: 700,
      quality: 90
    }
  }
];
