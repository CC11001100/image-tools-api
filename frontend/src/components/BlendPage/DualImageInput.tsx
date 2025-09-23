import React from 'react';
import { Typography, Box, Button, Paper, Grid } from '@mui/material';
import { ImageInput } from '../ImageInput';
import { ClickableImage } from '../ClickableImage';

interface DualImageInputProps {
  basePreviewUrl: string | null;
  overlayPreviewUrl: string | null;
  onBaseImageSelect: (file: File | null, imageUrl: string | null) => void;
  onOverlayImageSelect: (file: File | null, imageUrl: string | null) => void;
  onUseDefaultImages: () => void;
}

export const DualImageInput: React.FC<DualImageInputProps> = ({
  basePreviewUrl,
  overlayPreviewUrl,
  onBaseImageSelect,
  onOverlayImageSelect,
  onUseDefaultImages,
}) => {
  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6">选择图片</Typography>
        <Button 
          variant="outlined" 
          size="small"
          onClick={onUseDefaultImages}
        >
          使用示例图片
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* 基础图片 */}
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle1" gutterBottom>
            基础图片（底层）
          </Typography>
          <ImageInput onImageSelect={onBaseImageSelect} />
          
          {basePreviewUrl && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                基础图片预览:
              </Typography>
              <ClickableImage
                src={basePreviewUrl}
                alt="基础图片"
                title="基础图片预览"
                style={{ 
                  maxWidth: 'min(100%, 450px)', 
                  minWidth: '250px',
                  height: 'auto', 
                  border: '2px solid #e0e0e0',
                  borderRadius: '8px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                }}
                downloadFileName="base-image.jpg"
              />
            </Box>
          )}
        </Grid>

        {/* 叠加图片 */}
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle1" gutterBottom>
            叠加图片（上层）
          </Typography>
          <ImageInput onImageSelect={onOverlayImageSelect} />
          
          {overlayPreviewUrl && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                叠加图片预览:
              </Typography>
              <ClickableImage
                src={overlayPreviewUrl}
                alt="叠加图片"
                title="叠加图片预览"
                style={{ 
                  maxWidth: 'min(100%, 450px)', 
                  minWidth: '250px',
                  height: 'auto', 
                  border: '2px solid #e0e0e0',
                  borderRadius: '8px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                }}
                downloadFileName="overlay-image.jpg"
              />
            </Box>
          )}
        </Grid>
      </Grid>
    </Paper>
  );
}; 