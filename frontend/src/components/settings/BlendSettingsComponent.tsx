import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
  Box,
  Button,
  Alert,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

interface BlendSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const BlendSettingsComponent: React.FC<BlendSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [blendMode, setBlendMode] = useState('normal');
  const [opacity, setOpacity] = useState(0.5);
  const [position, setPosition] = useState('center');
  const [xOffset, setXOffset] = useState(0);
  const [yOffset, setYOffset] = useState(0);
  const [scale, setScale] = useState(1.0);
  const [overlayFile, setOverlayFile] = useState<File | null>(null);
  const [overlayUrl, setOverlayUrl] = useState<string>('');
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      blend_mode: blendMode,
      opacity: opacity,
      position: position,
      scale: scale,
      quality: quality,
    };

    if (position === 'custom') {
      settings.x_offset = xOffset;
      settings.y_offset = yOffset;
    }

    if (overlayFile) {
      settings.overlay_file = overlayFile;
    } else if (overlayUrl) {
      settings.overlay_url = overlayUrl;
    }

    onSettingsChange(settings);
  }, [blendMode, opacity, position, xOffset, yOffset, scale, overlayFile, overlayUrl, quality, onSettingsChange]);

  const handleOverlayFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setOverlayFile(event.target.files[0]);
      setOverlayUrl('');
    }
  };

  return (
    <Box>
      <Alert severity="info" sx={{ mb: 3 }}>
        混合功能需要两张图片：基础图片和叠加图片
      </Alert>

      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1" gutterBottom>
          选择叠加图片
        </Typography>
        <Button
          variant="outlined"
          component="label"
          startIcon={<CloudUploadIcon />}
          fullWidth
          sx={{ mb: 2 }}
        >
          上传叠加图片
          <input
            type="file"
            hidden
            accept="image/*"
            onChange={handleOverlayFileSelect}
            disabled={isLoading}
          />
        </Button>
        {overlayFile && (
          <Typography variant="body2" color="text.secondary">
            已选择: {overlayFile.name}
          </Typography>
        )}
      </Box>

      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>混合模式</InputLabel>
        <Select
          value={blendMode}
          label="混合模式"
          onChange={(e) => setBlendMode(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="normal">正常</MenuItem>
          <MenuItem value="multiply">正片叠底</MenuItem>
          <MenuItem value="screen">滤色</MenuItem>
          <MenuItem value="overlay">叠加</MenuItem>
          <MenuItem value="soft_light">柔光</MenuItem>
          <MenuItem value="hard_light">强光</MenuItem>
          <MenuItem value="color_dodge">颜色减淡</MenuItem>
          <MenuItem value="color_burn">颜色加深</MenuItem>
          <MenuItem value="darken">变暗</MenuItem>
          <MenuItem value="lighten">变亮</MenuItem>
          <MenuItem value="difference">差值</MenuItem>
          <MenuItem value="exclusion">排除</MenuItem>
        </Select>
      </FormControl>

      <Typography gutterBottom>不透明度: {(opacity * 100).toFixed(0)}%</Typography>
      <Slider
        value={opacity}
        min={0}
        max={1}
        step={0.05}
        onChange={(_, value) => setOpacity(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>位置</InputLabel>
        <Select
          value={position}
          label="位置"
          onChange={(e) => setPosition(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="center">居中</MenuItem>
          <MenuItem value="top-left">左上</MenuItem>
          <MenuItem value="top-right">右上</MenuItem>
          <MenuItem value="bottom-left">左下</MenuItem>
          <MenuItem value="bottom-right">右下</MenuItem>
          <MenuItem value="custom">自定义</MenuItem>
        </Select>
      </FormControl>

      {position === 'custom' && (
        <>
          <Typography gutterBottom>X偏移: {xOffset}px</Typography>
          <Slider
            value={xOffset}
            min={-500}
            max={500}
            onChange={(_, value) => setXOffset(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            sx={{ mb: 2 }}
          />

          <Typography gutterBottom>Y偏移: {yOffset}px</Typography>
          <Slider
            value={yOffset}
            min={-500}
            max={500}
            onChange={(_, value) => setYOffset(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            sx={{ mb: 3 }}
          />
        </>
      )}

      <Typography gutterBottom>缩放: {(scale * 100).toFixed(0)}%</Typography>
      <Slider
        value={scale}
        min={0.1}
        max={3}
        step={0.1}
        onChange={(_, value) => setScale(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        marks={[
          { value: 0.1, label: '10%' },
          { value: 1, label: '100%' },
          { value: 3, label: '300%' },
        ]}
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

export default BlendSettingsComponent; 