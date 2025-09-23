import { CompositionExample } from '../../../components/CompositionShowcase';

// 基础混合模式示例 (10种)
export const basicBlendExamples: CompositionExample[] = [
  {
    title: '正常混合',
    description: '标准的图层混合，保持自然的叠加效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/normal-blend.png',
    parameters: [
      { label: '模式', value: 'normal' },
      { label: '透明度', value: '60%' },
      { label: '位置', value: '对齐' }
    ],
    apiParams: {
      blend_mode: 'normal',
      opacity: 0.6,
      quality: 90
    }
  },
  {
    title: '正片叠底',
    description: '颜色变暗，产生深色阴影效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/multiply-blend.jpg',
    parameters: [
      { label: '模式', value: 'multiply' },
      { label: '透明度', value: '75%' },
      { label: '位置', value: '居中' }
    ],
    apiParams: {
      blend_mode: 'multiply',
      opacity: 0.75,
      quality: 90
    }
  },
  {
    title: '滤色混合',
    description: '颜色变亮，产生明亮的光影效果',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/screen-blend.jpg',
    parameters: [
      { label: '模式', value: 'screen' },
      { label: '透明度', value: '65%' },
      { label: '位置', value: '对齐' }
    ],
    apiParams: {
      blend_mode: 'screen',
      opacity: 0.65,
      quality: 90
    }
  },
  {
    title: '叠加混合',
    description: '结合正片叠底和滤色，增强对比度',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-blend.jpg',
    parameters: [
      { label: '模式', value: 'overlay' },
      { label: '透明度', value: '70%' },
      { label: '位置', value: '居中' }
    ],
    apiParams: {
      blend_mode: 'overlay',
      opacity: 0.7,
      quality: 90
    }
  },
  {
    title: '颜色减淡',
    description: '通过减少对比度来提亮颜色',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/color-dodge-blend.jpg',
    parameters: [
      { label: '模式', value: 'color-dodge' },
      { label: '透明度', value: '55%' },
      { label: '位置', value: '对齐' }
    ],
    apiParams: {
      blend_mode: 'color-dodge',
      opacity: 0.55,
      quality: 90
    }
  },
  {
    title: '颜色加深',
    description: '通过增加对比度来加深颜色',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/color-burn-blend.jpg',
    parameters: [
      { label: '模式', value: 'color-burn' },
      { label: '透明度', value: '65%' },
      { label: '位置', value: '居中' }
    ],
    apiParams: {
      blend_mode: 'color-burn',
      opacity: 0.65,
      quality: 90
    }
  },
  {
    title: '轻微混合',
    description: '轻微的混合效果，保持原图主要特征',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/soft-light-blend.jpg',
    parameters: [
      { label: '模式', value: 'soft-light' },
      { label: '透明度', value: '50%' },
      { label: '位置', value: '对齐' }
    ],
    apiParams: {
      blend_mode: 'soft-light',
      opacity: 0.5,
      quality: 90
    }
  },
  {
    title: '强烈混合',
    description: '强烈的混合效果，产生戏剧性对比',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/hard-light-blend.jpg',
    parameters: [
      { label: '模式', value: 'hard-light' },
      { label: '透明度', value: '80%' },
      { label: '位置', value: '居中' }
    ],
    apiParams: {
      blend_mode: 'hard-light',
      opacity: 0.8,
      quality: 90
    }
  },
  {
    title: '柔和正片叠底',
    description: '柔和版本的正片叠底，效果更自然',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/soft-multiply-blend.jpg',
    parameters: [
      { label: '模式', value: 'soft-multiply' },
      { label: '透明度', value: '60%' },
      { label: '位置', value: '对齐' }
    ],
    apiParams: {
      blend_mode: 'soft-multiply',
      opacity: 0.6,
      quality: 90
    }
  },
  {
    title: '强烈滤色',
    description: '强烈版本的滤色混合，光影效果更明显',
    baseImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg',
    overlayImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/hard-screen-blend.jpg',
    parameters: [
      { label: '模式', value: 'hard-screen' },
      { label: '透明度', value: '70%' },
      { label: '位置', value: '居中' }
    ],
    apiParams: {
      blend_mode: 'hard-screen',
      opacity: 0.7,
      quality: 90
    }
  }
];
