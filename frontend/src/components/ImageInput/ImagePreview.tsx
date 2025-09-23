import React from 'react';
import {
  Box,
  Typography,
  Paper,
  IconButton,
  Fade,
} from '@mui/material';
import {
  Close as CloseIcon,
} from '@mui/icons-material';
import { ClickableImage } from '../ClickableImage';

interface ImagePreviewProps {
  previewUrl: string | null;
  onClear: () => void;
}

export const ImagePreview: React.FC<ImagePreviewProps> = ({ previewUrl, onClear }) => {
  if (!previewUrl) return null;

  return (
    <Fade in={true}>
      <Paper elevation={3} sx={{ mt: 3, p: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="subtitle1" color="primary">
            图片预览
          </Typography>
          <IconButton onClick={onClear} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
        <Box sx={{ textAlign: 'center' }}>
          <ClickableImage
            src={previewUrl}
            alt="图片预览"
            title="图片预览"
            style={{
              maxWidth: 'min(100%, 450px)',
              minWidth: '250px',
              maxHeight: '350px',
              borderRadius: '8px',
              border: '2px solid #e0e0e0',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            }}
            downloadFileName="preview-image.jpg"
          />
        </Box>
      </Paper>
    </Fade>
  );
};
