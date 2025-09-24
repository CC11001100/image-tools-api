/**
 * ImageGallery - 图片画廊组件
 * 用于展示图片集合，支持预览、导航、下载等功能
 */

import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  IconButton,
  Typography,
  Box,
  Button,
  Fade,
} from '@mui/material';
import {
  Close as CloseIcon,
  NavigateBefore as PrevIcon,
  NavigateNext as NextIcon,
  Download as DownloadIcon,
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
} from '@mui/icons-material';

// 类型定义
export interface GalleryImage {
  id?: string;
  url?: string;
  src: string;
  alt?: string;
  title?: string;
  description?: string;
  downloadFileName?: string;
}

export interface ImageGalleryProps {
  images: GalleryImage[];
  currentIndex?: number;
  open: boolean;
  onClose: () => void;
  onIndexChange?: (index: number) => void;
  showNavigation?: boolean;
  showDownload?: boolean;
  showCounter?: boolean;
  showZoom?: boolean;
  maxDialogWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | false;
}

const ImageGallery: React.FC<ImageGalleryProps> = ({
  images = [],
  currentIndex = 0,
  open,
  onClose,
  onIndexChange,
  showNavigation = true,
  showDownload = true,
  showCounter = true,
  showZoom = false,
  maxDialogWidth = false,
}) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(currentIndex);
  const [zoom, setZoom] = useState(1);
  const [imageLoaded, setImageLoaded] = useState(false);

  // 同步外部索引变化
  useEffect(() => {
    setCurrentImageIndex(currentIndex);
  }, [currentIndex]);

  // 重置状态当对话框打开时
  useEffect(() => {
    if (open) {
      setZoom(1);
      setImageLoaded(false);
    }
  }, [open]);

  // 处理索引变化
  const handleIndexChange = (newIndex: number) => {
    if (newIndex >= 0 && newIndex < images.length) {
      setCurrentImageIndex(newIndex);
      setImageLoaded(false);
      setZoom(1);
      if (onIndexChange) {
        onIndexChange(newIndex);
      }
    }
  };

  // 导航函数
  const goToPrevious = () => {
    const newIndex = currentImageIndex > 0 ? currentImageIndex - 1 : images.length - 1;
    handleIndexChange(newIndex);
  };

  const goToNext = () => {
    const newIndex = currentImageIndex < images.length - 1 ? currentImageIndex + 1 : 0;
    handleIndexChange(newIndex);
  };

  // 键盘导航
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (!open) return;

      switch (event.key) {
        case 'ArrowLeft':
          goToPrevious();
          break;
        case 'ArrowRight':
          goToNext();
          break;
        case 'Escape':
          onClose();
          break;
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    return () => document.removeEventListener('keydown', handleKeyPress);
  }, [open, currentImageIndex, images.length]);

  // 下载图片
  const handleDownload = () => {
    const currentImage = images[currentImageIndex];
    if (!currentImage) return;

    const link = document.createElement('a');
    link.href = currentImage.src;
    link.download = currentImage.downloadFileName || currentImage.title || `image-${currentImageIndex + 1}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // 缩放控制
  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.25, 3));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.25, 0.25));

  if (!images.length) return null;

  const currentImage = images[currentImageIndex];

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth={maxDialogWidth}
      fullWidth
      PaperProps={{
        sx: {
          backgroundColor: 'rgba(0, 0, 0, 0.9)',
          color: 'white',
          maxHeight: '100vh',
          margin: 0,
        }
      }}
    >
      <DialogContent sx={{ p: 0, position: 'relative', display: 'flex', flexDirection: 'column', height: '100vh' }}>
        {/* 顶部工具栏 */}
        <Box sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          zIndex: 2,
          background: 'linear-gradient(to bottom, rgba(0,0,0,0.7), transparent)',
          p: 2,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <Box>
            {showCounter && (
              <Typography variant="body2" sx={{ color: 'white' }}>
                {currentImageIndex + 1} / {images.length}
              </Typography>
            )}
            {currentImage?.title && (
              <Typography variant="h6" sx={{ color: 'white', mt: 0.5 }}>
                {currentImage.title}
              </Typography>
            )}
          </Box>

          <Box sx={{ display: 'flex', gap: 1 }}>
            {showZoom && (
              <>
                <IconButton onClick={handleZoomOut} sx={{ color: 'white' }}>
                  <ZoomOutIcon />
                </IconButton>
                <IconButton onClick={handleZoomIn} sx={{ color: 'white' }}>
                  <ZoomInIcon />
                </IconButton>
              </>
            )}
            {showDownload && (
              <IconButton onClick={handleDownload} sx={{ color: 'white' }}>
                <DownloadIcon />
              </IconButton>
            )}
            <IconButton onClick={onClose} sx={{ color: 'white' }}>
              <CloseIcon />
            </IconButton>
          </Box>
        </Box>

        {/* 图片显示区域 */}
        <Box sx={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          overflow: 'hidden'
        }}>
          {currentImage && (
            <Fade in={imageLoaded} timeout={300}>
              <img
                src={currentImage.src}
                alt={currentImage.alt || currentImage.title || '图片'}
                style={{
                  maxWidth: '100%',
                  maxHeight: '100%',
                  objectFit: 'contain',
                  transform: `scale(${zoom})`,
                  transition: 'transform 0.2s ease-in-out',
                  cursor: showZoom ? (zoom > 1 ? 'zoom-out' : 'zoom-in') : 'default'
                }}
                onLoad={() => setImageLoaded(true)}
                onClick={showZoom ? (zoom > 1 ? handleZoomOut : handleZoomIn) : undefined}
              />
            </Fade>
          )}
        </Box>

        {/* 导航按钮 */}
        {showNavigation && images.length > 1 && (
          <>
            <IconButton
              onClick={goToPrevious}
              sx={{
                position: 'absolute',
                left: 16,
                top: '50%',
                transform: 'translateY(-50%)',
                color: 'white',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                '&:hover': {
                  backgroundColor: 'rgba(0, 0, 0, 0.7)',
                }
              }}
            >
              <PrevIcon />
            </IconButton>

            <IconButton
              onClick={goToNext}
              sx={{
                position: 'absolute',
                right: 16,
                top: '50%',
                transform: 'translateY(-50%)',
                color: 'white',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                '&:hover': {
                  backgroundColor: 'rgba(0, 0, 0, 0.7)',
                }
              }}
            >
              <NextIcon />
            </IconButton>
          </>
        )}

        {/* 底部描述 */}
        {currentImage?.description && (
          <Box sx={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            background: 'linear-gradient(to top, rgba(0,0,0,0.7), transparent)',
            p: 2
          }}>
            <Typography variant="body2" sx={{ color: 'white', textAlign: 'center' }}>
              {currentImage.description}
            </Typography>
          </Box>
        )}
      </DialogContent>
    </Dialog>
  );
};

export { ImageGallery };
export default ImageGallery;
