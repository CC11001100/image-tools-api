import React from 'react';
import {
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
} from '@mui/material';
import { blendModes } from '../../config/endpoints/blendEndpoint';

interface BlendSettingsProps {
  blendMode: string;
  opacity: number;
  quality: number;
  isLoading: boolean;
  onBlendModeChange: (mode: string) => void;
  onOpacityChange: (opacity: number) => void;
  onQualityChange: (quality: number) => void;
}

export const BlendSettings: React.FC<BlendSettingsProps> = ({
  blendMode,
  opacity,
  quality,
  isLoading,
  onBlendModeChange,
  onOpacityChange,
  onQualityChange,
}) => {
  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        混合设置
      </Typography>
      
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>混合模式</InputLabel>
        <Select
          value={blendMode}
          label="混合模式"
          onChange={(e) => onBlendModeChange(e.target.value)}
          disabled={isLoading}
        >
          {blendModes.map((mode) => (
            <MenuItem key={mode.value} value={mode.value}>
              {mode.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Typography gutterBottom>不透明度: {(opacity * 100).toFixed(0)}%</Typography>
      <Slider
        value={opacity}
        min={0}
        max={1}
        step={0.05}
        onChange={(_, value) => onOpacityChange(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <Typography gutterBottom>输出质量: {quality}%</Typography>
      <Slider
        value={quality}
        min={10}
        max={100}
        step={5}
        onChange={(_, value) => onQualityChange(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </Paper>
  );
}; 