/**
 * StitchShowcase - 简化实现
 * 临时占位符组件，避免循环引用
 */

import React from 'react';

// 添加类型定义
export interface StitchExample {
  id?: string;
  title: string;
  description?: string;
  images?: string[];
  originalImages?: string[];
  resultImage?: string;
  processedImage?: string;
  parameters?: any[];
  apiParams?: any;
}

export interface StitchShowcaseProps {
  examples?: StitchExample[];
}

const StitchShowcase: React.FC<StitchShowcaseProps> = (props) => {
  return (
    <div className="p-4 border border-gray-300 rounded">
      <h3 className="text-lg font-semibold mb-2">StitchShowcase</h3>
      <p className="text-gray-600">组件正在重构中...</p>
    </div>
  );
};

export { StitchShowcase };
export default StitchShowcase;
