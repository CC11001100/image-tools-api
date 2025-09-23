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
  Switch,
  FormControlLabel,
} from '@mui/material';
import { TransformType, RotateSettings } from '../hooks/useTransform';
import styles from './TransformSettings.module.css';

interface TransformSettingsProps {
  transformType: TransformType;
  quality: number;
  rotateSettings: RotateSettings;
  isLoading: boolean;
  onTransformTypeChange: (type: TransformType) => void;
  onQualityChange: (quality: number) => void;
  onRotateSettingsChange: (settings: RotateSettings) => void;
  onApply: () => void;
  getTransformTypeName: (type: TransformType) => string;
}

const TransformSettings: React.FC<TransformSettingsProps> = ({
  transformType,
  quality,
  rotateSettings,
  isLoading,
  onTransformTypeChange,
  onQualityChange,
  onRotateSettingsChange,
  onApply,
  getTransformTypeName,
}) => {
  const renderRotateSettings = () => (
    <>
      <Grid item xs={12}>
        <Typography gutterBottom>旋转角度: {rotateSettings.angle}°</Typography>
        <Slider
          value={rotateSettings.angle}
          min={-180}
          max={180}
          step={1}
          onChange={(_, value) => onRotateSettingsChange({
            ...rotateSettings,
            angle: value as number
          })}
          valueLabelDisplay="auto"
          marks={[
            { value: -180, label: '-180°' },
            { value: -90, label: '-90°' },
            { value: 0, label: '0°' },
            { value: 90, label: '90°' },
            { value: 180, label: '180°' },
          ]}
        />
      </Grid>
      
      <Grid item xs={12}>
        <FormControlLabel
          control={
            <Switch
              checked={rotateSettings.expand}
              onChange={(e) => onRotateSettingsChange({
                ...rotateSettings,
                expand: e.target.checked
              })}
              color="primary"
            />
          }
          label="扩展画布（避免裁剪）"
        />
      </Grid>
      
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="填充颜色"
          type="color"
          value={rotateSettings.fillColor}
          onChange={(e) => onRotateSettingsChange({
            ...rotateSettings,
            fillColor: e.target.value
          })}
          helperText="当不扩展画布时的背景填充颜色"
        />
      </Grid>
    </>
  );

  const transformOptions = [
    { value: 'rotate', label: '自定义旋转' },
    { value: 'flip-horizontal', label: '水平翻转（镜像）' },
    { value: 'flip-vertical', label: '垂直翻转' },
    { value: 'rotate-90-cw', label: '顺时针旋转90°' },
    { value: 'rotate-90-ccw', label: '逆时针旋转90°' },
    { value: 'rotate-180', label: '旋转180°' },
  ];

  return (
    <Paper elevation={2} className={styles.paramForm}>
      <Typography variant="h6" gutterBottom>
        图片变换设置
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>变换类型</InputLabel>
            <Select
              value={transformType}
              label="变换类型"
              onChange={(e) => onTransformTypeChange(e.target.value as TransformType)}
            >
              {transformOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {transformType === 'rotate' && renderRotateSettings()}

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
            {isLoading ? '处理中...' : `应用${getTransformTypeName(transformType)}`}
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default TransformSettings; 