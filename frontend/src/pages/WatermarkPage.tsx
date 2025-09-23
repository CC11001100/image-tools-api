import React from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import WatermarkSettingsComponent from '../components/settings/WatermarkSettingsComponent';
import { watermarkExamples } from '../config/examples/watermarkExamples';
import { watermarkEndpoint } from '../config/endpoints';

const WatermarkPage: React.FC = () => {
  // 自定义JSON构建函数，将前端参数映射到后端期望的参数名
  const buildWatermarkJsonData = (imageUrl: string, settings: Record<string, any>) => {
    return {
      image_url: imageUrl,
      watermark_text: settings.text, // 将 text 映射为 watermark_text
      position: settings.position,
      font_size: settings.font_size,
      font_color: settings.font_color,
      font_family: settings.font_family,
      opacity: settings.opacity,
      margin_x: settings.margin_x,
      margin_y: settings.margin_y,
      rotation: settings.rotation,
      stroke_width: settings.stroke_width,
      stroke_color: settings.stroke_color,
      shadow_offset_x: settings.shadow_offset_x,
      shadow_offset_y: settings.shadow_offset_y,
      shadow_color: settings.shadow_color,
      repeat_mode: settings.repeat_mode,
      quality: settings.quality,
    };
  };

  return (
    <ImageToolTabLayout
      title="图片水印"
      description="为图片添加水印，支持自定义文字、位置、字体、颜色等属性。可以用于添加版权信息、品牌标识等。"
      endpoint={watermarkEndpoint}
      settingsComponent={WatermarkSettingsComponent}
      effectExamples={watermarkExamples}
      downloadFileName="watermarked-image.jpg"
      customJsonDataBuilder={buildWatermarkJsonData}
    />
  );
};

export default WatermarkPage;