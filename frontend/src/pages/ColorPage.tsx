import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import ColorSettingsComponent from '../components/settings/ColorSettingsComponent';
import { colorExamples } from '../config/examples/colorExamples';
import { colorEndpoint } from '../config/endpoints/colorEndpoint';
import { buildColorFormData, buildColorJsonData } from '../utils/colorApiLogic';
import { ColorSettings } from '../types/settings';

const ColorPage: React.FC = () => {
  // 自定义FormData构建函数
  const customFormDataBuilder = (formData: FormData, settings: Record<string, any>) => {
    buildColorFormData(formData, settings as ColorSettings);
  };

  // 自定义JSON构建函数
  const customJsonDataBuilder = (imageUrl: string, settings: Record<string, any>) => {
    return buildColorJsonData(imageUrl, settings as ColorSettings);
  };

  return (
    <ImageToolTabLayout
      title="色彩调整"
      description="专业的色彩调整工具，支持色相饱和度、色彩平衡、色阶等多种调整方式。支持文件上传和URL输入两种方式。"
      endpoint={colorEndpoint}
      settingsComponent={ColorSettingsComponent}
      effectExamples={colorExamples}
      downloadFileName="color-adjusted-image.jpg"
      customFormDataBuilder={customFormDataBuilder}
      customJsonDataBuilder={customJsonDataBuilder}
      enableLargeDisplay={true}
    />
  );
};

export default ColorPage;