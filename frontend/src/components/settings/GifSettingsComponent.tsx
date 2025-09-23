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

interface GifSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const GifSettingsComponent: React.FC<GifSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [operation, setOperation] = useState('extract');
  const [frameNumber, setFrameNumber] = useState(0);
  const [duration, setDuration] = useState(100);
  const [loop, setLoop] = useState(0);
  const [optimize, setOptimize] = useState(true);
  const [quality, setQuality] = useState(90);
  const [resizeWidth, setResizeWidth] = useState<number | ''>('');
  const [resizeHeight, setResizeHeight] = useState<number | ''>('');

  useEffect(() => {
    const settings: any = {
      operation: operation,
      quality: quality,
    };

    switch (operation) {
      case 'extract':
        settings.frame_number = frameNumber;
        break;
      case 'create':
        settings.duration = duration;
        settings.loop = loop;
        settings.optimize = optimize;
        if (resizeWidth) settings.resize_width = resizeWidth;
        if (resizeHeight) settings.resize_height = resizeHeight;
        break;
      case 'optimize':
        settings.optimize = optimize;
        if (resizeWidth) settings.resize_width = resizeWidth;
        if (resizeHeight) settings.resize_height = resizeHeight;
        break;
    }

    onSettingsChange(settings);
  }, [operation, frameNumber, duration, loop, optimize, quality, resizeWidth, resizeHeight, onSettingsChange]);

  const renderExtractSettings = () => (
    <>
      <Typography gutterBottom>提取帧号: {frameNumber}</Typography>
      <Slider
        value={frameNumber}
        min={0}
        max={100}
        onChange={(_, value) => setFrameNumber(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );

  const renderCreateSettings = () => (
    <>
      <Typography gutterBottom>帧持续时间: {duration}ms</Typography>
      <Slider
        value={duration}
        min={20}
        max={1000}
        step={10}
        onChange={(_, value) => setDuration(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        marks={[
          { value: 20, label: '20ms' },
          { value: 500, label: '500ms' },
          { value: 1000, label: '1s' },
        ]}
        sx={{ mb: 3 }}
      />

      <Typography gutterBottom>循环次数: {loop === 0 ? '无限' : loop}</Typography>
      <Slider
        value={loop}
        min={0}
        max={10}
        onChange={(_, value) => setLoop(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        marks={[
          { value: 0, label: '无限' },
          { value: 5, label: '5次' },
          { value: 10, label: '10次' },
        ]}
        sx={{ mb: 3 }}
      />
    </>
  );

  const renderOptimizeSettings = () => (
    <>
      <FormControlLabel
        control={
          <Checkbox
            checked={optimize}
            onChange={(e) => setOptimize(e.target.checked)}
            disabled={isLoading}
          />
        }
        label="优化文件大小"
        sx={{ mb: 3 }}
      />

      <TextField
        fullWidth
        label="调整宽度（可选）"
        type="number"
        value={resizeWidth}
        onChange={(e) => setResizeWidth(e.target.value ? parseInt(e.target.value) : '')}
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <TextField
        fullWidth
        label="调整高度（可选）"
        type="number"
        value={resizeHeight}
        onChange={(e) => setResizeHeight(e.target.value ? parseInt(e.target.value) : '')}
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>操作类型</InputLabel>
        <Select
          value={operation}
          label="操作类型"
          onChange={(e) => setOperation(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="extract">提取帧</MenuItem>
          <MenuItem value="create">创建GIF</MenuItem>
          <MenuItem value="optimize">优化GIF</MenuItem>
        </Select>
      </FormControl>

      {operation === 'extract' && renderExtractSettings()}
      {operation === 'create' && (
        <>
          {renderCreateSettings()}
          {renderOptimizeSettings()}
        </>
      )}
      {operation === 'optimize' && renderOptimizeSettings()}

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

export default GifSettingsComponent; 