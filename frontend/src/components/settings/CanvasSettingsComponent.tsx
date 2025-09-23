import React, { useState, useEffect } from 'react';
import {
  TextField,
  Slider,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
} from '@mui/material';

interface CanvasSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const CanvasSettingsComponent: React.FC<CanvasSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [canvasWidth, setCanvasWidth] = useState(800);
  const [canvasHeight, setCanvasHeight] = useState(600);
  const [backgroundColor, setBackgroundColor] = useState('#FFFFFF');
  const [backgroundOpacity, setBackgroundOpacity] = useState(1.0);
  const [padding, setPadding] = useState(50);
  const [position, setPosition] = useState('center');
  const [maintainAspectRatio, setMaintainAspectRatio] = useState(true);
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      canvas_width: canvasWidth,
      canvas_height: canvasHeight,
      background_color: backgroundColor,
      background_opacity: backgroundOpacity,
      padding: padding,
      position: position,
      maintain_aspect_ratio: maintainAspectRatio,
      quality: quality,
    };

    onSettingsChange(settings);
  }, [canvasWidth, canvasHeight, backgroundColor, backgroundOpacity, padding, position, maintainAspectRatio, quality, onSettingsChange]);

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom>
        画布尺寸
      </Typography>
      
      <TextField
        fullWidth
        label="画布宽度"
        type="number"
        value={canvasWidth}
        onChange={(e) => setCanvasWidth(parseInt(e.target.value) || 800)}
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <TextField
        fullWidth
        label="画布高度"
        type="number"
        value={canvasHeight}
        onChange={(e) => setCanvasHeight(parseInt(e.target.value) || 600)}
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <Typography variant="subtitle1" gutterBottom>
        背景设置
      </Typography>

      <TextField
        fullWidth
        label="背景颜色"
        type="color"
        value={backgroundColor}
        onChange={(e) => setBackgroundColor(e.target.value)}
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>背景不透明度: {(backgroundOpacity * 100).toFixed(0)}%</Typography>
      <Slider
        value={backgroundOpacity}
        min={0}
        max={1}
        step={0.1}
        onChange={(_, value) => setBackgroundOpacity(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <Typography gutterBottom>内边距: {padding}px</Typography>
      <Slider
        value={padding}
        min={0}
        max={200}
        onChange={(_, value) => setPadding(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        marks={[
          { value: 0, label: '0px' },
          { value: 100, label: '100px' },
          { value: 200, label: '200px' },
        ]}
        sx={{ mb: 3 }}
      />

      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>图片位置</InputLabel>
        <Select
          value={position}
          label="图片位置"
          onChange={(e) => setPosition(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="center">居中</MenuItem>
          <MenuItem value="top-left">左上</MenuItem>
          <MenuItem value="top-center">上中</MenuItem>
          <MenuItem value="top-right">右上</MenuItem>
          <MenuItem value="middle-left">左中</MenuItem>
          <MenuItem value="middle-right">右中</MenuItem>
          <MenuItem value="bottom-left">左下</MenuItem>
          <MenuItem value="bottom-center">下中</MenuItem>
          <MenuItem value="bottom-right">右下</MenuItem>
        </Select>
      </FormControl>

      <FormControlLabel
        control={
          <Checkbox
            checked={maintainAspectRatio}
            onChange={(e) => setMaintainAspectRatio(e.target.checked)}
            disabled={isLoading}
          />
        }
        label="保持宽高比"
        sx={{ mb: 3 }}
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
    </Box>
  );
};

export default CanvasSettingsComponent; 