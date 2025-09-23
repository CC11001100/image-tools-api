import { EffectExample } from '../../types/api';

export const extractGifExamples: EffectExample[] = [
  {
    title: '提取所有帧',
    description: '提取GIF中的所有帧图片',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/extract-gif/original-all-frames.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/extract-gif/extracted-all-frames.jpg',
    parameters: [
      { label: '提取类型', value: '所有帧' },
      { label: '输出格式', value: 'JPEG' },
      { label: '质量', value: '95%' }
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract',
      extract_type: 'all',
      output_format: 'jpeg',
      quality: 95
    }
  },
  {
    title: '提取关键帧',
    description: '提取GIF中的关键帧',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/extract-gif/original-key-frames.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/extract-gif/extracted-key-frames.jpg',
    parameters: [
      { label: '提取类型', value: '关键帧' },
      { label: '输出格式', value: 'JPEG' },
      { label: '质量', value: '95%' }
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract',
      extract_type: 'key',
      output_format: 'jpeg',
      quality: 95
    }
  },
  {
    title: '按时间提取',
    description: '按指定时间间隔提取帧',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/extract-gif/original-time-frames.gif',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/extract-gif/extracted-time-frames.jpg',
    parameters: [
      { label: '提取类型', value: '时间间隔' },
      { label: '间隔时间', value: '1秒' },
      { label: '输出格式', value: 'JPEG' }
    ],
    apiParams: {
      endpoint: '/api/v1/gif/extract',
      extract_type: 'time',
      time_interval: 1.0,
      output_format: 'jpeg',
      quality: 95
    }
  }
];
