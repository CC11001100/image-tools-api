import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import GifCreateSettingsComponent from '../components/settings/GifCreateSettingsComponent';
import { gifCreateExamples } from '../config/examples/gifCreateExamples';
import { gifCreateEndpoint } from '../config/endpoints';

const ImageToGifPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="GIF动画创建"
      description="将多张图片合成为GIF动画，支持自定义帧率、循环次数、优化设置。创建流畅的动态图片。"
      endpoint={gifCreateEndpoint}
      settingsComponent={GifCreateSettingsComponent}
      effectExamples={gifCreateExamples}
      downloadFileName="created-animation.gif"
    />
  );
};

export default ImageToGifPage; 