/**
 * 多行文字设置组件
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
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import { MultilineTextSettingsProps } from './types';

const MultilineTextSettings: React.FC<MultilineTextSettingsProps> = ({
  isLoading,
  lineSpacing,
  setLineSpacing,
  maxWidth,
  setMaxWidth,
  lineHeight,
  setLineHeight,
  textAlign,
  setTextAlign,
  letterSpacing,
  setLetterSpacing,
}) => {
  return (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography>多行文字设置</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="行间距"
              type="number"
              value={lineSpacing}
              onChange={(e) => setLineSpacing(parseInt(e.target.value) || 5)}
              disabled={isLoading}
              inputProps={{ min: 0, max: 50 }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="最大宽度"
              type="number"
              value={maxWidth}
              onChange={(e) => setMaxWidth(e.target.value)}
              disabled={isLoading}
              helperText="自动换行"
              inputProps={{ min: 50 }}
            />
          </Grid>
        </Grid>

        <Typography gutterBottom>行高: {lineHeight}</Typography>
        <Slider
          value={lineHeight}
          min={0.5}
          max={3}
          step={0.1}
          onChange={(_, value) => setLineHeight(value as number)}
          valueLabelDisplay="auto"
          disabled={isLoading}
          sx={{ mb: 2 }}
        />

        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>文字对齐</InputLabel>
          <Select
            value={textAlign}
            label="文字对齐"
            onChange={(e) => setTextAlign(e.target.value)}
            disabled={isLoading}
          >
            <MenuItem value="left">左对齐</MenuItem>
            <MenuItem value="center">居中</MenuItem>
            <MenuItem value="right">右对齐</MenuItem>
          </Select>
        </FormControl>

        <Typography gutterBottom>字间距: {letterSpacing}px</Typography>
        <Slider
          value={letterSpacing}
          min={-10}
          max={50}
          onChange={(_, value) => setLetterSpacing(value as number)}
          valueLabelDisplay="auto"
          disabled={isLoading}
          sx={{ mb: 2 }}
        />
      </AccordionDetails>
    </Accordion>
  );
};

export default MultilineTextSettings;
