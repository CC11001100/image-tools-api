import React from 'react';
import {
  Box,
  Typography,
  CardMedia,
} from '@mui/material';
import {
  ZoomIn as ZoomInIcon,
} from '@mui/icons-material';

interface ResultImageProps {
  image: string;
  title: string;
  onImageClick: (src: string, title: string) => void;
  enableLargeDisplay?: boolean;
}

export const ResultImage: React.FC<ResultImageProps> = ({
  image,
  title,
  onImageClick,
  enableLargeDisplay = false,
}) => {
  return (
    <>
      {/* 混合过程分隔 */}
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          py: 1.5,
          backgroundColor: 'rgba(156, 39, 176, 0.1)',
          borderTop: '2px solid rgba(156, 39, 176, 0.2)',
          borderBottom: '2px solid rgba(156, 39, 176, 0.2)',
        }}
      >
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 1,
          backgroundColor: 'white',
          px: 2,
          py: 0.5,
          borderRadius: 2,
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <Typography variant="body2" sx={{ 
            fontWeight: 'bold',
            color: 'secondary.main',
            fontSize: '0.8rem'
          }}>
            ⬇️ 混合处理
          </Typography>
        </Box>
      </Box>
      
      {/* 混合结果 */}
      <Box sx={{ position: 'relative', cursor: 'pointer' }} onClick={() => onImageClick(image, title)}>
        <CardMedia
          component="img"
          height={enableLargeDisplay ? "280" : "140"}
          image={image}
          alt={title}
          sx={{ 
            transition: 'opacity 0.2s',
            '&:hover': { opacity: 0.8 }
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: 4,
            left: 4,
            backgroundColor: 'rgba(76, 175, 80, 0.9)',
            color: 'white',
            px: 1,
            py: 0.5,
            borderRadius: 1,
            fontSize: '0.7rem',
            fontWeight: 'bold',
            zIndex: 2,
            boxShadow: '0 1px 3px rgba(0,0,0,0.2)'
          }}
        >
          混合结果
        </Box>
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
    </>
  );
};
