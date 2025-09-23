import { EffectExample } from '../../types/api';

export const artFilterExamples: EffectExample[] = [
  {
    title: "油画效果",
    description: "将图片转换为油画风格，呈现厚重的笔触和丰富的色彩层次",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/original-oil_painting.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-filter-oil_painting.jpg",
    parameters: [
      { label: "滤镜类型", value: "油画" },
      { label: "强度", value: "80%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/art-filter",
      filter_type: "oil_painting",
      intensity: 0.8,
      quality: 90
    }
  },
  {
    title: "轻度油画",
    description: "轻度油画效果，保留更多原图细节的同时增加艺术感",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/original-oil_painting_light.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-filter-oil_painting_light.jpg",
    parameters: [
      { label: "滤镜类型", value: "油画" },
      { label: "强度", value: "50%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/art-filter",
      filter_type: "oil_painting",
      intensity: 0.5,
      quality: 90
    }
  },
  {
    title: "铅笔素描",
    description: "将图片转换为铅笔素描风格，突出线条和明暗对比",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/original-pencil_sketch.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-filter-pencil_sketch.jpg",
    parameters: [
      { label: "滤镜类型", value: "素描" },
      { label: "强度", value: "100%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/art-filter",
      filter_type: "pencil_sketch",
      intensity: 1.0,
      quality: 90
    }
  },
  {
    title: "重度油画",
    description: "强烈的油画效果，色彩浓郁，笔触明显",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/original-oil_painting_heavy.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-filter-oil_painting_heavy.jpg",
    parameters: [
      { label: "滤镜类型", value: "油画" },
      { label: "强度", value: "120%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/art-filter",
      filter_type: "oil_painting",
      intensity: 1.2,
      quality: 90
    }
  },
  {
    title: "复古效果",
    description: "添加复古怀旧色调，营造经典的胶片摄影氛围",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/original-vintage.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/art-filter/art-filter-vintage.jpg",
    parameters: [
      { label: "滤镜类型", value: "复古效果" },
      { label: "强度", value: "70%" },
      { label: "质量", value: "90" }
    ],
    apiParams: {
      endpoint: "/api/v1/art-filter",
      filter_type: "vintage",
      intensity: 0.7,
      quality: 90
    }
  }
];
