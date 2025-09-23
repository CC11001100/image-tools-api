import { EffectExample, MultiImageEffectExample } from '../../types/api';

export const blendExamples: MultiImageEffectExample[] = [
  {
    title: "正常混合",
    description: "标准的图层混合，保持自然的叠加效果",
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-normal.jpg",
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-normal.jpg"
    ],
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-normal.jpg",
    parameters: [
      { label: "混合模式", value: "正常混合" },
      { label: "不透明度", value: "60%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/blend",
      blend_mode: "normal",
      opacity: 0.6,
      quality: 90
    }
  },
  {
    title: "正片叠底",
    description: "颜色变暗，产生深色阴影效果",
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-multiply.jpg",
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-multiply.jpg"
    ],
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-multiply.jpg",
    parameters: [
      { label: "混合模式", value: "正片叠底" },
      { label: "不透明度", value: "75%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/blend",
      blend_mode: "multiply",
      opacity: 0.75,
      quality: 90
    }
  },
  {
    title: "滤色混合",
    description: "使用滤色混合模式，产生更亮的混合效果",
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-screen.jpg",
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-screen.jpg"
    ],
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-screen.jpg",
    parameters: [
      { label: "混合模式", value: "滤色" },
      { label: "不透明度", value: "80%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/blend",
      blend_mode: "screen",
      opacity: 0.8,
      quality: 90
    }
  },
  {
    title: "叠加混合",
    description: "使用叠加混合模式，结合正片叠底和滤色效果",
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-overlay.jpg",
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-overlay.jpg"
    ],
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-overlay.jpg",
    parameters: [
      { label: "混合模式", value: "叠加" },
      { label: "不透明度", value: "90%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/blend",
      blend_mode: "overlay",
      opacity: 0.9,
      quality: 90
    }
  },
  {
    title: "滤色混合",
    description: "颜色变亮，产生明亮的光影效果",
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-screen.jpg",
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-screen.jpg"
    ],
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-screen.jpg",
    parameters: [
      { label: "混合模式", value: "滤色混合" },
      { label: "不透明度", value: "65%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/blend",
      blend_mode: "screen",
      opacity: 0.65,
      quality: 90
    }
  },
  {
    title: "叠加混合",
    description: "结合正片叠底和滤色，增强对比度",
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-overlay.jpg",
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-overlay.jpg"
    ],
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-overlay.jpg",
    parameters: [
      { label: "混合模式", value: "叠加混合" },
      { label: "不透明度", value: "70%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/blend",
      blend_mode: "overlay",
      opacity: 0.7,
      quality: 90
    }
  },
  {
    title: "颜色减淡",
    description: "通过减少对比度来提亮颜色",
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-color-dodge.jpg",
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-color-dodge.jpg"
    ],
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-color-dodge.jpg",
    parameters: [
      { label: "混合模式", value: "颜色减淡" },
      { label: "不透明度", value: "55%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/blend",
      blend_mode: "color-dodge",
      opacity: 0.55,
      quality: 90
    }
  },
  {
    title: "颜色加深",
    description: "通过增加对比度来加深颜色",
    originalImages: [
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/base-color-burn.jpg",
      "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/overlay-color-burn.jpg"
    ],
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/blend/blend-color-burn.jpg",
    parameters: [
      { label: "混合模式", value: "颜色加深" },
      { label: "不透明度", value: "60%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/blend",
      blend_mode: "color-burn",
      opacity: 0.6,
      quality: 90
    }
  }
];
