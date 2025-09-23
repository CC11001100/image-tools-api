import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import MaskSettingsComponent from '../components/settings/MaskSettingsComponent';
import { maskExamples } from '../config/examples/maskExamples';
import { maskEndpoint } from '../config/endpoints';

const MaskPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="图片遮罩"
      description="图片遮罩效果，支持多种遮罩形状和渐变效果。可以创建各种遮罩效果，如渐变遮罩、形状遮罩等。"
      endpoint={maskEndpoint}
      settingsComponent={MaskSettingsComponent}
      effectExamples={maskExamples}
      downloadFileName="masked-image.jpg"
    />
  );
};

export default MaskPage; 