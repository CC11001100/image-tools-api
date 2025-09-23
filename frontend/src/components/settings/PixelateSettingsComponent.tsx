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
  FormControlLabel,
  Checkbox,
} from '@mui/material';

interface PixelateSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const PixelateSettingsComponent: React.FC<PixelateSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [pixelateType, setPixelateType] = useState('standard');
  const [pixelSize, setPixelSize] = useState(10);
  const [preserveEdges, setPreserveEdges] = useState(false);
  const [edgeThreshold, setEdgeThreshold] = useState(30);
  const [region, setRegion] = useState('');
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      pixelate_type: pixelateType,
      pixel_size: pixelSize,
      quality: quality,
    };

    if (pixelateType === 'adaptive') {
      settings.preserve_edges = preserveEdges;
      settings.edge_threshold = edgeThreshold;
    }

    if (pixelateType === 'region' && region) {
      settings.region = region;
    }

    onSettingsChange(settings);
  }, [pixelateType, pixelSize, preserveEdges, edgeThreshold, region, quality, onSettingsChange]);

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>像素化类型</InputLabel>
        <Select
          value={pixelateType}
          label="像素化类型"
          onChange={(e) => setPixelateType(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="standard">标准像素化</MenuItem>
          <MenuItem value="adaptive">自适应像素化</MenuItem>
          <MenuItem value="region">区域像素化</MenuItem>
        </Select>
      </FormControl>

      <Typography gutterBottom>像素大小: {pixelSize}px</Typography>
      <Slider
        value={pixelSize}
        min={2}
        max={100}
        onChange={(_, value) => setPixelSize(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        marks={[
          { value: 2, label: '2px' },
          { value: 50, label: '50px' },
          { value: 100, label: '100px' },
        ]}
        sx={{ mb: 3 }}
      />

      {pixelateType === 'adaptive' && (
        <>
          <FormControlLabel
            control={
              <Checkbox
                checked={preserveEdges}
                onChange={(e) => setPreserveEdges(e.target.checked)}
                disabled={isLoading}
              />
            }
            label="保留边缘"
            sx={{ mb: 2 }}
          />

          {preserveEdges && (
            <>
              <Typography gutterBottom>边缘阈值: {edgeThreshold}</Typography>
              <Slider
                value={edgeThreshold}
                min={10}
                max={100}
                onChange={(_, value) => setEdgeThreshold(value as number)}
                valueLabelDisplay="auto"
                disabled={isLoading}
                sx={{ mb: 3 }}
              />
            </>
          )}
        </>
      )}

      {pixelateType === 'region' && (
        <TextField
          fullWidth
          label="区域定义"
          placeholder="x,y,width,height (例如: 100,100,200,200)"
          value={region}
          onChange={(e) => setRegion(e.target.value)}
          disabled={isLoading}
          helperText="指定要像素化的矩形区域，格式：x,y,宽度,高度"
          sx={{ mb: 3 }}
        />
      )}

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

export default PixelateSettingsComponent; 