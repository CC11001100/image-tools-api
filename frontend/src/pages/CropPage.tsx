import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import CropSettingsComponent from '../components/settings/CropSettingsComponent';
import { cropExamples } from '../config/examples/cropExamples';
import { cropEndpoint } from '../config/endpoints';

const CropPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="图片裁剪"
      description="图片裁剪功能，支持矩形裁剪、圆形裁剪、智能裁剪等多种方式。可以指定裁剪区域和纵横比。"
      endpoint={cropEndpoint}
      settingsComponent={CropSettingsComponent}
      effectExamples={cropExamples}
      downloadFileName="cropped-image.jpg"
    />
  );
};

export default CropPage; 