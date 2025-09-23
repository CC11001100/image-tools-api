import React, { useState, ReactNode } from 'react';
import { Typography, Box, Button, Paper, Grid } from '@mui/material';
import ImageUpload from './ImageUpload';
import { ImageInput } from './ImageInput';
import { ClickableImage } from './ClickableImage';
import { DEFAULT_SAMPLE_IMAGE } from '../config/constants';

interface ImageProcessingPageProps {
  title: string;
  description: string;
  settingsPanel: React.ComponentType<{
    onProcess: () => void;
    isLoading: boolean;
    onChange?: (settings: any) => void;
    [key: string]: any;
  }>;
  processImage: (imageFile: File | null, imageUrl: string | null, settings: any) => Promise<Blob>;
  defaultSettings?: any;
}

const ImageProcessingPage: React.FC<ImageProcessingPageProps> = ({
  title,
  description,
  settingsPanel: SettingsPanel,
  processImage,
  defaultSettings = {}
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedImageUrl, setSelectedImageUrl] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [settings, setSettings] = useState(defaultSettings);

  const handleImageSelect = (file: File | null, imageUrl: string | null) => {
    setSelectedFile(file);
    setSelectedImageUrl(imageUrl);
    
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewUrl(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    } else if (imageUrl) {
      setPreviewUrl(imageUrl);
    }
  };

  const handleProcess = async () => {
    if (!selectedFile && !selectedImageUrl) {
      alert('请先选择图片');
      return;
    }
    
    setIsLoading(true);
    try {
      const resultBlob = await processImage(selectedFile, selectedImageUrl, settings);
      const url = URL.createObjectURL(resultBlob);
      setResultImage(url);
    } catch (error) {
      console.error('Error:', error);
      alert('处理失败');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUseDefaultImage = () => {
    setSelectedFile(null);
    setSelectedImageUrl(null);
    setPreviewUrl(DEFAULT_SAMPLE_IMAGE);
  };

  const updateSettings = (newSettings: any) => {
    setSettings({ ...settings, ...newSettings });
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body1" paragraph>
        {description}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">选择图片</Typography>
              <Button 
                variant="outlined" 
                size="small"
                onClick={handleUseDefaultImage}
              >
                使用示例图片
              </Button>
            </Box>
            
            <ImageInput onImageSelect={handleImageSelect} />
            
            {previewUrl && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  当前图片预览:
                </Typography>
                <ClickableImage
                  src={previewUrl} 
                  alt="当前图片" 
                  title="当前图片预览"
                  style={{ 
                    maxWidth: '100%', 
                    height: 'auto', 
                    borderRadius: '4px',
                    border: '1px solid #ddd'
                  }} 
                  downloadFileName="current-image.jpg"
                />
              </Box>
            )}
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              参数设置
            </Typography>
            
            <SettingsPanel
              onProcess={handleProcess}
              isLoading={isLoading}
              {...settings}
              onChange={updateSettings}
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          {resultImage && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                处理结果
              </Typography>
              <ClickableImage
                src={resultImage} 
                alt="处理后图片" 
                title="处理结果"
                style={{ 
                  maxWidth: '100%', 
                  height: 'auto', 
                  borderRadius: '4px',
                  border: '1px solid #ddd'
                }} 
                downloadFileName="processed-image.jpg"
              />
              <Button 
                fullWidth
                variant="outlined" 
                color="primary" 
                sx={{ mt: 2 }}
                href={resultImage}
                download="processed-image.jpg"
              >
                下载图片
              </Button>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default ImageProcessingPage; 