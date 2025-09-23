/**
 * 效果展示组件 - 重构版本
 * 将原来的467行大文件拆分为多个小组件，提高可维护性
 */

import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Grid,
} from '@mui/material';
import { ImageGallery, GalleryImage } from '../ImageGallery';
import EffectCard from './EffectCard';
import { EffectShowcaseProps, GalleryState } from './types';

export const EffectShowcase: React.FC<EffectShowcaseProps> = ({
  title,
  description,
  examples,
  onApplyParams,
  showOriginal = true,
  originalImage,
  enableSizeComparison = false,
  showOriginalSize = false,
  enableLargeDisplay = false
}) => {
  // 状态管理
  const [galleryState, setGalleryState] = useState<GalleryState>({
    galleryOpen: false,
    currentImageIndex: 0,
    galleryImages: [],
  });

  // 处理图片点击
  const handleImageClick = (imageSrc: string, imageTitle: string) => {
    setGalleryState({
      galleryOpen: true,
      currentImageIndex: 0,
      galleryImages: [{
        src: imageSrc,
        alt: imageTitle,
        title: imageTitle,
        description: `${imageTitle} 预览图`
      }],
    });
  };

  // 处理画廊关闭
  const handleCloseGallery = () => {
    setGalleryState(prev => ({
      ...prev,
      galleryOpen: false,
    }));
  };

  // 处理应用参数
  const handleApplyParams = (example: any) => {
    if (onApplyParams && example.apiParams) {
      onApplyParams(example.apiParams);
    }
  };

  // 处理画廊索引变化
  const handleIndexChange = (index: number) => {
    setGalleryState(prev => ({
      ...prev,
      currentImageIndex: index,
    }));
  };

  return (
    <>
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          🎨 {title}
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          {description}
        </Typography>
        
        <Grid container spacing={3}>
          {examples.map((example, index) => (
            <Grid item xs={12} sm={12} md={6} lg={4} xl={3} key={index}>
              <EffectCard
                example={example}
                originalImage={originalImage}
                enableSizeComparison={enableSizeComparison}
                showOriginalSize={showOriginalSize}
                onImageClick={handleImageClick}
                onApplyParams={handleApplyParams}
              />
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* 图片画廊 */}
      <ImageGallery
        images={galleryState.galleryImages}
        currentIndex={galleryState.currentImageIndex}
        open={galleryState.galleryOpen}
        onClose={handleCloseGallery}
        onIndexChange={handleIndexChange}
        showNavigation={true}
        showDownload={true}
        showCounter={true}
      />
    </>
  );
};
