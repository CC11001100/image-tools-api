import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import PixelateSettingsComponent from '../components/settings/PixelateSettingsComponent';
import { pixelateExamples } from '../config/examples/pixelateExamples';
import { pixelateEndpoint } from '../config/endpoints';

const PixelatePage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="图片像素化"
      description="图片像素化处理，支持整体像素化和区域像素化。可以调整像素块大小和处理区域。"
      endpoint={pixelateEndpoint}
      settingsComponent={PixelateSettingsComponent}
      effectExamples={pixelateExamples}
      downloadFileName="pixelated-image.jpg"
    />
  );
};

export default PixelatePage; 