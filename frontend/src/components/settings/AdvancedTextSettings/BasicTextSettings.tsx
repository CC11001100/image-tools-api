/**
 * 基础文字设置组件
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
  Switch,
  FormControlLabel,
} from '@mui/material';

import { BasicTextSettingsProps } from './types';

const BasicTextSettings: React.FC<BasicTextSettingsProps> = ({
  isLoading,
  text,
  setText,
  fontFamily,
  setFontFamily,
  fontSize,
  setFontSize,
  fontColor,
  setFontColor,
  bold,
  setBold,
  italic,
  setItalic,
  underline,
  setUnderline,
}) => {
  return (
    <>
      <Typography variant="subtitle1" gutterBottom>
        文字内容
      </Typography>
      
      <TextField
        fullWidth
        multiline
        rows={3}
        label="文字内容"
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={isLoading}
        sx={{ mb: 3 }}
        helperText="支持多行文字，使用回车键换行"
      />

      <Typography variant="subtitle1" gutterBottom>
        字体设置
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>字体</InputLabel>
            <Select
              value={fontFamily}
              label="字体"
              onChange={(e) => setFontFamily(e.target.value)}
              disabled={isLoading}
            >
              <MenuItem value="Arial">Arial</MenuItem>
              <MenuItem value="Helvetica">Helvetica</MenuItem>
              <MenuItem value="Times New Roman">Times New Roman</MenuItem>
              <MenuItem value="Courier New">Courier New</MenuItem>
              <MenuItem value="Georgia">Georgia</MenuItem>
              <MenuItem value="Verdana">Verdana</MenuItem>
              <MenuItem value="Impact">Impact</MenuItem>
              <MenuItem value="Comic Sans MS">Comic Sans MS</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="字体颜色"
            type="color"
            value={fontColor}
            onChange={(e) => setFontColor(e.target.value)}
            disabled={isLoading}
          />
        </Grid>
      </Grid>

      <Typography gutterBottom>字体大小: {fontSize}px</Typography>
      <Slider
        value={fontSize}
        min={12}
        max={200}
        onChange={(_, value) => setFontSize(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        sx={{ mb: 2 }}
      />

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={4}>
          <FormControlLabel
            control={
              <Switch
                checked={bold}
                onChange={(e) => setBold(e.target.checked)}
                disabled={isLoading}
              />
            }
            label="粗体"
          />
        </Grid>
        <Grid item xs={4}>
          <FormControlLabel
            control={
              <Switch
                checked={italic}
                onChange={(e) => setItalic(e.target.checked)}
                disabled={isLoading}
              />
            }
            label="斜体"
          />
        </Grid>
        <Grid item xs={4}>
          <FormControlLabel
            control={
              <Switch
                checked={underline}
                onChange={(e) => setUnderline(e.target.checked)}
                disabled={isLoading}
              />
            }
            label="下划线"
          />
        </Grid>
      </Grid>
    </>
  );
};

export default BasicTextSettings;
