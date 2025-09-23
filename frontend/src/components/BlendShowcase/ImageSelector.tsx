import React from 'react';
import {
  Box,
  Typography,
  IconButton,
  CardMedia,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  ArrowForward as ArrowForwardIcon,
  ZoomIn as ZoomInIcon,
  Layers as LayersIcon,
  Palette as BlendingModeIcon,
} from '@mui/icons-material';

interface ImageSelectorProps {
  images: string[];
  currentIndex: number;
  onImageChange: (direction: 'prev' | 'next') => void;
  onImageClick: (src: string, title: string) => void;
  title: string;
  type: 'base' | 'overlay';
  enableLargeDisplay?: boolean;
}

export const ImageSelector: React.FC<ImageSelectorProps> = ({
  images,
  currentIndex,
  onImageChange,
  onImageClick,
  title,
  type,
  enableLargeDisplay = false,
}) => {
  const currentImage = images[currentIndex];
  const isBase = type === 'base';
  const Icon = isBase ? LayersIcon : BlendingModeIcon;
  const backgroundColor = isBase ? 'rgba(25, 118, 210, 0.05)' : 'rgba(255, 152, 0, 0.05)';
  const borderColor = isBase ? 'rgba(25, 118, 210, 0.3)' : 'rgba(255, 152, 0, 0.3)';
  const buttonColor = isBase ? 'rgba(25, 118, 210, 0.1)' : 'rgba(255, 152, 0, 0.1)';
  const buttonHoverColor = isBase ? 'rgba(25, 118, 210, 0.2)' : 'rgba(255, 152, 0, 0.2)';

  return (
    <Box sx={{ 
      position: 'relative',
      backgroundColor,
      p: 1
    }}>
      {/* 标题栏 */}
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        mb: 1,
        px: 1
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Icon sx={{ fontSize: 16, color: isBase ? 'primary.main' : 'warning.main' }} />
          <Typography variant="body2" sx={{ 
            fontWeight: 'bold',
            color: isBase ? 'primary.main' : 'warning.main',
            fontSize: '0.8rem'
          }}>
            {title} {currentIndex + 1}/{images.length}
          </Typography>
        </Box>
        
        {/* 图片切换按钮 */}
        {images.length > 1 && (
          <Box sx={{ display: 'flex', gap: 0.5 }}>
            <IconButton
              size="small"
              onClick={() => onImageChange('prev')}
              sx={{ 
                backgroundColor: buttonColor,
                '&:hover': { backgroundColor: buttonHoverColor },
                width: 24,
                height: 24
              }}
            >
              <ArrowBackIcon sx={{ fontSize: 14 }} />
            </IconButton>
            <IconButton
              size="small"
              onClick={() => onImageChange('next')}
              sx={{ 
                backgroundColor: buttonColor,
                '&:hover': { backgroundColor: buttonHoverColor },
                width: 24,
                height: 24
              }}
            >
              <ArrowForwardIcon sx={{ fontSize: 14 }} />
            </IconButton>
          </Box>
        )}
      </Box>
      
      {/* 图片显示 */}
      <Box sx={{ position: 'relative', cursor: 'pointer' }} onClick={() => onImageClick(currentImage, title)}>
        <CardMedia
          component="img"
          height={enableLargeDisplay ? "280" : "140"}
          image={currentImage}
          alt={title}
          sx={{ 
            transition: 'opacity 0.2s',
            '&:hover': { opacity: 0.8 },
            borderRadius: 1,
            border: `1px solid ${borderColor}`
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: 4,
            right: 4,
            backgroundColor: 'rgba(0,0,0,0.6)',
            color: 'white',
            borderRadius: '50%',
            p: 0.3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 3,
            transition: 'all 0.2s ease-in-out',
            '&:hover': {
              backgroundColor: 'rgba(0,0,0,0.8)',
              transform: 'scale(1.1)'
            }
          }}
        >
          <ZoomInIcon fontSize="small" />
        </Box>
      </Box>
    </Box>
  );
};
