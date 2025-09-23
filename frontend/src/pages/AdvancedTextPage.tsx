import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import AdvancedTextSettingsComponent from '../components/settings/AdvancedTextSettingsComponent';
import { advancedTextExamples } from '../config/examples/advancedTextExamples';
import { advancedTextEndpoint } from '../config/endpoints';

const AdvancedTextPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="高级文字效果"
      description="高级文字效果处理，支持3D文字、发光文字、渐变文字等特效。可以创建各种炫酷的文字效果。"
      endpoint={advancedTextEndpoint}
      settingsComponent={AdvancedTextSettingsComponent}
      effectExamples={advancedTextExamples}
      downloadFileName="advanced-text.jpg"
    />
  );
};

export default AdvancedTextPage; 