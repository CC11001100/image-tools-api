import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
  Box,
  TextField,
  Switch,
  FormControlLabel,
} from '@mui/material';

interface TransformSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const TransformSettingsComponent: React.FC<TransformSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [transformType, setTransformType] = useState('rotate');
  const [angle, setAngle] = useState(0);
  const [expand, setExpand] = useState(true);
  const [fillColor, setFillColor] = useState('#ffffff');
  const [quality, setQuality] = useState(90);

  const transformOptions = [
    { value: 'rotate', label: '自定义旋转' },
    { value: 'flip-horizontal', label: '水平翻转' },
    { value: 'flip-vertical', label: '垂直翻转' },
    { value: 'rotate-90-cw', label: '顺时针旋转90°' },
    { value: 'rotate-90-ccw', label: '逆时针旋转90°' },
    { value: 'rotate-180', label: '旋转180°' },
  ];

  useEffect(() => {
    const settings: any = {
      transform_type: transformType,
      quality: quality,
    };

    if (transformType === 'rotate') {
      settings.angle = angle;
      settings.expand = expand;
      settings.fill_color = fillColor;
    }

    onSettingsChange(settings);
  }, [transformType, angle, expand, fillColor, quality, onSettingsChange]);

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>变换类型</InputLabel>
        <Select
          value={transformType}
          label="变换类型"
          onChange={(e) => setTransformType(e.target.value)}
          disabled={isLoading}
        >
          {transformOptions.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {transformType === 'rotate' && (
        <>
          <Typography gutterBottom>旋转角度: {angle}°</Typography>
          <Slider
            value={angle}
            min={-180}
            max={180}
            step={1}
            onChange={(_, value) => setAngle(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            marks={[
              { value: -180, label: '-180°' },
              { value: -90, label: '-90°' },
              { value: 0, label: '0°' },
              { value: 90, label: '90°' },
              { value: 180, label: '180°' },
            ]}
            sx={{ mb: 2 }}
          />
          
          <FormControlLabel
            control={
              <Switch
                checked={expand}
                onChange={(e) => setExpand(e.target.checked)}
                disabled={isLoading}
              />
            }
            label="扩展画布（避免裁剪）"
            sx={{ mb: 2 }}
          />
          
          <TextField
            fullWidth
            label="填充颜色"
            type="color"
            value={fillColor}
            onChange={(e) => setFillColor(e.target.value)}
            disabled={isLoading}
            sx={{ mb: 2 }}
            helperText="当不扩展画布时的背景填充颜色"
          />
        </>
      )}

      <Typography gutterBottom>图片质量: {quality}%</Typography>
      <Slider
        value={quality}
        min={10}
        max={100}
        step={5}
        onChange={(_, value) => setQuality(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
      />
    </Box>
  );
};

export default TransformSettingsComponent; 