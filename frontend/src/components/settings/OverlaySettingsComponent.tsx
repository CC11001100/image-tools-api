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
} from '@mui/material';

interface OverlaySettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const OverlaySettingsComponent: React.FC<OverlaySettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [overlayType, setOverlayType] = useState('gradient');
  const [gradientType, setGradientType] = useState('linear');
  const [gradientDirection, setGradientDirection] = useState('to_bottom');
  const [startColor, setStartColor] = useState('#000000');
  const [endColor, setEndColor] = useState('#FFFFFF');
  const [startOpacity, setStartOpacity] = useState(0.0);
  const [endOpacity, setEndOpacity] = useState(0.8);
  const [vignetteIntensity, setVignetteIntensity] = useState(0.5);
  const [vignetteRadius, setVignetteRadius] = useState(0.8);
  const [patternType, setPatternType] = useState('dots');
  const [patternSize, setPatternSize] = useState(10);
  const [patternOpacity, setPatternOpacity] = useState(0.3);
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      overlay_type: overlayType,
      quality: quality,
    };

    switch (overlayType) {
      case 'gradient':
        settings.gradient_type = gradientType;
        settings.gradient_direction = gradientDirection;
        settings.start_color = startColor;
        settings.end_color = endColor;
        settings.start_opacity = startOpacity;
        settings.end_opacity = endOpacity;
        break;
      case 'vignette':
        settings.intensity = vignetteIntensity;
        settings.radius = vignetteRadius;
        break;
      case 'pattern':
        settings.pattern_type = patternType;
        settings.pattern_size = patternSize;
        settings.pattern_opacity = patternOpacity;
        break;
    }

    onSettingsChange(settings);
  }, [overlayType, gradientType, gradientDirection, startColor, endColor, startOpacity, endOpacity,
      vignetteIntensity, vignetteRadius, patternType, patternSize, patternOpacity, quality, onSettingsChange]);

  const renderGradientSettings = () => (
    <>
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>渐变类型</InputLabel>
        <Select
          value={gradientType}
          label="渐变类型"
          onChange={(e) => setGradientType(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="linear">线性渐变</MenuItem>
          <MenuItem value="radial">径向渐变</MenuItem>
        </Select>
      </FormControl>

      {gradientType === 'linear' && (
        <FormControl fullWidth sx={{ mb: 3 }}>
          <InputLabel>渐变方向</InputLabel>
          <Select
            value={gradientDirection}
            label="渐变方向"
            onChange={(e) => setGradientDirection(e.target.value)}
            disabled={isLoading}
          >
            <MenuItem value="to_bottom">从上到下</MenuItem>
            <MenuItem value="to_top">从下到上</MenuItem>
            <MenuItem value="to_right">从左到右</MenuItem>
            <MenuItem value="to_left">从右到左</MenuItem>
            <MenuItem value="to_bottom_right">左上到右下</MenuItem>
            <MenuItem value="to_bottom_left">右上到左下</MenuItem>
          </Select>
        </FormControl>
      )}

      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <TextField
          fullWidth
          label="起始颜色"
          type="color"
          value={startColor}
          onChange={(e) => setStartColor(e.target.value)}
          disabled={isLoading}
        />
        <TextField
          fullWidth
          label="结束颜色"
          type="color"
          value={endColor}
          onChange={(e) => setEndColor(e.target.value)}
          disabled={isLoading}
        />
      </Box>

      <Typography gutterBottom>起始不透明度: {(startOpacity * 100).toFixed(0)}%</Typography>
      <Slider
        value={startOpacity}
        min={0}
        max={1}
        step={0.1}
        onChange={(_, value) => setStartOpacity(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Typography gutterBottom>结束不透明度: {(endOpacity * 100).toFixed(0)}%</Typography>
      <Slider
        value={endOpacity}
        min={0}
        max={1}
        step={0.1}
        onChange={(_, value) => setEndOpacity(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );

  const renderVignetteSettings = () => (
    <>
      <Typography gutterBottom>暗角强度: {(vignetteIntensity * 100).toFixed(0)}%</Typography>
      <Slider
        value={vignetteIntensity}
        min={0}
        max={1}
        step={0.05}
        onChange={(_, value) => setVignetteIntensity(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <Typography gutterBottom>暗角半径: {(vignetteRadius * 100).toFixed(0)}%</Typography>
      <Slider
        value={vignetteRadius}
        min={0.1}
        max={1.5}
        step={0.05}
        onChange={(_, value) => setVignetteRadius(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );

  const renderPatternSettings = () => (
    <>
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>图案类型</InputLabel>
        <Select
          value={patternType}
          label="图案类型"
          onChange={(e) => setPatternType(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="dots">圆点</MenuItem>
          <MenuItem value="lines">线条</MenuItem>
          <MenuItem value="grid">网格</MenuItem>
          <MenuItem value="diagonal">斜线</MenuItem>
        </Select>
      </FormControl>

      <Typography gutterBottom>图案大小: {patternSize}px</Typography>
      <Slider
        value={patternSize}
        min={5}
        max={50}
        onChange={(_, value) => setPatternSize(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <Typography gutterBottom>图案不透明度: {(patternOpacity * 100).toFixed(0)}%</Typography>
      <Slider
        value={patternOpacity}
        min={0}
        max={1}
        step={0.05}
        onChange={(_, value) => setPatternOpacity(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>叠加类型</InputLabel>
        <Select
          value={overlayType}
          label="叠加类型"
          onChange={(e) => setOverlayType(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="gradient">渐变叠加</MenuItem>
          <MenuItem value="vignette">暗角效果</MenuItem>
          <MenuItem value="pattern">图案叠加</MenuItem>
        </Select>
      </FormControl>

      {overlayType === 'gradient' && renderGradientSettings()}
      {overlayType === 'vignette' && renderVignetteSettings()}
      {overlayType === 'pattern' && renderPatternSettings()}

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

export default OverlaySettingsComponent; 