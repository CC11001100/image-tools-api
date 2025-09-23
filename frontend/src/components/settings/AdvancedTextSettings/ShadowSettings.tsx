/**
 * 阴影设置组件
 */

import React from 'react';
import {
  TextField,
  Typography,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import { ShadowSettingsProps } from './types';

const ShadowSettings: React.FC<ShadowSettingsProps> = ({
  isLoading,
  shadowOffsetX,
  setShadowOffsetX,
  shadowOffsetY,
  setShadowOffsetY,
  shadowBlur,
  setShadowBlur,
  shadowColor,
  setShadowColor,
}) => {
  return (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography>阴影设置</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={4}>
            <TextField
              fullWidth
              label="X偏移"
              type="number"
              value={shadowOffsetX}
              onChange={(e) => setShadowOffsetX(parseInt(e.target.value) || 0)}
              disabled={isLoading}
            />
          </Grid>
          <Grid item xs={4}>
            <TextField
              fullWidth
              label="Y偏移"
              type="number"
              value={shadowOffsetY}
              onChange={(e) => setShadowOffsetY(parseInt(e.target.value) || 0)}
              disabled={isLoading}
            />
          </Grid>
          <Grid item xs={4}>
            <TextField
              fullWidth
              label="模糊度"
              type="number"
              value={shadowBlur}
              onChange={(e) => setShadowBlur(parseInt(e.target.value) || 0)}
              disabled={isLoading}
              inputProps={{ min: 0, max: 50 }}
            />
          </Grid>
        </Grid>

        {(shadowOffsetX !== 0 || shadowOffsetY !== 0 || shadowBlur > 0) && (
          <TextField
            fullWidth
            label="阴影颜色"
            type="color"
            value={shadowColor}
            onChange={(e) => setShadowColor(e.target.value)}
            disabled={isLoading}
            sx={{ mb: 2 }}
          />
        )}
      </AccordionDetails>
    </Accordion>
  );
};

export default ShadowSettings;
