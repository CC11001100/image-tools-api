import React, { useState } from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import { canvasExamples } from '../config/examples/canvasExamples';

const CanvasPage: React.FC = () => {
  const [settings, setSettings] = useState({
    canvas_type: 'border',
    background_color: '#FFFFFF',
    border_width: 2,
    border_color: '#000000',
    padding: 0,
    quality: 90
  });

  return (
    <ImageToolTabLayout
      title="画布处理"
      description="为图片添加边框、背景等画布效果"
      endpoint={{
        method: 'POST',
        path: '/api/v1/canvas',
        urlPath: '/api/v1/canvas-by-url',
        category: '画布处理',
        description: '为图片添加边框、背景等画布效果',
        requestType: {
          file: 'multipart/form-data',
          url: 'application/json'
        },
        responseType: 'image/*',
        parameters: [
          {
            name: 'canvas_type',
            type: 'select',
            required: true,
            description: '画布类型',
            options: ['border', 'padding', 'expand'],
            defaultValue: 'border'
          },
          {
            name: 'background_color',
            type: 'color',
            required: false,
            description: '背景颜色',
            defaultValue: '#FFFFFF'
          },
          {
            name: 'border_width',
            type: 'number',
            required: false,
            description: '边框宽度',
            min: 0,
            max: 100,
            defaultValue: 2
          },
          {
            name: 'border_color',
            type: 'color',
            required: false,
            description: '边框颜色',
            defaultValue: '#000000'
          },
          {
            name: 'padding',
            type: 'number',
            required: false,
            description: '内边距',
            min: 0,
            max: 100,
            defaultValue: 0
          },
          {
            name: 'quality',
            type: 'number',
            required: false,
            description: '输出质量',
            min: 1,
            max: 100,
            defaultValue: 90
          }
        ]
      }}
      settings={settings}
      onSettingsChange={setSettings}
      effectExamples={canvasExamples}
      downloadFileName="canvas-result.jpg"
      enableLargeDisplay={true}
    />
  );
};

export default CanvasPage; 