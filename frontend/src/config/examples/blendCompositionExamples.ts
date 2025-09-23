import { CompositionExample } from '../../components/CompositionShowcase';
import {
  basicBlendExamples,
  specialEffectBlendExamples,
  artisticBlendExamples,
  sceneBlendExamples
} from './blend';

// 图片混合合成效果示例 - 34种混合效果（模块化）
export const blendCompositionExamples: CompositionExample[] = [
  ...basicBlendExamples,
  ...specialEffectBlendExamples,
  ...artisticBlendExamples,
  ...sceneBlendExamples
];
