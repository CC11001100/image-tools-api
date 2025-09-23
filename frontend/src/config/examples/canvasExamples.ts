import { EffectExample } from '../../types/api';

export const canvasExamples: EffectExample[] = [
  {
    title: "简单实线边框",
    description: "添加黑色实线边框",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/canvas-original-solid-border.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/solid-border.jpg",
    parameters: [
      { label: "边框类型", value: "实线" },
      { label: "边框宽度", value: "2px" },
      { label: "边框颜色", value: "黑色" },
      { label: "边框样式", value: "简单" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/canvas",
      canvas_type: "border",
      border_width: 2,
      border_color: "#000000",
      quality: 90
    }
  },
  {
    title: "花式虚线边框",
    description: "添加彩色虚线边框",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/canvas-original-fancy-dashed.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/fancy-dashed.jpg",
    parameters: [
      { label: "边框类型", value: "虚线" },
      { label: "边框宽度", value: "3px" },
      { label: "边框颜色", value: "橙红色" },
      { label: "边框样式", value: "花式" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/canvas",
      canvas_type: "border",
      border_width: 3,
      border_color: "#FF5733",
      quality: 90
    }
  },
  {
    title: "现代点线边框",
    description: "添加现代风格的点线边框",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/canvas-original-modern-dotted.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/modern-dotted.jpg",
    parameters: [
      { label: "边框类型", value: "点线" },
      { label: "边框宽度", value: "2px" },
      { label: "边框颜色", value: "蓝色" },
      { label: "边框样式", value: "现代" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/canvas",
      canvas_type: "border",
      border_width: 2,
      border_color: "#3498DB",
      quality: 90
    }
  },
  {
    title: "经典双线边框",
    description: "添加经典风格的双线边框",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/canvas-original-classic-double.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/classic-double.jpg",
    parameters: [
      { label: "边框类型", value: "双线" },
      { label: "边框宽度", value: "4px" },
      { label: "边框颜色", value: "深灰色" },
      { label: "边框样式", value: "经典" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/canvas",
      canvas_type: "border",
      border_width: 4,
      border_color: "#2C3E50",
      quality: 90
    }
  },
  {
    title: "画布扩展",
    description: "扩展画布大小，增加边距空间",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/canvas-original-padding-expand.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/padding-expand.jpg",
    parameters: [
      { label: "画布类型", value: "扩展" },
      { label: "内边距", value: "20px" },
      { label: "背景颜色", value: "浅灰色" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/canvas",
      canvas_type: "expand",
      padding: 20,
      background_color: "#F8F9FA",
      quality: 90
    }
  },
  {
    title: "背景填充",
    description: "添加背景色填充，创建边距效果",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/canvas-original-background-fill.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/canvas/background-fill.jpg",
    parameters: [
      { label: "画布类型", value: "填充" },
      { label: "内边距", value: "15px" },
      { label: "背景颜色", value: "浅蓝色" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/canvas",
      canvas_type: "padding",
      padding: 15,
      background_color: "#E8F4FD",
      quality: 90
    }
  }
];



// 格式转换效果示例
