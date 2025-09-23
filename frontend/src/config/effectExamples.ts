// 效果示例配置 - 重构后的统一导出文件
// 原来的2065行大文件已被拆分为16个小文件，每个文件负责一个功能模块的示例配置
// 这样做提高了代码的可维护性，每个模块的示例都有独立的文件

// 重新导出所有效果示例配置
export {
  artFilterExamples,
  blendExamples,
  colorExamples,
  cropExamples,
  transformExamples,
  watermarkExamples,
  filterExamples,
  resizeExamples,
  enhanceExamples,
  pixelateExamples,
  noiseExamples,
  stitchExamples,
  canvasExamples,
  formatExamples,

  perspectiveExamples
} from './examples';

// 导出类型定义
export type { EffectExample } from '../types/api';