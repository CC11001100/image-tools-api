import { EffectExample } from '../../../types/api';

// 艺术文字效果示例 (11种)
export const artisticTextExamples: EffectExample[] = [
  {
    title: '艺术字体',
    description: '艺术风格的字体效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-11.jpg',
    parameters: [
      { label: '文字内容', value: 'Artistic' },
      { label: '字体', value: 'Brush Script' },
      { label: '字体大小', value: '54px' },
      { label: '颜色', value: '#FF1493' }
    ],
    apiParams: {
      endpoint: '/text/artistic',
      text: 'Artistic',
      font_family: 'Brush Script',
      font_size: 54,
      font_color: '#FF1493',
      artistic_style: 'brush',
      quality: 90
    }
  },
  {
    title: '透明效果',
    description: '半透明文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-12.jpg',
    parameters: [
      { label: '文字内容', value: 'Transparent' },
      { label: '字体大小', value: '48px' },
      { label: '透明度', value: '60%' },
      { label: '颜色', value: '#FFFFFF' }
    ],
    apiParams: {
      endpoint: '/text/transparent',
      text: 'Transparent',
      font_family: 'Arial',
      font_size: 48,
      font_color: '#FFFFFF',
      opacity: 0.6,
      quality: 90
    }
  },
  {
    title: '3D立体效果',
    description: '立体三维文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-13.jpg',
    parameters: [
      { label: '文字内容', value: '3D TEXT' },
      { label: '字体大小', value: '56px' },
      { label: '立体深度', value: '8px' },
      { label: '光照角度', value: '45°' }
    ],
    apiParams: {
      endpoint: '/text/3d',
      text: '3D TEXT',
      font_family: 'Arial',
      font_size: 56,
      font_color: '#4169E1',
      depth: 8,
      light_angle: 45,
      quality: 90
    }
  },
  {
    title: '霓虹发光',
    description: '霓虹灯发光效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-14.jpg',
    parameters: [
      { label: '文字内容', value: 'NEON' },
      { label: '字体大小', value: '52px' },
      { label: '发光强度', value: '80%' },
      { label: '发光颜色', value: '#00FFFF' }
    ],
    apiParams: {
      endpoint: '/text/neon',
      text: 'NEON',
      font_family: 'Arial',
      font_size: 52,
      font_color: '#00FFFF',
      glow_intensity: 0.8,
      glow_color: '#00FFFF',
      quality: 90
    }
  },
  {
    title: '金属质感',
    description: '金属材质文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-15.jpg',
    parameters: [
      { label: '文字内容', value: 'METAL' },
      { label: '字体大小', value: '50px' },
      { label: '金属类型', value: '银色' },
      { label: '反光强度', value: '70%' }
    ],
    apiParams: {
      endpoint: '/text/metal',
      text: 'METAL',
      font_family: 'Arial',
      font_size: 50,
      metal_type: 'silver',
      reflection: 0.7,
      quality: 90
    }
  },
  {
    title: '彩虹渐变',
    description: '彩虹渐变色文字',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-16.jpg',
    parameters: [
      { label: '文字内容', value: 'RAINBOW' },
      { label: '字体大小', value: '48px' },
      { label: '渐变方向', value: '水平' },
      { label: '色彩饱和度', value: '90%' }
    ],
    apiParams: {
      endpoint: '/text/rainbow',
      text: 'RAINBOW',
      font_family: 'Arial',
      font_size: 48,
      gradient_direction: 'horizontal',
      saturation: 0.9,
      quality: 90
    }
  },
  {
    title: '火焰效果',
    description: '燃烧火焰文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-17.jpg',
    parameters: [
      { label: '文字内容', value: 'FIRE' },
      { label: '字体大小', value: '54px' },
      { label: '火焰强度', value: '85%' },
      { label: '火焰颜色', value: '#FF4500' }
    ],
    apiParams: {
      endpoint: '/text/fire',
      text: 'FIRE',
      font_family: 'Arial',
      font_size: 54,
      fire_intensity: 0.85,
      fire_color: '#FF4500',
      quality: 90
    }
  },
  {
    title: '冰雪水晶',
    description: '冰雪水晶文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-18.jpg',
    parameters: [
      { label: '文字内容', value: 'ICE' },
      { label: '字体大小', value: '50px' },
      { label: '冰晶密度', value: '75%' },
      { label: '透明度', value: '80%' }
    ],
    apiParams: {
      endpoint: '/text/ice',
      text: 'ICE',
      font_family: 'Arial',
      font_size: 50,
      ice_density: 0.75,
      transparency: 0.8,
      quality: 90
    }
  },
  {
    title: '多重阴影',
    description: '多层阴影文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-19.jpg',
    parameters: [
      { label: '文字内容', value: 'SHADOW' },
      { label: '字体大小', value: '46px' },
      { label: '阴影层数', value: '3' },
      { label: '阴影距离', value: '5px' }
    ],
    apiParams: {
      endpoint: '/text/multi_shadow',
      text: 'SHADOW',
      font_family: 'Arial',
      font_size: 46,
      shadow_layers: 3,
      shadow_distance: 5,
      quality: 90
    }
  },
  {
    title: '浮雕效果',
    description: '浮雕立体文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-20.jpg',
    parameters: [
      { label: '文字内容', value: 'EMBOSS' },
      { label: '字体大小', value: '52px' },
      { label: '浮雕深度', value: '6px' },
      { label: '光照方向', value: '左上' }
    ],
    apiParams: {
      endpoint: '/text/emboss',
      text: 'EMBOSS',
      font_family: 'Arial',
      font_size: 52,
      emboss_depth: 6,
      light_direction: 'top_left',
      quality: 90
    }
  },
  {
    title: '透视变形',
    description: '透视变形文字效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-21.jpg',
    parameters: [
      { label: '文字内容', value: 'PERSPECTIVE' },
      { label: '字体大小', value: '44px' },
      { label: '透视角度', value: '30°' },
      { label: '变形强度', value: '60%' }
    ],
    apiParams: {
      endpoint: '/text/perspective',
      text: 'PERSPECTIVE',
      font_family: 'Arial',
      font_size: 44,
      perspective_angle: 30,
      distortion: 0.6,
      quality: 90
    }
  }
];
