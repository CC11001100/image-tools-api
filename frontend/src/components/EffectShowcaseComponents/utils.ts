/**
 * 效果展示组件的工具函数
 */

import { EffectExample, MultiImageEffectExample } from '../../types/api';

// 获取图片尺寸显示文本
export const getImageDimensionsText = (example: EffectExample | MultiImageEffectExample): string => {
  if (example.imageDimensions?.processed) {
    const { width, height } = example.imageDimensions.processed;
    return `${width}×${height}px`;
  }
  return '处理后';
};

// 计算图片样式
export const getImageStyle = (example: EffectExample | MultiImageEffectExample, showOriginalSize: boolean) => {
  const baseStyle = {
    border: '2px solid #4caf50',
    borderRadius: '4px',
  };

  if (showOriginalSize) {
    return {
      ...baseStyle,
      width: 'auto',
      height: 'auto',
      maxWidth: 'none',
      maxHeight: 'none',
      transform: example.imageDimensions?.processed &&
                example.imageDimensions.processed.width <= 300 &&
                example.imageDimensions.processed.height <= 300
                ? 'scale(1.5)'
                : 'scale(1)'
    };
  }

  if (example.imageDimensions?.processed) {
    return {
      ...baseStyle,
      width: `${Math.min(260, (example.imageDimensions.processed.width / 4128) * 260)}px`,
      height: `${Math.min(195, (example.imageDimensions.processed.height / 6192) * 195)}px`
    };
  }

  return {
    ...baseStyle,
    maxWidth: '100%',
    maxHeight: '280px',
    objectFit: 'contain' as const
  };
};
