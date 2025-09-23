import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
  Box,
  Grid,
  Slider,
} from '@mui/material';

interface CropSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const CropSettingsComponent: React.FC<CropSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [cropType, setCropType] = useState('rectangle');
  const [quality, setQuality] = useState(90);
  
  // 矩形裁剪参数
  const [rectangle, setRectangle] = useState({
    x: 0,
    y: 0,
    width: 200,
    height: 200,
  });
  
  // 圆形裁剪参数
  const [circle, setCircle] = useState({
    center_x: 100,
    center_y: 100,
    radius: 50,
  });
  
  // 智能居中裁剪参数
  const [smartCenter, setSmartCenter] = useState({
    target_width: 400,
    target_height: 400,
  });

  useEffect(() => {
    const settings: any = {
      crop_type: cropType,
      quality: quality,
    };

    if (cropType === 'rectangle') {
      settings.x = rectangle.x;
      settings.y = rectangle.y;
      settings.width = rectangle.width;
      settings.height = rectangle.height;
    } else if (cropType === 'circle') {
      settings.center_x = circle.center_x;
      settings.center_y = circle.center_y;
      settings.radius = circle.radius;
    } else if (cropType === 'smart-center') {
      settings.target_width = smartCenter.target_width;
      settings.target_height = smartCenter.target_height;
    }

    onSettingsChange(settings);
  }, [cropType, quality, rectangle, circle, smartCenter, onSettingsChange]);

  const renderRectangleSettings = () => (
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <TextField
          fullWidth
          label="X坐标"
          type="number"
          value={rectangle.x}
          onChange={(e) => setRectangle({ ...rectangle, x: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
      <Grid item xs={6}>
        <TextField
          fullWidth
          label="Y坐标"
          type="number"
          value={rectangle.y}
          onChange={(e) => setRectangle({ ...rectangle, y: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
      <Grid item xs={6}>
        <TextField
          fullWidth
          label="宽度"
          type="number"
          value={rectangle.width}
          onChange={(e) => setRectangle({ ...rectangle, width: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
      <Grid item xs={6}>
        <TextField
          fullWidth
          label="高度"
          type="number"
          value={rectangle.height}
          onChange={(e) => setRectangle({ ...rectangle, height: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
    </Grid>
  );

  const renderCircleSettings = () => (
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <TextField
          fullWidth
          label="圆心X坐标"
          type="number"
          value={circle.center_x}
          onChange={(e) => setCircle({ ...circle, center_x: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
      <Grid item xs={6}>
        <TextField
          fullWidth
          label="圆心Y坐标"
          type="number"
          value={circle.center_y}
          onChange={(e) => setCircle({ ...circle, center_y: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="半径"
          type="number"
          value={circle.radius}
          onChange={(e) => setCircle({ ...circle, radius: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
    </Grid>
  );

  const renderSmartCenterSettings = () => (
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <TextField
          fullWidth
          label="目标宽度"
          type="number"
          value={smartCenter.target_width}
          onChange={(e) => setSmartCenter({ ...smartCenter, target_width: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
      <Grid item xs={6}>
        <TextField
          fullWidth
          label="目标高度"
          type="number"
          value={smartCenter.target_height}
          onChange={(e) => setSmartCenter({ ...smartCenter, target_height: Number(e.target.value) })}
          disabled={isLoading}
          size="small"
        />
      </Grid>
    </Grid>
  );

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>裁剪类型</InputLabel>
        <Select
          value={cropType}
          label="裁剪类型"
          onChange={(e) => setCropType(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="rectangle">矩形裁剪</MenuItem>
          <MenuItem value="circle">圆形裁剪</MenuItem>
          <MenuItem value="smart-center">智能居中裁剪</MenuItem>
        </Select>
      </FormControl>

      <Box sx={{ mb: 2 }}>
        {cropType === 'rectangle' && renderRectangleSettings()}
        {cropType === 'circle' && renderCircleSettings()}
        {cropType === 'smart-center' && renderSmartCenterSettings()}
      </Box>

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

export default CropSettingsComponent; 