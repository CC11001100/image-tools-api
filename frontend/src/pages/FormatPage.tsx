import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import FormatSettingsComponent from '../components/settings/FormatSettingsComponent';
import { formatExamples } from '../config/examples/formatExamples';
import { formatEndpoint } from '../config/endpoints';

const FormatPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="格式转换"
      description="转换图片格式，支持多种格式之间的转换，可以调整压缩质量和其他参数。支持JPEG、PNG、WebP等常见格式。"
      endpoint={formatEndpoint}
      settingsComponent={FormatSettingsComponent}
      effectExamples={formatExamples}
      downloadFileName="converted-image"
    />
  );
};

export default FormatPage; 