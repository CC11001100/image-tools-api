import React, { useState } from 'react';
import { Box, IconButton, Typography } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import { PhoneFrame } from './PhoneFrameComponents';

interface MultiImagePhoneFrameProps {
  images: string[];
  title: string;
  onImageClick: (imageSrc: string, title: string) => void;
  scale?: number;
  maxWidth?: string;
  showNotch?: boolean;
  showHomeButton?: boolean;
}

export const MultiImagePhoneFrame: React.FC<MultiImagePhoneFrameProps> = ({
  images,
  title,
  onImageClick,
  scale = 2.0,
  maxWidth = "100%",
  showNotch = true,
  showHomeButton = false,
}) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const handlePrevImage = (e: React.MouseEvent) => {
    e.stopPropagation(); // 阻止事件冒泡，避免触发图片点击
    setCurrentImageIndex((prev) => (prev === 0 ? images.length - 1 : prev - 1));
  };

  const handleNextImage = (e: React.MouseEvent) => {
    e.stopPropagation(); // 阻止事件冒泡，避免触发图片点击
    setCurrentImageIndex((prev) => (prev === images.length - 1 ? 0 : prev + 1));
  };

  const currentImage = images[currentImageIndex];

  return (
    <Box sx={{
      position: 'relative',
      cursor: 'pointer',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      p: 0
    }} onClick={() => onImageClick(currentImage, title)}>
      <PhoneFrame
        scale={scale}
        maxWidth={maxWidth}
        showNotch={showNotch}
        showHomeButton={showHomeButton}
      >
        {/* 图片容器 */}
        <Box sx={{
          position: 'relative',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          {/* 图片 */}
          <img
            src={currentImage}
            alt={title}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'contain',
              transition: 'opacity 0.2s',
            }}
          />

          {/* 图片计数器 - 显示在屏幕内部顶部，避开状态栏 */}
          {images.length > 1 && (
            <Typography
              variant="caption"
              sx={{
                position: 'absolute',
                top: 38, // 从8px调整到38px，向下移动30px
                left: '50%',
                transform: 'translateX(-50%)',
                backgroundColor: 'rgba(0,0,0,0.6)',
                color: 'white',
                px: 1,
                py: 0.5,
                borderRadius: 1,
                fontSize: '0.7rem',
                zIndex: 10
              }}
            >
              {title} {currentImageIndex + 1}/{images.length}
            </Typography>
          )}

          {/* 左侧切换按钮 - 显示在屏幕内部左侧 */}
          {images.length > 1 && (
            <IconButton
              onClick={handlePrevImage}
              sx={{
                position: 'absolute',
                left: 8,
                top: '50%',
                transform: 'translateY(-50%)',
                backgroundColor: 'rgba(0,0,0,0.5)',
                color: 'white',
                width: 32,
                height: 32,
                zIndex: 10,
                '&:hover': {
                  backgroundColor: 'rgba(0,0,0,0.7)'
                },
              }}
            >
              <ArrowBackIcon sx={{ fontSize: 16 }} />
            </IconButton>
          )}

          {/* 右侧切换按钮 - 显示在屏幕内部右侧 */}
          {images.length > 1 && (
            <IconButton
              onClick={handleNextImage}
              sx={{
                position: 'absolute',
                right: 8,
                top: '50%',
                transform: 'translateY(-50%)',
                backgroundColor: 'rgba(0,0,0,0.5)',
                color: 'white',
                width: 32,
                height: 32,
                zIndex: 10,
                '&:hover': {
                  backgroundColor: 'rgba(0,0,0,0.7)'
                },
              }}
            >
              <ArrowForwardIcon sx={{ fontSize: 16 }} />
            </IconButton>
          )}
        </Box>
      </PhoneFrame>
    </Box>
  );
};

export default MultiImagePhoneFrame;
