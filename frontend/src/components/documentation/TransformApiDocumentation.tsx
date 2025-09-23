import React from 'react';
import { Box } from '@mui/material';
import { UniversalApiDocumentation } from './UniversalApiDocumentation';
import { transformEndpoint } from '../../config/endpoints';
import { TransformSettings } from '../../types/settings';

interface TransformApiDocumentationProps {
  settings: TransformSettings;
}

export const TransformApiDocumentation: React.FC<TransformApiDocumentationProps> = ({
  settings
}) => {
  return (
    <Box>
      <UniversalApiDocumentation
        endpoint={{
          ...transformEndpoint,
          description: `图片变换API，支持旋转、翻转、倾斜等操作。当前选择的变换类型：${settings.transform_type}。

本接口提供专业的图片变换功能，可以精确控制图片的几何变换。支持以下变换类型：
• 旋转：任意角度旋转图片
• 翻转：水平或垂直翻转图片
• 倾斜：水平或垂直方向倾斜图片

参数：
- image: File (必需)
- transform_type: string (必需) - 可选值: rotate, flip, skew
- angle: number (可选) - 旋转角度，范围：-360 到 360
- flip_direction: string (可选) - 翻转方向，可选值：horizontal, vertical, both
- skew_x: number (可选) - 水平倾斜角度，范围：-89 到 89
- skew_y: number (可选) - 垂直倾斜角度，范围：-89 到 89
- quality: number (可选) - 输出质量，范围：10 到 100，默认：90`
        }}
        settings={settings}
      />
    </Box>
  );
}; 