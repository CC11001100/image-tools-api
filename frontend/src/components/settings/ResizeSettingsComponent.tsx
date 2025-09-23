import React from 'react';
import {
  FormControl,
  FormControlLabel,
  FormGroup,
  FormHelperText,
  Grid,
  InputAdornment,
  MenuItem,
  Select,
  Switch,
  TextField,
  Typography,
} from '@mui/material';

interface ResizeSettingsProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
  appliedParams?: Record<string, any> | null;
  settings?: {
    width?: number;
    height?: number;
    mode?: string;
    quality?: number;
    keepAspectRatio?: boolean;
    compressionLevel?: number;
  };
}

const ResizeSettingsComponent: React.FC<ResizeSettingsProps> = ({
  settings = {},
  onSettingsChange,
  isLoading,
  appliedParams,
}) => {
  const handleChange = (field: string, value: any) => {
    onSettingsChange({
      ...settings,
      [field]: value,
    });
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          调整大小设置
        </Typography>
      </Grid>

      <Grid item xs={12} sm={6}>
        <FormControl fullWidth>
          <TextField
            label="宽度"
            type="number"
            value={settings.width?.toString() || ''}
            onChange={(e) => {
              const value = e.target.value;
              // 如果是空字符串，传递 undefined；否则转换为数字
              handleChange('width', value === '' ? undefined : parseInt(value, 10));
            }}
            InputProps={{
              endAdornment: <InputAdornment position="end">px</InputAdornment>,
            }}
          />
          <FormHelperText>设置图片的新宽度（像素）</FormHelperText>
        </FormControl>
      </Grid>

      <Grid item xs={12} sm={6}>
        <FormControl fullWidth>
          <TextField
            label="高度"
            type="number"
            value={settings.height?.toString() || ''}
            onChange={(e) => {
              const value = e.target.value;
              // 如果是空字符串，传递 undefined；否则转换为数字
              handleChange('height', value === '' ? undefined : parseInt(value, 10));
            }}
            InputProps={{
              endAdornment: <InputAdornment position="end">px</InputAdornment>,
            }}
          />
          <FormHelperText>设置图片的新高度（像素）</FormHelperText>
        </FormControl>
      </Grid>

      <Grid item xs={12}>
        <FormControl fullWidth>
          <Select
            value={settings.mode || 'fit'}
            onChange={(e) => handleChange('mode', e.target.value)}
          >
            <MenuItem value="fit">适应（保持比例）</MenuItem>
            <MenuItem value="fill">填充（可能裁剪）</MenuItem>
            <MenuItem value="stretch">拉伸（可能变形）</MenuItem>
          </Select>
          <FormHelperText>选择调整大小的模式</FormHelperText>
        </FormControl>
      </Grid>

      <Grid item xs={12} sm={6}>
        <FormControl fullWidth>
          <TextField
            label="质量"
            type="number"
            value={settings.quality || 90}
            onChange={(e) => handleChange('quality', Number(e.target.value))}
            InputProps={{
              endAdornment: <InputAdornment position="end">%</InputAdornment>,
            }}
          />
          <FormHelperText>设置图片质量（1-100）</FormHelperText>
        </FormControl>
      </Grid>

      <Grid item xs={12} sm={6}>
        <FormControl fullWidth>
          <TextField
            label="压缩级别"
            type="number"
            value={settings.compressionLevel || 6}
            onChange={(e) => handleChange('compressionLevel', Number(e.target.value))}
            InputProps={{
              inputProps: { min: 0, max: 9 }
            }}
          />
          <FormHelperText>设置压缩级别（0-9，0为无压缩）</FormHelperText>
        </FormControl>
      </Grid>

      <Grid item xs={12}>
        <FormGroup>
          <FormControlLabel
            control={
              <Switch
                checked={settings.keepAspectRatio ?? true}
                onChange={(e) => handleChange('keepAspectRatio', e.target.checked)}
              />
            }
            label="保持宽高比"
          />
          <FormHelperText>
            启用后将保持原始图片的宽高比
          </FormHelperText>
        </FormGroup>
      </Grid>
    </Grid>
  );
};

export default ResizeSettingsComponent; 