import React, { useState, useMemo } from 'react';
import {
  Typography,
  Paper,
  Grid,
  FormControlLabel,
  Switch,
  Box,
} from '@mui/material';
import { ImageGallery } from './ImageGallery';
import { BlendExampleCard, BlendExample, BlendShowcaseProps, GalleryImage } from './BlendShowcase/index';

export const BlendShowcase: React.FC<BlendShowcaseProps> = ({
  title,
  description,
  examples,
  onApplyParams
}) => {
  const [currentBaseIndex, setCurrentBaseIndex] = useState<Record<number, number>>({});
  const [currentOverlayIndex, setCurrentOverlayIndex] = useState<Record<number, number>>({});
  const [galleryOpen, setGalleryOpen] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [enableLargeDisplay, setEnableLargeDisplay] = useState(false);

  // 生成画廊图片列表
  const galleryImages: GalleryImage[] = useMemo(() => {
    const images: GalleryImage[] = [];
    
    examples.forEach((example, exampleIndex) => {
      // 添加基础图片
      example.baseImages.forEach((img, imgIndex) => {
        images.push({
          src: img,
          alt: `${example.title} - 基础图 ${imgIndex + 1}`,
          title: `${example.title} - 基础图 ${imgIndex + 1}`,
          description: example.description
        });
      });

      // 添加叠加图片
      example.overlayImages.forEach((img, imgIndex) => {
        images.push({
          src: img,
          alt: `${example.title} - 叠加图 ${imgIndex + 1}`,
          title: `${example.title} - 叠加图 ${imgIndex + 1}`,
          description: example.description
        });
      });

      // 添加结果图片
      example.resultImages.forEach((img, imgIndex) => {
        images.push({
          src: img,
          alt: `${example.title} - 混合结果 ${imgIndex + 1}`,
          title: `${example.title} - 混合结果 ${imgIndex + 1}`,
          description: example.description
        });
      });
    });
    
    return images;
  }, [examples]);

  const handleImageClick = (src: string, title: string) => {
    const imageIndex = galleryImages.findIndex(img => img.src === src);
    if (imageIndex !== -1) {
      setCurrentImageIndex(imageIndex);
      setGalleryOpen(true);
    }
  };

  const handleCloseGallery = () => {
    setGalleryOpen(false);
  };

  const handleApplyParams = (example: BlendExample) => {
    console.log('🎯 BlendShowcase: 应用参数按钮被点击:', example.title);
    console.log('📦 传递的参数:', example.apiParams);
    
    if (onApplyParams && example.apiParams) {
      onApplyParams(example.apiParams);
    }
  };

  const handleBaseImageChange = (exampleIndex: number, direction: 'prev' | 'next') => {
    const currentIndex = currentBaseIndex[exampleIndex] || 0;
    const totalImages = examples[exampleIndex].baseImages.length;

    let newIndex: number;
    if (direction === 'next') {
      newIndex = (currentIndex + 1) % totalImages;
    } else {
      newIndex = currentIndex === 0 ? totalImages - 1 : currentIndex - 1;
    }
    
    setCurrentBaseIndex(prev => ({
      ...prev,
      [exampleIndex]: newIndex
    }));
  };

  const handleOverlayImageChange = (exampleIndex: number, direction: 'prev' | 'next') => {
    const currentIndex = currentOverlayIndex[exampleIndex] || 0;
    const totalImages = examples[exampleIndex].overlayImages.length;

    let newIndex: number;
    if (direction === 'next') {
      newIndex = (currentIndex + 1) % totalImages;
    } else {
      newIndex = currentIndex === 0 ? totalImages - 1 : currentIndex - 1;
    }
    
    setCurrentOverlayIndex(prev => ({
      ...prev,
      [exampleIndex]: newIndex
    }));
  };

  return (
    <>
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        {/* 标题和描述 */}
        <Typography variant="h4" component="h2" gutterBottom sx={{ 
          textAlign: 'center',
          color: 'primary.main',
          fontWeight: 'bold',
          mb: 2
        }}>
          {title}
        </Typography>
        
        <Typography variant="body1" color="text.secondary" sx={{ 
          textAlign: 'center',
          mb: 3,
          maxWidth: '800px',
          mx: 'auto'
        }}>
          {description}
        </Typography>

        {/* 显示模式切换 */}
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
          <FormControlLabel
            control={
              <Switch
                checked={enableLargeDisplay}
                onChange={(e) => setEnableLargeDisplay(e.target.checked)}
                color="primary"
              />
            }
            label="大图显示模式"
          />
        </Box>

        {/* 示例网格 */}
        <Grid container spacing={3}>
          {examples.map((example, index) => {
            const currentBaseIdx = currentBaseIndex[index] || 0;
            const currentOverlayIdx = currentOverlayIndex[index] || 0;
            
            return (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <BlendExampleCard
                  example={example}
                  index={index}
                  currentBaseIndex={currentBaseIdx}
                  currentOverlayIndex={currentOverlayIdx}
                  onBaseImageChange={(direction) => handleBaseImageChange(index, direction)}
                  onOverlayImageChange={(direction) => handleOverlayImageChange(index, direction)}
                  onImageClick={handleImageClick}
                  onApplyParams={onApplyParams ? handleApplyParams : undefined}
                  enableLargeDisplay={enableLargeDisplay}
                />
              </Grid>
            );
          })}
        </Grid>
      </Paper>

      {/* 图片画廊 */}
      <ImageGallery
        images={galleryImages}
        currentIndex={currentImageIndex}
        open={galleryOpen}
        onClose={handleCloseGallery}
        onIndexChange={setCurrentImageIndex}
        showNavigation={true}
        showDownload={true}
        showCounter={true}
      />
    </>
  );
};
