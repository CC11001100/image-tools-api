/**
 * 描边设置组件
 */

import React from 'react';
import {
  TextField,
  Slider,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import { StrokeSettingsProps } from './types';

const StrokeSettings: React.FC<StrokeSettingsProps> = ({
  isLoading,
  strokeWidth,
  setStrokeWidth,
  strokeColor,
  setStrokeColor,
}) => {
  return (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography>描边设置</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Typography gutterBottom>描边宽度: {strokeWidth}px</Typography>
        <Slider
          value={strokeWidth}
          min={0}
          max={20}
          onChange={(_, value) => setStrokeWidth(value as number)}
          valueLabelDisplay="auto"
          disabled={isLoading}
          sx={{ mb: 2 }}
        />

        {strokeWidth > 0 && (
          <TextField
            fullWidth
            label="描边颜色"
            type="color"
            value={strokeColor}
            onChange={(e) => setStrokeColor(e.target.value)}
            disabled={isLoading}
            sx={{ mb: 2 }}
          />
        )}
      </AccordionDetails>
    </Accordion>
  );
};

export default StrokeSettings;
