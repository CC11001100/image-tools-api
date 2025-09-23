import { CompositionExample } from '../../../components/CompositionShowcase';

// 场景应用混合示例 (8种)
export const sceneBlendExamples: CompositionExample[] = [
  {
    title: '人像美化',
    description: '专为人像摄影优化的混合美化效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/portrait-enhancement-blend.jpg',
    parameters: [
      { label: '模式', value: 'portrait-enhancement' },
      { label: '透明度', value: '45%' },
      { label: '美化程度', value: '中' }
    ],
    apiParams: {
      blend_mode: 'portrait-enhancement',
      opacity: 0.45,
      enhancement_level: 0.6,
      quality: 90
    }
  },
  {
    title: '风景调色',
    description: '风景摄影的色彩调整混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/landscape-color-blend.jpg',
    parameters: [
      { label: '模式', value: 'landscape-color' },
      { label: '透明度', value: '60%' },
      { label: '色彩强度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'landscape-color',
      opacity: 0.6,
      color_intensity: 0.8,
      quality: 90
    }
  },
  {
    title: '建筑色调',
    description: '建筑摄影的专业色调混合',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/architecture-tone-blend.jpg',
    parameters: [
      { label: '模式', value: 'architecture-tone' },
      { label: '透明度', value: '55%' },
      { label: '结构强化', value: '中' }
    ],
    apiParams: {
      blend_mode: 'architecture-tone',
      opacity: 0.55,
      structure_enhancement: 0.7,
      quality: 90
    }
  },
  {
    title: '自然氛围',
    description: '增强自然场景氛围的混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/natural-atmosphere-blend.jpg',
    parameters: [
      { label: '模式', value: 'natural-atmosphere' },
      { label: '透明度', value: '40%' },
      { label: '氛围强度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'natural-atmosphere',
      opacity: 0.4,
      atmosphere_intensity: 0.8,
      quality: 90
    }
  },
  {
    title: '电影感',
    description: '电影级别的色彩分级混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/cinematic-blend.jpg',
    parameters: [
      { label: '模式', value: 'cinematic' },
      { label: '透明度', value: '70%' },
      { label: '电影感', value: '强' }
    ],
    apiParams: {
      blend_mode: 'cinematic',
      opacity: 0.7,
      cinematic_intensity: 0.9,
      quality: 90
    }
  },
  {
    title: '商业级混合',
    description: '商业摄影级别的专业混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/commercial-grade-blend.jpg',
    parameters: [
      { label: '模式', value: 'commercial-grade' },
      { label: '透明度', value: '65%' },
      { label: '专业程度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'commercial-grade',
      opacity: 0.65,
      professional_level: 0.9,
      quality: 90
    }
  },
  {
    title: '戏剧对比',
    description: '戏剧性对比的强烈混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/dramatic-contrast-blend.jpg',
    parameters: [
      { label: '模式', value: 'dramatic-contrast' },
      { label: '透明度', value: '80%' },
      { label: '戏剧强度', value: '强' }
    ],
    apiParams: {
      blend_mode: 'dramatic-contrast',
      opacity: 0.8,
      dramatic_intensity: 0.9,
      quality: 90
    }
  },
  {
    title: '柔和发光',
    description: '柔和的发光混合效果，温馨自然',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/soft-glow-blend.jpg',
    parameters: [
      { label: '模式', value: 'soft-glow' },
      { label: '透明度', value: '30%' },
      { label: '发光柔度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'soft-glow',
      opacity: 0.3,
      glow_softness: 0.9,
      quality: 90
    }
  }
];
