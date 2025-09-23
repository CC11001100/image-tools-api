import { CompositionExample } from '../../../components/CompositionShowcase';

// 特殊效果混合示例 (8种)
export const specialEffectBlendExamples: CompositionExample[] = [
  {
    title: '双重曝光',
    description: '创造双重曝光的艺术效果，层次丰富',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/double-exposure-blend.jpg',
    parameters: [
      { label: '模式', value: 'double-exposure' },
      { label: '透明度', value: '45%' },
      { label: '混合强度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'double-exposure',
      opacity: 0.45,
      intensity: 0.8,
      quality: 90
    }
  },
  {
    title: '梦幻光影',
    description: '营造梦幻般的光影效果，柔和朦胧',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/dreamy-light-blend.jpg',
    parameters: [
      { label: '模式', value: 'dreamy-light' },
      { label: '透明度', value: '40%' },
      { label: '光晕强度', value: '中' }
    ],
    apiParams: {
      blend_mode: 'dreamy-light',
      opacity: 0.4,
      glow_intensity: 0.6,
      quality: 90
    }
  },
  {
    title: '复古色调',
    description: '复古胶片风格的色调混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/vintage-tone-blend.jpg',
    parameters: [
      { label: '模式', value: 'vintage-tone' },
      { label: '透明度', value: '55%' },
      { label: '复古程度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'vintage-tone',
      opacity: 0.55,
      vintage_intensity: 0.8,
      quality: 90
    }
  },
  {
    title: '高对比度',
    description: '增强对比度的混合效果，视觉冲击强',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/high-contrast-blend.jpg',
    parameters: [
      { label: '模式', value: 'high-contrast' },
      { label: '透明度', value: '75%' },
      { label: '对比强度', value: '强' }
    ],
    apiParams: {
      blend_mode: 'high-contrast',
      opacity: 0.75,
      contrast_boost: 0.9,
      quality: 90
    }
  },
  {
    title: '阴影合成',
    description: '专注于阴影部分的混合合成效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/shadow-composite-blend.jpg',
    parameters: [
      { label: '模式', value: 'shadow-composite' },
      { label: '透明度', value: '65%' },
      { label: '阴影深度', value: '中' }
    ],
    apiParams: {
      blend_mode: 'shadow-composite',
      opacity: 0.65,
      shadow_depth: 0.6,
      quality: 90
    }
  },
  {
    title: '高光合成',
    description: '专注于高光部分的混合合成效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/highlight-composite-blend.jpg',
    parameters: [
      { label: '模式', value: 'highlight-composite' },
      { label: '透明度', value: '50%' },
      { label: '高光强度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'highlight-composite',
      opacity: 0.5,
      highlight_intensity: 0.8,
      quality: 90
    }
  },
  {
    title: '焦点突出',
    description: '突出焦点区域的混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/focus-highlight-blend.jpg',
    parameters: [
      { label: '模式', value: 'focus-highlight' },
      { label: '透明度', value: '60%' },
      { label: '焦点强度', value: '中' }
    ],
    apiParams: {
      blend_mode: 'focus-highlight',
      opacity: 0.6,
      focus_intensity: 0.7,
      quality: 90
    }
  },
  {
    title: '纹理叠加',
    description: '纹理图案的叠加混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/texture-overlay-blend.jpg',
    parameters: [
      { label: '模式', value: 'texture-overlay' },
      { label: '透明度', value: '35%' },
      { label: '纹理强度', value: '中' }
    ],
    apiParams: {
      blend_mode: 'texture-overlay',
      opacity: 0.35,
      texture_intensity: 0.6,
      quality: 90
    }
  }
];
