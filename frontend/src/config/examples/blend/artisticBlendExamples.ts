import { CompositionExample } from '../../../components/CompositionShowcase';

// 艺术风格混合示例 (8种)
export const artisticBlendExamples: CompositionExample[] = [
  {
    title: '水彩效果',
    description: '模拟水彩画的柔和混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/watercolor-blend.jpg',
    parameters: [
      { label: '模式', value: 'watercolor' },
      { label: '透明度', value: '45%' },
      { label: '水彩强度', value: '中' }
    ],
    apiParams: {
      blend_mode: 'watercolor',
      opacity: 0.45,
      watercolor_intensity: 0.6,
      quality: 90
    }
  },
  {
    title: '油画质感',
    description: '创造油画般的厚重质感效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/oil-painting-blend.jpg',
    parameters: [
      { label: '模式', value: 'oil-painting' },
      { label: '透明度', value: '60%' },
      { label: '笔触强度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'oil-painting',
      opacity: 0.6,
      brush_intensity: 0.8,
      quality: 90
    }
  },
  {
    title: '印象派光影',
    description: '印象派风格的光影混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/impressionist-blend.jpg',
    parameters: [
      { label: '模式', value: 'impressionist' },
      { label: '透明度', value: '50%' },
      { label: '光影强度', value: '中' }
    ],
    apiParams: {
      blend_mode: 'impressionist',
      opacity: 0.5,
      light_intensity: 0.7,
      quality: 90
    }
  },
  {
    title: '现代艺术',
    description: '现代艺术风格的抽象混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/modern-art-blend.jpg',
    parameters: [
      { label: '模式', value: 'modern-art' },
      { label: '透明度', value: '55%' },
      { label: '抽象程度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'modern-art',
      opacity: 0.55,
      abstraction_level: 0.8,
      quality: 90
    }
  },
  {
    title: '奇幻合成',
    description: '奇幻风格的创意混合合成',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/fantasy-composite-blend.jpg',
    parameters: [
      { label: '模式', value: 'fantasy-composite' },
      { label: '透明度', value: '40%' },
      { label: '奇幻强度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'fantasy-composite',
      opacity: 0.4,
      fantasy_intensity: 0.9,
      quality: 90
    }
  },
  {
    title: '复古胶片',
    description: '复古胶片风格的色彩混合',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/vintage-film-blend.jpg',
    parameters: [
      { label: '模式', value: 'vintage-film' },
      { label: '透明度', value: '65%' },
      { label: '胶片感', value: '强' }
    ],
    apiParams: {
      blend_mode: 'vintage-film',
      opacity: 0.65,
      film_grain: 0.8,
      quality: 90
    }
  },
  {
    title: '空灵发光',
    description: '空灵梦幻的发光混合效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/ethereal-glow-blend.jpg',
    parameters: [
      { label: '模式', value: 'ethereal-glow' },
      { label: '透明度', value: '35%' },
      { label: '发光强度', value: '高' }
    ],
    apiParams: {
      blend_mode: 'ethereal-glow',
      opacity: 0.35,
      glow_intensity: 0.9,
      quality: 90
    }
  },
  {
    title: '艺术融合',
    description: '多种艺术风格的融合混合',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/artistic-fusion-blend.jpg',
    parameters: [
      { label: '模式', value: 'artistic-fusion' },
      { label: '透明度', value: '50%' },
      { label: '融合程度', value: '中' }
    ],
    apiParams: {
      blend_mode: 'artistic-fusion',
      opacity: 0.5,
      fusion_level: 0.7,
      quality: 90
    }
  }
];
