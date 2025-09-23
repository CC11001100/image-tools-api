import React, { useState } from 'react';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import { artFilterExamples } from '../config/examples/artFilterExamples';
import { FilterOption } from '../types/api';

const ArtFilterPage: React.FC = () => {
  const [settings, setSettings] = useState({
    filter_type: 'oil_painting',
    intensity: 50,
    quality: 90
  });

  const filterOptions: FilterOption[] = [
    {
      value: 'oil_painting',
      label: '油画',
      description: '将图片转换为油画风格',
      category: 'artistic'
    },
    {
      value: 'watercolor',
      label: '水彩',
      description: '将图片转换为水彩画风格',
      category: 'artistic'
    },
    {
      value: 'pencil_sketch',
      label: '铅笔素描',
      description: '将图片转换为铅笔素描风格',
      category: 'artistic'
    },
    {
      value: 'colored_pencil',
      label: '彩色铅笔',
      description: '将图片转换为彩色铅笔画风格',
      category: 'artistic'
    }
  ];

  return (
    <ImageToolTabLayout
      title="艺术滤镜"
      description="为图片添加艺术效果，支持多种艺术风格"
      endpoint={{
        method: 'POST',
        path: '/api/v1/art-filter',
        urlPath: '/api/v1/art-filter-by-url',
        category: '艺术滤镜',
        description: '为图片添加艺术效果',
        requestType: {
          file: 'multipart/form-data',
          url: 'application/json'
        },
        responseType: 'image/*',
        parameters: [
          {
            name: 'filter_type',
            type: 'select',
            required: true,
            description: '滤镜类型',
            options: filterOptions.map(opt => opt.value)
          },
          {
            name: 'intensity',
            type: 'number',
            required: false,
            description: '效果强度',
            min: 0,
            max: 100,
            defaultValue: 50
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
      effectExamples={artFilterExamples}
      downloadFileName="art-filter-result.jpg"
      enableLargeDisplay={true}
    />
  );
};

export default ArtFilterPage; 