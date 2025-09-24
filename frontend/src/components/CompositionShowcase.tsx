/**
 * CompositionShowcase - 简化实现
 * 临时占位符组件，避免循环引用
 */

import React from 'react';

// 添加类型定义
export interface CompositionExample {
  id?: string;
  title: string;
  description?: string;
  beforeImage?: string;
  afterImage?: string;
  resultImage?: string;
  baseImage?: string;
  overlayImage?: string;
  processedImage?: string;
  parameters?: any[];
  apiParams?: any;
}

export interface CompositionShowcaseProps {
  examples?: CompositionExample[];
}

const CompositionShowcase: React.FC<CompositionShowcaseProps> = (props) => {
  return (
    <div className="p-4 border border-gray-300 rounded">
      <h3 className="text-lg font-semibold mb-2">CompositionShowcase</h3>
      <p className="text-gray-600">组件正在重构中...</p>
    </div>
  );
};

export { CompositionShowcase };
export default CompositionShowcase;
