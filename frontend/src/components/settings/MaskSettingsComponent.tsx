import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
  Box,
  FormControlLabel,
  Checkbox,
} from '@mui/material';

interface MaskSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const MaskSettingsComponent: React.FC<MaskSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [maskType, setMaskType] = useState('circle');
  const [radius, setRadius] = useState(100);
  const [centerX, setCenterX] = useState(50);
  const [centerY, setCenterY] = useState(50);
  const [width, setWidth] = useState(200);
  const [height, setHeight] = useState(200);
  const [borderRadius, setBorderRadius] = useState(0);
  const [feather, setFeather] = useState(0);
  const [invert, setInvert] = useState(false);
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      mask_type: maskType,
      feather: feather,
      invert: invert,
      quality: quality,
    };

    switch (maskType) {
      case 'circle':
        settings.radius = radius;
        settings.center_x = centerX;
        settings.center_y = centerY;
        break;
      case 'rectangle':
        settings.x = centerX - width / 2;
        settings.y = centerY - height / 2;
        settings.width = width;
        settings.height = height;
        settings.border_radius = borderRadius;
        break;
      case 'ellipse':
        settings.center_x = centerX;
        settings.center_y = centerY;
        settings.width = width;
        settings.height = height;
        break;
    }

    onSettingsChange(settings);
  }, [maskType, radius, centerX, centerY, width, height, borderRadius, feather, invert, quality, onSettingsChange]);

  const renderCircleSettings = () => (
    <>
      <Typography gutterBottom>半径: {radius}px</Typography>
      <Slider
        value={radius}
        min={10}
        max={500}
        onChange={(_, value) => setRadius(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <Typography gutterBottom>中心X: {centerX}%</Typography>
      <Slider
        value={centerX}
        min={0}
        max={100}
        onChange={(_, value) => setCenterX(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>中心Y: {centerY}%</Typography>
      <Slider
        value={centerY}
        min={0}
        max={100}
        onChange={(_, value) => setCenterY(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );

  const renderRectangleSettings = () => (
    <>
      <Typography gutterBottom>宽度: {width}px</Typography>
      <Slider
        value={width}
        min={10}
        max={1000}
        onChange={(_, value) => setWidth(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>高度: {height}px</Typography>
      <Slider
        value={height}
        min={10}
        max={1000}
        onChange={(_, value) => setHeight(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>中心X: {centerX}%</Typography>
      <Slider
        value={centerX}
        min={0}
        max={100}
        onChange={(_, value) => setCenterX(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>中心Y: {centerY}%</Typography>
      <Slider
        value={centerY}
        min={0}
        max={100}
        onChange={(_, value) => setCenterY(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>圆角: {borderRadius}px</Typography>
      <Slider
        value={borderRadius}
        min={0}
        max={Math.min(width, height) / 2}
        onChange={(_, value) => setBorderRadius(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );

  const renderEllipseSettings = () => (
    <>
      <Typography gutterBottom>宽度: {width}px</Typography>
      <Slider
        value={width}
        min={10}
        max={1000}
        onChange={(_, value) => setWidth(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>高度: {height}px</Typography>
      <Slider
        value={height}
        min={10}
        max={1000}
        onChange={(_, value) => setHeight(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>中心X: {centerX}%</Typography>
      <Slider
        value={centerX}
        min={0}
        max={100}
        onChange={(_, value) => setCenterX(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>中心Y: {centerY}%</Typography>
      <Slider
        value={centerY}
        min={0}
        max={100}
        onChange={(_, value) => setCenterY(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>遮罩形状</InputLabel>
        <Select
          value={maskType}
          label="遮罩形状"
          onChange={(e) => setMaskType(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="circle">圆形</MenuItem>
          <MenuItem value="rectangle">矩形</MenuItem>
          <MenuItem value="ellipse">椭圆</MenuItem>
        </Select>
      </FormControl>

      {maskType === 'circle' && renderCircleSettings()}
      {maskType === 'rectangle' && renderRectangleSettings()}
      {maskType === 'ellipse' && renderEllipseSettings()}

      <Typography gutterBottom>羽化: {feather}px</Typography>
      <Slider
        value={feather}
        min={0}
        max={100}
        onChange={(_, value) => setFeather(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <FormControlLabel
        control={
          <Checkbox
            checked={invert}
            onChange={(e) => setInvert(e.target.checked)}
            disabled={isLoading}
          />
        }
        label="反转遮罩"
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

export default MaskSettingsComponent; 