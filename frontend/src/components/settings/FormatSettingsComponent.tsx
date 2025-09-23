import React, { useState, useEffect } from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Switch,
  FormControlLabel,
  Typography,
} from '@mui/material';

interface FormatSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const FormatSettingsComponent: React.FC<FormatSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [targetFormat, setTargetFormat] = useState('jpeg');
  const [quality, setQuality] = useState(90);
  const [optimize, setOptimize] = useState(true);
  const [compressLevel, setCompressLevel] = useState(6);
  const [lossless, setLossless] = useState(false);

  useEffect(() => {
    onSettingsChange({
      target_format: targetFormat,
      quality,
      optimize,
      compress_level: compressLevel,
      lossless,
    });
  }, [targetFormat, quality, optimize, compressLevel, lossless, onSettingsChange]);

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>目标格式</InputLabel>
        <Select
          value={targetFormat}
          label="目标格式"
          onChange={(e) => setTargetFormat(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="jpeg">JPEG</MenuItem>
          <MenuItem value="png">PNG</MenuItem>
          <MenuItem value="webp">WebP</MenuItem>
          <MenuItem value="bmp">BMP</MenuItem>
          <MenuItem value="tiff">TIFF</MenuItem>
        </Select>
      </FormControl>

      {(targetFormat === 'jpeg' || targetFormat === 'webp') && (
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom>质量: {quality}%</Typography>
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
      )}

      {targetFormat === 'png' && (
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom>压缩级别: {compressLevel}</Typography>
          <Slider
            value={compressLevel}
            min={0}
            max={9}
            step={1}
            onChange={(_, value) => setCompressLevel(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            marks={[
              { value: 0, label: '0' },
              { value: 6, label: '6' },
              { value: 9, label: '9' },
            ]}
          />
        </Box>
      )}

      {targetFormat === 'webp' && (
        <FormControlLabel
          control={
            <Switch
              checked={lossless}
              onChange={(e) => setLossless(e.target.checked)}
              disabled={isLoading}
            />
          }
          label="无损压缩"
          sx={{ mb: 2 }}
        />
      )}

      <FormControlLabel
        control={
          <Switch
            checked={optimize}
            onChange={(e) => setOptimize(e.target.checked)}
            disabled={isLoading}
          />
        }
        label="优化文件大小"
      />
    </Box>
  );
};

export default FormatSettingsComponent; 