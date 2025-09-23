import { EffectExample } from '../../types/api';

export const colorExamples: EffectExample[] = [
  {
    title: "亮度调整",
    description: "增强图片亮度，让图片更明亮清晰",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/original-brightness.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/color-brightness.jpg",
    parameters: [
      { label: "调整类型", value: "亮度" },
      { label: "调整值", value: "30%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/color",
      brightness: 30,
      quality: 90
    }
  },
  {
    title: "对比度调整",
    description: "增强图片对比度，让明暗对比更鲜明",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/original-contrast.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/color-contrast.jpg",
    parameters: [
      { label: "调整类型", value: "对比度" },
      { label: "调整值", value: "25%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/color",
      contrast: 25,
      quality: 90
    }
  },
  {
    title: "饱和度调整",
    description: "增强图片饱和度，让色彩更鲜艳生动",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/original-saturation.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/color-saturation.jpg",
    parameters: [
      { label: "调整类型", value: "饱和度" },
      { label: "调整值", value: "40%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/color",
      saturation: 40,
      quality: 90
    }
  },
  {
    title: "色相调整",
    description: "调整图片色相，改变整体色调",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/original-hue.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/color-hue.jpg",
    parameters: [
      { label: "调整类型", value: "色相" },
      { label: "调整值", value: "30°" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/color",
      hue: 30,
      quality: 90
    }
  },
  {
    title: "伽马调整",
    description: "调整图片伽马值，改善明暗层次",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/original-gamma.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/color-gamma.jpg",
    parameters: [
      { label: "调整类型", value: "伽马" },
      { label: "调整值", value: "1.5" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/color",
      gamma: 1.5,
      quality: 90
    }
  }
];
