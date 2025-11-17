import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import GifExtractSettingsComponent from '../components/settings/GifExtractSettingsComponent';
import { gifExtractExamples } from '../config/examples/gifExtractExamples';
import { gifExtractEndpoint } from '../config/endpoints';

const GifExtractPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="GIF帧提取"
      description="将GIF动画分解为单独的图片帧，支持选择性提取、批量下载、多种输出格式。轻松获取GIF中的任意帧。"
      endpoint={gifExtractEndpoint}
      settingsComponent={GifExtractSettingsComponent}
      effectExamples={gifExtractExamples}
      downloadFileName="extracted-frames.zip"
    />
  );
};

export default GifExtractPage; 