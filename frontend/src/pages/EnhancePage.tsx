import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import EnhanceSettingsComponent from '../components/settings/EnhanceSettingsComponent';
import { enhanceExamples } from '../config/examples/enhanceExamples';
import { enhanceEndpoint } from '../config/endpoints';

const EnhancePage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="图片增强"
      description="图片增强处理，支持多种增强效果，包括锐化、降噪、HDR等。可以调整效果强度和参数。"
      endpoint={enhanceEndpoint}
      settingsComponent={EnhanceSettingsComponent}
      effectExamples={enhanceExamples}
      downloadFileName="enhanced-image.jpg"
    />
  );
};

export default EnhancePage; 