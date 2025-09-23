import React from 'react';
import { Box } from '@mui/material';
import { UniversalApiDocumentation } from './documentation/UniversalApiDocumentation';
import { colorEndpoint } from '../config/endpoints/colorEndpoint';
import { ColorSettings } from '../types/settings';

interface ColorApiDocumentationProps {
  settings: ColorSettings;
}

export const ColorApiDocumentation: React.FC<ColorApiDocumentationProps> = ({
  settings
}) => {
  return (
    <Box>
      <UniversalApiDocumentation
        endpoint={{
          ...colorEndpoint,
          description: `图片色彩调整API，支持多种调整方式和参数设置。当前选择的调整类型：${settings.adjustment_type}。

本接口提供专业的色彩调整功能，可以精确控制图片的色彩表现。支持以下调整类型：
• HSL调整：控制色相、饱和度、亮度
• RGB调整：调整红、绿、蓝通道
• CMYK调整：调整青、品红、黄、黑通道
• 自动调整：智能分析并优化色彩

参数：
- image: File (必需)
- adjustment_type: string (必需) - 可选值: hsl, rgb, cmyk, auto
- brightness: number (可选) - 亮度调整，范围：-100 到 100
- contrast: number (可选) - 对比度调整，范围：-100 到 100
- saturation: number (可选) - 饱和度调整，范围：-100 到 100
- hue: number (可选) - 色相调整，范围：-180 到 180
- gamma: number (可选) - 伽马值调整，范围：0.1 到 10
- temperature: number (可选) - 色温调整，范围：-100 到 100
- tint: number (可选) - 色调调整，范围：-100 到 100
- vibrance: number (可选) - 自然饱和度，范围：-100 到 100
- exposure: number (可选) - 曝光度调整，范围：-100 到 100`
        }}
        settings={settings}
      />
    </Box>
  );
}; 