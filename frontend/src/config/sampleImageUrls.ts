/**
 * 示例图片URL配置
 * 用于快速测试图片处理功能
 */

export interface SampleImageUrl {
  name: string;
  url: string;
  description: string;
  category: string;
  size?: string;
}

export const sampleImageUrls: SampleImageUrl[] = [
  // 风景类
  {
    name: "自然风景",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg",
    description: "自然风景，适合测试色彩调整和滤镜效果",
    category: "风景",
    size: "1600×2400"
  },
  {
    name: "城市建筑",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-stretch.jpg",
    description: "城市建筑摄影，适合测试亮度对比度调整",
    category: "风景",
    size: "1600×2400"
  },
  {
    name: "自然景观",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-hq-600px.jpg",
    description: "美丽自然景观，适合测试暖色调效果",
    category: "风景",
    size: "1600×2400"
  },

  // 色彩测试
  {
    name: "色彩测试-1",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/original.jpg",
    description: "色彩测试图片，适合测试色彩调整功能",
    category: "色彩",
    size: "800×600"
  },
  {
    name: "色彩测试-2",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/hsl-combined.jpg",
    description: "色彩测试图片，适合测试HSL调整",
    category: "色彩",
    size: "800×600"
  },
  {
    name: "色彩测试-3",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/color/balance-warm.jpg",
    description: "色彩测试图片，适合测试色彩平衡",
    category: "色彩",
    size: "800×600"
  },

  // 艺术效果
  {
    name: "艺术效果-1",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-oil-painting.jpg",
    description: "艺术效果测试图片，适合测试滤镜效果",
    category: "艺术",
    size: "800×600"
  },
  {
    name: "艺术效果-2",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-watercolor.jpg",
    description: "艺术效果测试图片，适合测试水彩效果",
    category: "艺术",
    size: "800×600"
  },

  // 文字测试
  {
    name: "文字测试-1",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-1.jpg",
    description: "文字测试图片，适合测试文字效果",
    category: "文字",
    size: "800×600"
  },
  {
    name: "文字测试-2",
    url: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/text/text-example-2.jpg",
    description: "文字测试图片，适合测试文字叠加",
    category: "文字",
    size: "800×600"
  }
];

export const sampleImageCategories = [
  "全部",
  "风景", 
  "色彩",
  "艺术",
  "文字"
];

/**
 * 根据分类获取示例图片
 */
export const getSampleImagesByCategory = (category: string): SampleImageUrl[] => {
  if (category === "全部") {
    return sampleImageUrls;
  }
  return sampleImageUrls.filter(img => img.category === category);
};

/**
 * 获取随机示例图片
 */
export const getRandomSampleImage = (): SampleImageUrl => {
  return sampleImageUrls[Math.floor(Math.random() * sampleImageUrls.length)];
}; 