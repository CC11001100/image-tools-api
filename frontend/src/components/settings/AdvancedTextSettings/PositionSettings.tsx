/**
 * 位置设置组件
 */

import React from 'react';
import {
  TextField,
  Slider,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
} from '@mui/material';

import { PositionSettingsProps } from './types';

const PositionSettings: React.FC<PositionSettingsProps> = ({
  isLoading,
  position,
  setPosition,
  xOffset,
  setXOffset,
  yOffset,
  setYOffset,
  rotation,
  setRotation,
}) => {
  return (
    <>
      <Typography variant="subtitle1" gutterBottom>
        位置设置
      </Typography>

      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>位置</InputLabel>
        <Select
          value={position}
          label="位置"
          onChange={(e) => setPosition(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="center">居中</MenuItem>
          <MenuItem value="top-left">左上</MenuItem>
          <MenuItem value="top-center">中上</MenuItem>
          <MenuItem value="top-right">右上</MenuItem>
          <MenuItem value="middle-left">左中</MenuItem>
          <MenuItem value="middle-right">右中</MenuItem>
          <MenuItem value="bottom-left">左下</MenuItem>
          <MenuItem value="bottom-center">中下</MenuItem>
          <MenuItem value="bottom-right">右下</MenuItem>
          <MenuItem value="custom">自定义</MenuItem>
        </Select>
      </FormControl>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="X偏移"
            type="number"
            value={xOffset}
            onChange={(e) => setXOffset(parseInt(e.target.value) || 0)}
            disabled={isLoading}
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="Y偏移"
            type="number"
            value={yOffset}
            onChange={(e) => setYOffset(parseInt(e.target.value) || 0)}
            disabled={isLoading}
          />
        </Grid>
      </Grid>

      <Typography gutterBottom>旋转角度: {rotation}°</Typography>
      <Slider
        value={rotation}
        min={-180}
        max={180}
        onChange={(_, value) => setRotation(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 3 }}
      />
    </>
  );
};

export default PositionSettings;
