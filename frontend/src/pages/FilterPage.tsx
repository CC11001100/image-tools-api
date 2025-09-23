import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import FilterSettingsComponent from '../components/settings/FilterSettingsComponent';
import { filterExamples } from '../config/examples/filterExamples';
import { filterEndpoint } from '../config/endpoints';

const FilterPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="图片滤镜"
      description="为图片添加各种滤镜效果，包括黑白、复古、锐化等多种效果。支持调整滤镜强度，让效果更自然。"
      endpoint={filterEndpoint}
      settingsComponent={FilterSettingsComponent}
      effectExamples={filterExamples}
      downloadFileName="filtered-image.jpg"
    />
  );
};

export default FilterPage; 