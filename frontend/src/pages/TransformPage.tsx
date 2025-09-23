import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import TransformSettingsComponent from '../components/settings/TransformSettingsComponent';
import { transformExamples } from '../config/examples/transformExamples';
import { transformEndpoint } from '../config/endpoints';

const TransformPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="图片变换"
      description="图片变换处理，支持旋转、翻转、缩放等基础变换。可以调整图片的角度、方向和比例。"
      endpoint={transformEndpoint}
      settingsComponent={TransformSettingsComponent}
      effectExamples={transformExamples}
      downloadFileName="transformed-image.jpg"
    />
  );
};

export default TransformPage; 