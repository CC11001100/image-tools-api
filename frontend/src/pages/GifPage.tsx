import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import GifSettingsComponent from '../components/settings/GifSettingsComponent';
import { gifExamples } from '../config/examples/gifExamples';
import { gifEndpoint } from '../config/endpoints';

const GifPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="GIF处理"
      description="GIF图片处理功能，支持调整帧率、尺寸、压缩等。可以优化GIF大小、调整播放速度、提取帧等。"
      endpoint={gifEndpoint}
      settingsComponent={GifSettingsComponent}
      effectExamples={gifExamples}
      downloadFileName="processed.gif"
    />
  );
};

export default GifPage; 