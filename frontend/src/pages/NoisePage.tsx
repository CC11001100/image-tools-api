import React, { useState } from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import { NoiseSettings } from '../types/settings';
import { ApiEndpoint } from '../types/api';
import { noiseExamples } from '../config/examples/noiseExamples';

const NoisePage: React.FC = () => {
  const [settings, setSettings] = useState<NoiseSettings>({
    noise_type: 'gaussian',
    intensity: 50,
    quality: 90
  });

  const endpoint: ApiEndpoint = {
    method: 'POST',
    path: '/api/v1/noise',
    urlPath: '/api/v1/noise-by-url',
    category: '图像噪点',
    description: '为图像添加或去除噪点效果',
    requestType: {
      file: 'multipart/form-data',
      url: 'application/json'
    },
    responseType: 'image/*',
    parameters: [
      {
        name: 'noise_type',
        type: 'select',
        required: true,
        description: '噪点类型',
        options: ['gaussian', 'salt_and_pepper', 'poisson', 'speckle']
      },
      {
        name: 'intensity',
        type: 'number',
        required: false,
        description: '噪点强度',
        min: 0,
        max: 100,
        defaultValue: 50
      },
      {
        name: 'quality',
        type: 'number',
        required: false,
        description: '输出图片质量',
        min: 1,
        max: 100,
        defaultValue: 90
      }
    ]
  };

  return (
    <ImageToolTabLayout
      title="图像噪点"
      description="为图像添加或去除噪点效果，支持多种噪点类型和强度调整"
      endpoint={endpoint}
      settings={settings}
      onSettingsChange={setSettings}
      effectExamples={noiseExamples}
    />
  );
};

export default NoisePage; 