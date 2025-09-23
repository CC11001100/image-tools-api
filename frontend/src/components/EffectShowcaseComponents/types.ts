/**
 * 效果展示组件相关的类型定义
 */

import { EffectExample, MultiImageEffectExample } from '../../types/api';

export interface EffectShowcaseProps {
  title: string;
  description: string;
  examples: EffectExample[] | MultiImageEffectExample[];
  onApplyParams?: (params: Record<string, any>) => void;
  showOriginal?: boolean;
  originalImage?: string;
  enableSizeComparison?: boolean;
  showOriginalSize?: boolean;
  enableLargeDisplay?: boolean;
}

export interface EffectCardProps {
  example: EffectExample | MultiImageEffectExample;
  originalImage?: string;
  enableSizeComparison: boolean;
  showOriginalSize: boolean;
  onImageClick: (imageSrc: string, imageTitle: string) => void;
  onApplyParams?: (example: EffectExample | MultiImageEffectExample) => void;
}

export interface ImageDisplayProps {
  example: EffectExample | MultiImageEffectExample;
  originalImage?: string;
  enableSizeComparison: boolean;
  showOriginalSize: boolean;
  onImageClick: (imageSrc: string, imageTitle: string) => void;
}

export interface CardContentProps {
  example: EffectExample | MultiImageEffectExample;
  onApplyParams?: (example: EffectExample | MultiImageEffectExample) => void;
}

export interface GalleryState {
  galleryOpen: boolean;
  currentImageIndex: number;
  galleryImages: Array<{
    src: string;
    alt: string;
    title: string;
    description: string;
  }>;
}
