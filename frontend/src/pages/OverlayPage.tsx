import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import OverlaySettingsComponent from '../components/settings/OverlaySettingsComponent';
import { overlayExamples } from '../config/examples/overlayExamples';
import { overlayEndpoint } from '../config/endpoints';

const OverlayPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="图片叠加"
      description="为图片添加叠加效果，支持多种叠加模式和透明度调整。可以用于添加水印、特效等。"
      endpoint={overlayEndpoint}
      settingsComponent={OverlaySettingsComponent}
      effectExamples={overlayExamples}
      downloadFileName="overlay-image.jpg"
    />
  );
};

export default OverlayPage; 