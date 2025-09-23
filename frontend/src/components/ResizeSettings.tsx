import React from 'react';
import {
  Paper,
  TextField,
  Button,
  Grid,
  FormControlLabel,
  Switch,
  Slider,
  Typography,
  Divider,
  InputAdornment,
} from '@mui/material';
import styles from './ResizeSettings.module.css';

interface ResizeSettingsProps {
  width: string;
  height: string;
  maintainRatio: boolean;
  quality: number;
  isLoading: boolean;
  onWidthChange: (width: string) => void;
  onHeightChange: (height: string) => void;
  onMaintainRatioChange: (maintain: boolean) => void;
  onQualityChange: (quality: number) => void;
  onApply: () => void;
}

const ResizeSettings: React.FC<ResizeSettingsProps> = ({
  width,
  height,
  maintainRatio,
  quality,
  isLoading,
  onWidthChange,
  onHeightChange,
  onMaintainRatioChange,
  onQualityChange,
  onApply,
}) => {
  return (
    <Paper elevation={2} className={styles.paramForm}>
      <Typography variant="h6" gutterBottom>
        尺寸设置
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="宽度"
            type="number"
            InputProps={{
              endAdornment: <InputAdornment position="end">px</InputAdornment>,
            }}
            inputProps={{ min: 1 }}
            value={width}
            onChange={(e) => onWidthChange(e.target.value)}
            placeholder="保持为空将按比例计算"
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
            inputProps={{ min: 1 }}
            value={height}
            onChange={(e) => onHeightChange(e.target.value)}
            placeholder="保持为空将按比例计算"
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={maintainRatio}
                onChange={(e) => onMaintainRatioChange(e.target.checked)}
                color="primary"
              />
            }
            label="保持原始比例"
          />
        </Grid>

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
            disabled={isLoading || (!width && !height)}
            fullWidth
          >
            调整大小
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default ResizeSettings; 