import { EffectExample } from '../../../types/api';

// 特效文字示例 (11种)
export const effectTextExamples: EffectExample[] = [
  {
    title: '科技未来',
    description: '科技感未来风格文字',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-22.jpg',
    parameters: [
      { label: '文字内容', value: 'FUTURE' },
      { label: '字体大小', value: '50px' },
      { label: '科技风格', value: '电路' },
      { label: '发光效果', value: '蓝色' }
    ],
    apiParams: {
      endpoint: '/text/futuristic',
      text: 'FUTURE',
      font_family: 'Arial',
      font_size: 50,
      tech_style: 'circuit',
      glow_color: '#00BFFF',
      quality: 90
    }
  },
  {
    title: '复古霓虹',
    description: '80年代复古霓虹风格',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-23.jpg',
    parameters: [
      { label: '文字内容', value: 'RETRO' },
      { label: '字体大小', value: '48px' },
      { label: '霓虹颜色', value: '#FF1493' },
      { label: '复古程度', value: '80%' }
    ],
    apiParams: {
      endpoint: '/text/retro_neon',
      text: 'RETRO',
      font_family: 'Arial',
      font_size: 48,
      neon_color: '#FF1493',
      retro_intensity: 0.8,
      quality: 90
    }
  },
  {
    title: '奢华金箔',
    description: '奢华金箔文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-24.jpg',
    parameters: [
      { label: '文字内容', value: 'LUXURY' },
      { label: '字体大小', value: '52px' },
      { label: '金箔类型', value: '24K金' },
      { label: '光泽度', value: '90%' }
    ],
    apiParams: {
      endpoint: '/text/gold_foil',
      text: 'LUXURY',
      font_family: 'Arial',
      font_size: 52,
      foil_type: '24k_gold',
      shine: 0.9,
      quality: 90
    }
  },
  {
    title: '双色渐变',
    description: '双色渐变文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-25.jpg',
    parameters: [
      { label: '文字内容', value: 'GRADIENT' },
      { label: '字体大小', value: '46px' },
      { label: '起始颜色', value: '#FF6B6B' },
      { label: '结束颜色', value: '#4ECDC4' }
    ],
    apiParams: {
      endpoint: '/text/dual_gradient',
      text: 'GRADIENT',
      font_family: 'Arial',
      font_size: 46,
      start_color: '#FF6B6B',
      end_color: '#4ECDC4',
      quality: 90
    }
  },
  {
    title: '电路板风',
    description: '电路板科技风格文字',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-26.jpg',
    parameters: [
      { label: '文字内容', value: 'CIRCUIT' },
      { label: '字体大小', value: '48px' },
      { label: '电路密度', value: '70%' },
      { label: '发光强度', value: '60%' }
    ],
    apiParams: {
      endpoint: '/text/circuit',
      text: 'CIRCUIT',
      font_family: 'Arial',
      font_size: 48,
      circuit_density: 0.7,
      glow_intensity: 0.6,
      quality: 90
    }
  },
  {
    title: '水墨书法',
    description: '中国水墨书法风格',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-27.jpg',
    parameters: [
      { label: '文字内容', value: '书法' },
      { label: '字体', value: '楷体' },
      { label: '字体大小', value: '54px' },
      { label: '墨迹浓度', value: '80%' }
    ],
    apiParams: {
      endpoint: '/text/calligraphy',
      text: '书法',
      font_family: 'KaiTi',
      font_size: 54,
      ink_density: 0.8,
      brush_style: 'traditional',
      quality: 90
    }
  },
  {
    title: '炫光效果',
    description: '炫彩光线文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-28.jpg',
    parameters: [
      { label: '文字内容', value: 'GLOW' },
      { label: '字体大小', value: '50px' },
      { label: '光线数量', value: '12' },
      { label: '光线颜色', value: '彩虹' }
    ],
    apiParams: {
      endpoint: '/text/light_rays',
      text: 'GLOW',
      font_family: 'Arial',
      font_size: 50,
      ray_count: 12,
      ray_color: 'rainbow',
      quality: 90
    }
  },
  {
    title: '钻石切割',
    description: '钻石切割面文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-29.jpg',
    parameters: [
      { label: '文字内容', value: 'DIAMOND' },
      { label: '字体大小', value: '48px' },
      { label: '切割面数', value: '24' },
      { label: '折射强度', value: '85%' }
    ],
    apiParams: {
      endpoint: '/text/diamond',
      text: 'DIAMOND',
      font_family: 'Arial',
      font_size: 48,
      facet_count: 24,
      refraction: 0.85,
      quality: 90
    }
  },
  {
    title: '极光效果',
    description: '北极光文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-30.jpg',
    parameters: [
      { label: '文字内容', value: 'AURORA' },
      { label: '字体大小', value: '52px' },
      { label: '极光强度', value: '75%' },
      { label: '色彩变化', value: '动态' }
    ],
    apiParams: {
      endpoint: '/text/aurora',
      text: 'AURORA',
      font_family: 'Arial',
      font_size: 52,
      aurora_intensity: 0.75,
      color_animation: 'dynamic',
      quality: 90
    }
  },
  {
    title: '岩浆熔岩',
    description: '岩浆熔岩文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-31.jpg',
    parameters: [
      { label: '文字内容', value: 'LAVA' },
      { label: '字体大小', value: '54px' },
      { label: '熔岩温度', value: '高温' },
      { label: '流动效果', value: '80%' }
    ],
    apiParams: {
      endpoint: '/text/lava',
      text: 'LAVA',
      font_family: 'Arial',
      font_size: 54,
      temperature: 'high',
      flow_effect: 0.8,
      quality: 90
    }
  },
  {
    title: '粒子爆炸',
    description: '粒子爆炸文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-32.jpg',
    parameters: [
      { label: '文字内容', value: 'EXPLOSION' },
      { label: '字体大小', value: '46px' },
      { label: '粒子数量', value: '500' },
      { label: '爆炸强度', value: '90%' }
    ],
    apiParams: {
      endpoint: '/text/particle_explosion',
      text: 'EXPLOSION',
      font_family: 'Arial',
      font_size: 46,
      particle_count: 500,
      explosion_intensity: 0.9,
      quality: 90
    }
  }
];
