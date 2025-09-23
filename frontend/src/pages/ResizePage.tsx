import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import ResizeSettingsComponent from '../components/settings/ResizeSettingsComponent';
import { resizeExamples } from '../config/examples/resizeExamples';
import { resizeEndpoint } from '../config/endpoints';

const ResizePage: React.FC = () => {
  // 自定义参数映射函数，将前端参数名映射到后端期望的参数名
  const customFormDataBuilder = (formData: FormData, settings: Record<string, any>) => {
    // 映射参数名称
    const paramMapping: Record<string, string> = {
      'keepAspectRatio': 'maintain_aspect',
      // 其他参数保持原名
    };

    for (const [key, value] of Object.entries(settings)) {
      // 跳过不支持的参数
      if (key === 'mode' || key === 'compressionLevel') {
        continue;
      }

      // 使用映射后的参数名
      const mappedKey = paramMapping[key] || key;
      formData.append(mappedKey, String(value));
    }
  };

  return (
    <ImageToolTabLayout
      title="图片缩放"
      description="调整图片大小，支持多种调整模式和参数设置。可以按比例缩放、指定尺寸、保持纵横比等。"
      endpoint={resizeEndpoint}
      settingsComponent={ResizeSettingsComponent}
      effectExamples={resizeExamples}
      downloadFileName="resized-image.jpg"
      customFormDataBuilder={customFormDataBuilder}
    />
  );
};

export default ResizePage; 