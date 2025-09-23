/**
 * 效果设置组件
 */

import React from 'react';
import {
  Slider,
  Typography,
} from '@mui/material';

import { EffectSettingsProps } from './types';

const EffectSettings: React.FC<EffectSettingsProps> = ({
  isLoading,
  opacity,
  setOpacity,
  quality,
  setQuality,
}) => {
  return (
    <>
      <Typography variant="subtitle1" gutterBottom sx={{ mt: 3 }}>
        其他设置
      </Typography>

      <Typography gutterBottom>不透明度: {(opacity * 100).toFixed(0)}%</Typography>
      <Slider
        value={opacity}
        min={0}
        max={1}
        step={0.1}
        onChange={(_, value) => setOpacity(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>输出质量: {quality}%</Typography>
      <Slider
        value={quality}
        min={10}
        max={100}
        step={5}
        onChange={(_, value) => setQuality(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
      />
    </>
  );
};

export default EffectSettings;
