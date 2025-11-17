import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import GifOptimizeSettingsComponent from '../components/settings/GifOptimizeSettingsComponent';
import { gifOptimizeExamples } from '../config/examples/gifOptimizeExamples';
import { gifOptimizeEndpoint } from '../config/endpoints';

const GifPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="GIF优化压缩"
      description="GIF文件优化功能，支持压缩文件大小、调整颜色数量、缩放尺寸、优化帧率等。让你的GIF文件更小更流畅。"
      endpoint={gifOptimizeEndpoint}
      settingsComponent={GifOptimizeSettingsComponent}
      effectExamples={gifOptimizeExamples}
      downloadFileName="optimized.gif"
    />
  );
};

export default GifPage; 