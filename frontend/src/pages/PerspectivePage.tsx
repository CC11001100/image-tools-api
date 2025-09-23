import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import PerspectiveSettingsComponent from '../components/settings/PerspectiveSettingsComponent';
import { perspectiveExamples } from '../config/examples/perspectiveExamples';
import { perspectiveEndpoint } from '../config/endpoints';

const PerspectivePage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="透视校正"
      description="透视变换和校正，支持手动四点校正和自动文档检测。可以用于文档扫描、图片矫正等场景。"
      endpoint={perspectiveEndpoint}
      settingsComponent={PerspectiveSettingsComponent}
      effectExamples={perspectiveExamples}
      downloadFileName="perspective-corrected.jpg"
    />
  );
};

export default PerspectivePage; 