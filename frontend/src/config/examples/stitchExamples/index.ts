/**
 * 拼接展示示例 - 统一导出
 * 将原来的452行大文件拆分为4个功能模块，提高可维护性
 */

import { basicStitchExamples } from './basicStitchExamples';
import { horizontalStitchExamples } from './horizontalStitchExamples';
import { verticalStitchExamples } from './verticalStitchExamples';
import { gridStitchExamples } from './gridStitchExamples';
import { backgroundStitchExamples } from './backgroundStitchExamples';

// 合并所有拼接示例
export const stitchShowcaseExamples = [
  ...basicStitchExamples,
  ...horizontalStitchExamples,
  ...verticalStitchExamples,
  ...gridStitchExamples,
  ...backgroundStitchExamples
];

// 分类导出，便于按需使用
export {
  basicStitchExamples,
  horizontalStitchExamples,
  verticalStitchExamples,
  gridStitchExamples,
  backgroundStitchExamples
};
