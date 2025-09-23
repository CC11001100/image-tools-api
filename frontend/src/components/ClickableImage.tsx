import React, { useState } from 'react';
import {
  Tooltip,
  Box,
} from '@mui/material';
import {
  ZoomIn as ZoomInIcon,
} from '@mui/icons-material';
import { ImageGallery, GalleryImage } from './ImageGallery';

interface ClickableImageProps {
  src: string;
  alt: string;
  title?: string;
  style?: React.CSSProperties;
  className?: string;
  showZoomIcon?: boolean;
  downloadable?: boolean;
  downloadFileName?: string;
  maxDialogWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | false;
  // 支持图片列表的新属性
  images?: GalleryImage[];
  currentImageIndex?: number;
}

export const ClickableImage: React.FC<ClickableImageProps> = ({
  src,
  alt,
  title,
  style,
  className,
  showZoomIcon = true,
  downloadable = true,
  downloadFileName = 'image.jpg',
  maxDialogWidth = 'lg',
  images,
  currentImageIndex,
}) => {
  const [galleryOpen, setGalleryOpen] = useState(false);
  const [galleryIndex, setGalleryIndex] = useState(0);

  const handleImageClick = () => {
    if (images && images.length > 0) {
      // 如果有图片列表，查找当前图片的索引
      const index = images.findIndex(img => img.src === src);
      setGalleryIndex(index !== -1 ? index : (currentImageIndex || 0));
    } else {
      // 如果没有图片列表，创建单张图片的列表
      setGalleryIndex(0);
    }
    setGalleryOpen(true);
  };

  const handleCloseGallery = () => {
    setGalleryOpen(false);
  };

  // 构建图片列表
  const galleryImages: GalleryImage[] = images || [
    {
      src,
      alt,
      title: title || alt,
      downloadFileName,
    }
  ];

  const defaultStyle: React.CSSProperties = {
    cursor: 'pointer',
    transition: 'all 0.2s ease-in-out',
    borderRadius: '4px',
    ...style,
  };

  const hoverStyle: React.CSSProperties = {
    opacity: 0.8,
    transform: 'scale(1.02)',
    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
  };

  return (
    <>
      {/* 可点击的图片 */}
      <Box
        sx={{
          position: 'relative',
          display: 'inline-block',
          '&:hover': showZoomIcon ? {
            '& .zoom-overlay': {
              opacity: 1,
            }
          } : {},
          '&:hover img': hoverStyle,
        }}
      >
        <img
          src={src}
          alt={alt}
          style={defaultStyle}
          className={className}
          onClick={handleImageClick}
          loading="lazy"
        />
        
        {/* 放大镜图标覆盖层 */}
        {showZoomIcon && (
          <Box
            className="zoom-overlay"
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              backgroundColor: 'rgba(0, 0, 0, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              opacity: 0,
              transition: 'opacity 0.2s ease-in-out',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
            onClick={handleImageClick}
          >
            <Tooltip title="点击查看大图" placement="top">
              <ZoomInIcon
                sx={{
                  color: 'white',
                  fontSize: '2rem',
                  filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.5))',
                }}
              />
            </Tooltip>
          </Box>
        )}
      </Box>

      {/* 图片画廊 */}
      <ImageGallery
        images={galleryImages}
        currentIndex={galleryIndex}
        open={galleryOpen}
        onClose={handleCloseGallery}
        onIndexChange={setGalleryIndex}
        showNavigation={galleryImages.length > 1}
        showDownload={downloadable}
        showCounter={galleryImages.length > 1}
        maxDialogWidth={maxDialogWidth}
      />
    </>
  );
}; 