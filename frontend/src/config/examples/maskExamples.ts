import { EffectExample } from '../../types/api';

// 遮罩效果示例
export const maskExamples: EffectExample[] = [
  {
    title: "圆形遮罩",
    description: "使用圆形遮罩裁剪图片，创建圆形效果",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-circle.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-circle.jpg",
    parameters: [
      { label: '遮罩类型', value: '圆形' },
      { label: '羽化', value: '10px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: "/api/v1/mask",
      mask_type: "circle",
      feather: 10,
      quality: 90
    }
  },
  {
    title: "矩形遮罩",
    description: "使用矩形遮罩裁剪图片，创建矩形效果",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-rectangle.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-rectangle.jpg",
    parameters: [
      { label: '遮罩类型', value: '矩形' },
      { label: '羽化', value: '5px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: "/api/v1/mask",
      mask_type: "rectangle",
      feather: 5,
      quality: 90
    }
  },
  {
    title: "椭圆遮罩",
    description: "使用椭圆遮罩裁剪图片，创建椭圆效果",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-ellipse.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-ellipse.jpg",
    parameters: [
      { label: '遮罩类型', value: '椭圆' },
      { label: '羽化', value: '8px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: "/api/v1/mask",
      mask_type: "ellipse",
      feather: 8,
      quality: 90
    }
  },
  {
    title: "星形遮罩",
    description: "使用星形遮罩裁剪图片，创建星形效果",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-star.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-star.jpg",
    parameters: [
      { label: '遮罩类型', value: '星形' },
      { label: '角数', value: '5' },
      { label: '羽化', value: '5px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: "/api/v1/mask",
      mask_type: "star",
      feather: 5,
      points: 5,
      quality: 90
    }
  },
  {
    title: "心形遮罩",
    description: "使用心形遮罩裁剪图片，创建心形效果",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-heart.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-heart.jpg",
    parameters: [
      { label: '遮罩类型', value: '心形' },
      { label: '羽化', value: '8px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: "/api/v1/mask",
      mask_type: "heart",
      feather: 8,
      quality: 90
    }
  },
  {
    title: "圆角矩形遮罩",
    description: "使用圆角矩形遮罩裁剪图片，创建圆角效果",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-rounded_rectangle.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-rounded_rectangle.jpg",
    parameters: [
      { label: '遮罩类型', value: '圆角矩形' },
      { label: '圆角半径', value: '50px' },
      { label: '羽化', value: '5px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: "/api/v1/mask",
      mask_type: "rounded_rectangle",
      feather: 5,
      radius: 50,
      quality: 90
    }
  }
];
