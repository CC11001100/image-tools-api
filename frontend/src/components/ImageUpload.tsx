import React, { ChangeEvent, useState } from 'react';
import { Box, Button, CircularProgress, Typography } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { ClickableImage } from './ClickableImage';
import styles from './ImageUpload.module.css';

interface ImageUploadProps {
  onImageSelected: (file: File) => void;
  isLoading?: boolean;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ 
  onImageSelected, 
  isLoading = false 
}) => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const handleImageChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      onImageSelected(file);
      
      // 预览图像
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <Box sx={{ textAlign: 'center', my: 3 }}>
      <input
        accept="image/*"
        style={{ display: 'none' }}
        id="upload-image"
        type="file"
        onChange={handleImageChange}
        disabled={isLoading}
      />
      <label htmlFor="upload-image">
        <Button
          variant="contained"
          component="span"
          startIcon={<CloudUploadIcon />}
          disabled={isLoading}
          sx={{ mb: 2 }}
        >
          {isLoading ? '处理中...' : '上传图片'}
        </Button>
      </label>

      {isLoading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
          <CircularProgress />
        </Box>
      )}

      {selectedImage && !isLoading && (
        <Box className={styles.imageContainer}>
          <Typography variant="subtitle1" gutterBottom>
            原始图片:
          </Typography>
          <ClickableImage
            src={selectedImage}
            alt="原图预览"
            title="上传的图片"
            className={styles.imagePreview}
            downloadFileName="uploaded-image.jpg"
          />
        </Box>
      )}
    </Box>
  );
};

export default ImageUpload; 