import { EffectExample } from '../../types/api';

// Perspective 效果示例
export const perspectiveExamples: EffectExample[] = [
  {
    title: '透视校正 - 标准',
    description: '修正图像的透视变形，使画面更加自然',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/perspective-original-correct-standard.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/correct-standard.jpg',
    parameters: [
      { label: '类型', value: '透视校正' },
      { label: '宽度', value: '800' },
      { label: '高度', value: '600' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/perspective',
      points: '[[0,0],[800,0],[800,600],[0,600]]',
      width: 800,
      height: 600,
      quality: 90
    }
  },
  {
    title: '透视校正 - 倾斜',
    description: '修正倾斜拍摄的照片，恢复正常视角',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/perspective-original-correct-tilted.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/correct-tilted.jpg',
    parameters: [
      { label: '类型', value: '透视校正' },
      { label: '宽度', value: '500' },
      { label: '高度', value: '400' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/perspective',
      points: '[[70,80],[550,70],[530,420],[50,430]]',
      width: 500,
      height: 400,
      quality: 90
    }
  },
  {
    title: '自动文档校正 1',
    description: '自动检测并校正文档边缘',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/perspective-original-auto-document-1.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/auto-document-1.jpg',
    parameters: [
      { label: '类型', value: '自动文档校正' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/perspective',
      quality: 90,
      auto_document: true
    }
  },
  {
    title: '自动文档校正 2',
    description: '自动校正倾斜的文档扫描',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/perspective-original-auto-document-2.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/auto-document-2.jpg',
    parameters: [
      { label: '类型', value: '自动文档校正' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/perspective',
      quality: 90,
      auto_document: true
    }
  },
  {
    title: '透视校正 - 建筑',
    description: '修正建筑物的透视变形',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/perspective-original-correct-architecture.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/correct-architecture.jpg',
    parameters: [
      { label: '类型', value: '透视校正' },
      { label: '宽度', value: '600' },
      { label: '高度', value: '800' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/perspective',
      points: '[[100,50],[500,50],[500,750],[100,750]]',
      width: 600,
      height: 800,
      quality: 90
    }
  },
  {
    title: '透视校正 - 景观',
    description: '修正风景照片的透视变形',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/perspective-original-correct-landscape.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/perspective/correct-landscape.jpg',
    parameters: [
      { label: '类型', value: '透视校正' },
      { label: '宽度', value: '800' },
      { label: '高度', value: '500' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/perspective',
      points: '[[50,100],[750,100],[750,400],[50,400]]',
      width: 800,
      height: 500,
      quality: 90
    }
  }
];