/**
 * 帧选择器组件
 */

import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardMedia,
  FormControlLabel,
  Checkbox,
} from '@mui/material';

import { FrameSelectorProps } from './types';

const FrameSelector: React.FC<FrameSelectorProps> = ({
  frames,
  selectedFrames,
  onToggleFrameSelection,
}) => {
  if (frames.length === 0) {
    return null;
  }

  return (
    <Paper sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        帧选择器
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        点击帧缩略图来选择要提取的帧
      </Typography>
      
      <Grid container spacing={2}>
        {frames.map((frame) => (
          <Grid item xs={6} sm={4} md={3} lg={2} key={frame.index}>
            <Card
              sx={{
                cursor: 'pointer',
                border: selectedFrames.has(frame.index) ? '2px solid #1976d2' : '2px solid transparent',
                '&:hover': {
                  boxShadow: 3,
                },
              }}
              onClick={() => onToggleFrameSelection(frame.index)}
            >
              <CardMedia
                component="img"
                height="120"
                image={frame.dataUrl}
                alt={`Frame ${frame.index}`}
                sx={{
                  objectFit: 'contain',
                  backgroundColor: 'grey.100',
                }}
              />
              <Box sx={{ p: 1, textAlign: 'center' }}>
                <Typography variant="caption">
                  帧 {frame.index}
                </Typography>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={selectedFrames.has(frame.index)}
                      size="small"
                    />
                  }
                  label=""
                  sx={{ m: 0 }}
                />
              </Box>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
};

export default FrameSelector;
