import React from 'react';
import {
  Paper,
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  Slider,
  Typography,
  Divider,
} from '@mui/material';
import styles from './WatermarkSettings.module.css';

type Position = 'center' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';

interface WatermarkSettingsProps {
  watermarkText: string;
  position: Position;
  opacity: number;
  color: string;
  fontSize: number;
  angle: number;
  isLoading: boolean;
  onTextChange: (text: string) => void;
  onPositionChange: (position: Position) => void;
  onOpacityChange: (opacity: number) => void;
  onColorChange: (color: string) => void;
  onFontSizeChange: (size: number) => void;
  onAngleChange: (angle: number) => void;
  onApply: () => void;
}

const WatermarkSettings: React.FC<WatermarkSettingsProps> = ({
  watermarkText,
  position,
  opacity,
  color,
  fontSize,
  angle,
  isLoading,
  onTextChange,
  onPositionChange,
  onOpacityChange,
  onColorChange,
  onFontSizeChange,
  onAngleChange,
  onApply,
}) => {
  return (
    <Paper elevation={2} className={styles.paramForm}>
      <Typography variant="h6" gutterBottom>
        水印设置
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="水印文字"
            variant="outlined"
            value={watermarkText}
            onChange={(e) => onTextChange(e.target.value)}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>位置</InputLabel>
            <Select
              value={position}
              label="位置"
              onChange={(e: SelectChangeEvent<Position>) => onPositionChange(e.target.value as Position)}
            >
              <MenuItem value="center">中心</MenuItem>
              <MenuItem value="top-left">左上角</MenuItem>
              <MenuItem value="top-right">右上角</MenuItem>
              <MenuItem value="bottom-left">左下角</MenuItem>
              <MenuItem value="bottom-right">右下角</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="颜色"
            type="color"
            variant="outlined"
            value={color}
            onChange={(e) => onColorChange(e.target.value)}
            InputProps={{ style: { padding: '10px' } }}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <Typography gutterBottom>透明度: {opacity.toFixed(1)}</Typography>
          <Slider
            value={opacity}
            min={0.1}
            max={1}
            step={0.1}
            onChange={(_, value) => onOpacityChange(value as number)}
            valueLabelDisplay="auto"
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <Typography gutterBottom>字体大小: {fontSize}</Typography>
          <Slider
            value={fontSize}
            min={10}
            max={100}
            step={5}
            onChange={(_, value) => onFontSizeChange(value as number)}
            valueLabelDisplay="auto"
          />
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>旋转角度: {angle}°</Typography>
          <Slider
            value={angle}
            min={-180}
            max={180}
            step={5}
            onChange={(_, value) => onAngleChange(value as number)}
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
          <Button
            variant="contained"
            color="primary"
            onClick={onApply}
            disabled={isLoading || !watermarkText}
            fullWidth
          >
            应用水印
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default WatermarkSettings; 