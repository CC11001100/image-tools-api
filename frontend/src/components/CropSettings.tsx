import React from 'react';
import {
  Paper,
  Typography,
  Divider,
  Grid,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Box,
  InputAdornment,
} from '@mui/material';
import { CropType, CropRectangle, CropCircle, CropSmartCenter } from '../hooks/useCrop';
import styles from './CropSettings.module.css';

interface CropSettingsProps {
  cropType: CropType;
  quality: number;
  rectangle: CropRectangle;
  circle: CropCircle;
  smartCenter: CropSmartCenter;
  isLoading: boolean;
  originalImageSize: {width: number, height: number} | null;
  onCropTypeChange: (type: CropType) => void;
  onQualityChange: (quality: number) => void;
  onRectangleChange: (rectangle: CropRectangle) => void;
  onCircleChange: (circle: CropCircle) => void;
  onSmartCenterChange: (smartCenter: CropSmartCenter) => void;
  onApply: () => void;
}

const CropSettings: React.FC<CropSettingsProps> = ({
  cropType,
  quality,
  rectangle,
  circle,
  smartCenter,
  isLoading,
  originalImageSize,
  onCropTypeChange,
  onQualityChange,
  onRectangleChange,
  onCircleChange,
  onSmartCenterChange,
  onApply,
}) => {
  const renderRectangleSettings = () => (
    <>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="X坐标"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 0, max: originalImageSize?.width || 1000 }}
          value={rectangle.x}
          onChange={(e) => onRectangleChange({
            ...rectangle,
            x: Number(e.target.value)
          })}
        />
      </Grid>
      
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Y坐标"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 0, max: originalImageSize?.height || 1000 }}
          value={rectangle.y}
          onChange={(e) => onRectangleChange({
            ...rectangle,
            y: Number(e.target.value)
          })}
        />
      </Grid>
      
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="宽度"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 1, max: originalImageSize?.width || 1000 }}
          value={rectangle.width}
          onChange={(e) => onRectangleChange({
            ...rectangle,
            width: Number(e.target.value)
          })}
        />
      </Grid>
      
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="高度"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 1, max: originalImageSize?.height || 1000 }}
          value={rectangle.height}
          onChange={(e) => onRectangleChange({
            ...rectangle,
            height: Number(e.target.value)
          })}
        />
      </Grid>
    </>
  );

  const renderCircleSettings = () => (
    <>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="圆心X坐标"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 0, max: originalImageSize?.width || 1000 }}
          value={circle.centerX}
          onChange={(e) => onCircleChange({
            ...circle,
            centerX: Number(e.target.value)
          })}
        />
      </Grid>
      
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="圆心Y坐标"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 0, max: originalImageSize?.height || 1000 }}
          value={circle.centerY}
          onChange={(e) => onCircleChange({
            ...circle,
            centerY: Number(e.target.value)
          })}
        />
      </Grid>
      
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="半径"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 1, max: Math.min(originalImageSize?.width || 500, originalImageSize?.height || 500) / 2 }}
          value={circle.radius}
          onChange={(e) => onCircleChange({
            ...circle,
            radius: Number(e.target.value)
          })}
        />
      </Grid>
    </>
  );

  const renderSmartCenterSettings = () => (
    <>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="目标宽度"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 1, max: 5000 }}
          value={smartCenter.targetWidth}
          onChange={(e) => onSmartCenterChange({
            ...smartCenter,
            targetWidth: Number(e.target.value)
          })}
        />
      </Grid>
      
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="目标高度"
          type="number"
          InputProps={{
            endAdornment: <InputAdornment position="end">px</InputAdornment>,
          }}
          inputProps={{ min: 1, max: 5000 }}
          value={smartCenter.targetHeight}
          onChange={(e) => onSmartCenterChange({
            ...smartCenter,
            targetHeight: Number(e.target.value)
          })}
        />
      </Grid>
    </>
  );

  return (
    <Paper elevation={2} className={styles.paramForm}>
      <Typography variant="h6" gutterBottom>
        裁剪设置
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>裁剪类型</InputLabel>
            <Select
              value={cropType}
              label="裁剪类型"
              onChange={(e) => onCropTypeChange(e.target.value as CropType)}
            >
              <MenuItem value="rectangle">矩形裁剪</MenuItem>
              <MenuItem value="circle">圆形裁剪</MenuItem>
              <MenuItem value="smart-center">智能居中裁剪</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {originalImageSize && (
          <Grid item xs={12}>
            <Typography variant="body2" color="textSecondary">
              原图尺寸: {originalImageSize.width} × {originalImageSize.height} 像素
            </Typography>
          </Grid>
        )}

        {cropType === 'rectangle' && renderRectangleSettings()}
        {cropType === 'circle' && renderCircleSettings()}
        {cropType === 'smart-center' && renderSmartCenterSettings()}

        <Grid item xs={12}>
          <Typography gutterBottom>图片质量: {quality}%</Typography>
          <Slider
            value={quality}
            min={10}
            max={100}
            step={5}
            onChange={(_, value) => onQualityChange(value as number)}
            valueLabelDisplay="auto"
          />
        </Grid>

        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            onClick={onApply}
            disabled={isLoading}
            fullWidth
          >
            {isLoading ? '裁剪中...' : '应用裁剪'}
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default CropSettings; 