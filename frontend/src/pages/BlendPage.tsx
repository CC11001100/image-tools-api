import React from 'react';
import { Box } from '@mui/material';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import BlendSettingsComponent from '../components/settings/BlendSettingsComponent';
import { blendExamples } from '../config/examples/blendExamples';
import { blendEndpoint } from '../config/endpoints/blendEndpoint';

const BlendPage: React.FC = () => {
  // 自定义FormData构建函数，处理两张图片
  const customFormDataBuilder = (formData: FormData, settings: Record<string, any>) => {
    // 添加混合参数
    formData.append('blend_mode', settings.blend_mode || 'normal');
    formData.append('opacity', String(settings.opacity || 0.5));
    formData.append('quality', String(settings.quality || 90));

    if (settings.position) {
      formData.append('position', settings.position);
    }
    if (settings.x_offset !== undefined) {
      formData.append('x_offset', String(settings.x_offset));
    }
    if (settings.y_offset !== undefined) {
      formData.append('y_offset', String(settings.y_offset));
    }
    if (settings.scale !== undefined) {
      formData.append('scale', String(settings.scale));
    }

    // 添加叠加图片
    if (settings.overlay_file) {
      formData.append('blend_image', settings.overlay_file);
    }
  };

  // 自定义JSON构建函数，处理两张图片URL
  const customJsonDataBuilder = (imageUrl: string, settings: Record<string, any>) => {
    return {
      base_image_url: imageUrl,
      blend_image_url: settings.overlay_url || '',
      blend_mode: settings.blend_mode || 'normal',
      opacity: settings.opacity || 0.5,
      position: settings.position || 'center',
      x_offset: settings.x_offset || 0,
      y_offset: settings.y_offset || 0,
      scale: settings.scale || 1.0,
      quality: settings.quality || 90,
    };
  };
  return (
    <Box>
      <ImageToolTabLayout
        title="图像混合"
        description="将两张图片按照指定的混合模式进行合成，支持多种专业的混合效果。支持文件上传和URL输入两种方式。"
        endpoint={blendEndpoint}
        settingsComponent={BlendSettingsComponent}
        effectExamples={blendExamples}
        downloadFileName="blend-result.jpg"
        customFormDataBuilder={customFormDataBuilder}
        customJsonDataBuilder={customJsonDataBuilder}
        enableLargeDisplay={true}
      />
    </Box>
  );
};

export default BlendPage;