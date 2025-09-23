import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Slider,
  Typography,
  Button,
} from '@mui/material';

interface PerspectiveSettings {
  points: string;
  outputWidth: number;
  outputHeight: number;
  quality: number;
  auto_document: boolean;
}

interface PerspectiveSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
  [key: string]: any;
}

const PerspectiveSettingsComponent: React.FC<PerspectiveSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [points, setPoints] = useState('[[50,50],[350,80],[320,280],[20,250]]');
  const [outputWidth, setOutputWidth] = useState(400);
  const [outputHeight, setOutputHeight] = useState(300);
  const [quality, setQuality] = useState(90);
  const [useAutoDocument, setUseAutoDocument] = useState(false);

  // 初始化设置
  useEffect(() => {
    const initialSettings = {
      points,
      outputWidth,
      outputHeight,
      quality,
      auto_document: useAutoDocument,
    };
    onSettingsChange(initialSettings);
  }, []); // 只在组件挂载时执行一次

  const updateSettings = (newSettings: Partial<PerspectiveSettings>) => {
    const settings = {
      points,
      outputWidth,
      outputHeight,
      quality,
      auto_document: useAutoDocument,
      ...newSettings,
    };
    onSettingsChange(settings);
  };

  const handlePointsChange = (value: string) => {
    setPoints(value);
    updateSettings({ points: value });
  };

  const handleOutputWidthChange = (value: number) => {
    setOutputWidth(value);
    updateSettings({ outputWidth: value });
  };

  const handleOutputHeightChange = (value: number) => {
    setOutputHeight(value);
    updateSettings({ outputHeight: value });
  };

  const handleQualityChange = (value: number) => {
    setQuality(value);
    updateSettings({ quality: value });
  };

  const handleModeChange = (autoMode: boolean) => {
    setUseAutoDocument(autoMode);
    updateSettings({ auto_document: autoMode });
  };

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Button
          variant={useAutoDocument ? "outlined" : "contained"}
          onClick={() => handleModeChange(false)}
          sx={{ mr: 1 }}
          disabled={isLoading}
        >
          手动四点校正
        </Button>
        <Button
          variant={useAutoDocument ? "contained" : "outlined"}
          onClick={() => handleModeChange(true)}
          disabled={isLoading}
        >
          自动文档检测
        </Button>
      </Box>

      {!useAutoDocument && (
        <>
          <TextField
            fullWidth
            label="四个角点坐标 (JSON格式)"
            value={points}
            onChange={(e) => handlePointsChange(e.target.value)}
            placeholder="[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]"
            multiline
            rows={3}
            disabled={isLoading}
            sx={{ mb: 3 }}
            helperText="格式: [[左上x,左上y],[右上x,右上y],[右下x,右下y],[左下x,左下y]]"
          />

          <Typography gutterBottom>输出宽度: {outputWidth}px</Typography>
          <Slider
            value={outputWidth}
            min={100}
            max={1000}
            step={50}
            onChange={(_, value) => handleOutputWidthChange(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            sx={{ mb: 3 }}
          />

          <Typography gutterBottom>输出高度: {outputHeight}px</Typography>
          <Slider
            value={outputHeight}
            min={100}
            max={800}
            step={50}
            onChange={(_, value) => handleOutputHeightChange(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            sx={{ mb: 3 }}
          />
        </>
      )}

      <Typography gutterBottom>输出质量: {quality}%</Typography>
      <Slider
        value={quality}
        min={10}
        max={100}
        step={5}
        onChange={(_, value) => handleQualityChange(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </Box>
  );
};

export default PerspectiveSettingsComponent; 