import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import AnnotationSettingsComponent from '../components/settings/AnnotationSettingsComponent';
import { annotationExamples } from '../config/examples/annotationExamples';
import { annotationEndpoint } from '../config/endpoints';

const AnnotationPage: React.FC = () => {
  return (
    <ImageToolTabLayout
      title="图片标注"
      description="为图片添加箭头、文字等标注，支持自定义颜色、大小、位置等属性。可以用于图片说明、教程制作等场景。"
      endpoint={annotationEndpoint}
      settingsComponent={AnnotationSettingsComponent}
      effectExamples={annotationExamples}
      downloadFileName="annotated-image.jpg"
    />
  );
};

export default AnnotationPage; 