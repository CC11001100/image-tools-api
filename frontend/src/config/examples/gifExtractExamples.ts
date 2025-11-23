import { EffectExample } from '../../types/api';

export const gifExtractExamples: EffectExample[] = [
  {
    title: '全帧提取',
    description: '提取GIF中的所有帧，适合完整分析动画内容',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-center-crop.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-center-crop.jpg',
    parameters: [
      { label: '输出格式', value: 'JPEG' },
      { label: '输出质量', value: '90%' },
      { label: '提取范围', value: '全部帧' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract-frames',
      output_format: 'jpeg',
      quality: 90,
      extract_all: true,
    }
  },
  {
    title: '高质量PNG',
    description: '使用PNG格式提取，保持透明度和最高质量',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-square-crop.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-square-crop.jpg',
    parameters: [
      { label: '输出格式', value: 'PNG' },
      { label: '透明支持', value: '是' },
      { label: '提取范围', value: '全部帧' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract-frames',
      output_format: 'png',
      extract_all: true,
    }
  },
  {
    title: '关键帧提取',
    description: '每隔3帧提取一次，快速获取动画关键帧',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-rectangle-crop.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-rectangle-crop.jpg',
    parameters: [
      { label: '输出格式', value: 'JPEG' },
      { label: '输出质量', value: '85%' },
      { label: '跳帧间隔', value: '3帧' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract-frames',
      output_format: 'jpeg',
      quality: 85,
      extract_all: false,
      skip_frames: 3,
    }
  },
  {
    title: '范围提取',
    description: '提取指定范围的帧，适合分析特定片段',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-original-ratio-16-9.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/crop/crop-ratio-16-9.jpg',
    parameters: [
      { label: '输出格式', value: 'JPEG' },
      { label: '输出质量', value: '90%' },
      { label: '帧范围', value: '5-15帧' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract-frames',
      output_format: 'jpeg',
      quality: 90,
      extract_all: false,
      start_frame: 5,
      end_frame: 15,
    }
  },
  {
    title: '压缩提取',
    description: '使用较低质量设置，适合快速预览或节省空间',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-original-blur.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-blur.jpg',
    parameters: [
      { label: '输出格式', value: 'JPEG' },
      { label: '输出质量', value: '60%' },
      { label: '跳帧间隔', value: '2帧' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract-frames',
      output_format: 'jpeg',
      quality: 60,
      extract_all: false,
      skip_frames: 2,
    }
  },
  {
    title: '精选帧提取',
    description: '提取动画中间部分的精选帧，平衡质量和数量',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-original-sharpen.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/filter/filter-sharpen.jpg',
    parameters: [
      { label: '输出格式', value: 'JPEG' },
      { label: '输出质量', value: '85%' },
      { label: '帧范围', value: '10-30帧' },
      { label: '跳帧间隔', value: '2帧' },
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract-frames',
      output_format: 'jpeg',
      quality: 85,
      extract_all: false,
      start_frame: 10,
      end_frame: 30,
      skip_frames: 2,
    }
  }
]; 