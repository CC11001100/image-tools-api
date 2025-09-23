/**
 * 尺寸对比显示组件
 */

import React from 'react';
import { Box } from '@mui/material';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import { EffectExample, MultiImageEffectExample } from '../../types/api';
import { getImageStyle, getImageDimensionsText } from './utils';

interface SizeComparisonDisplayProps {
  example: EffectExample | MultiImageEffectExample;
  showOriginalSize: boolean;
  onImageClick: (imageSrc: string, imageTitle: string) => void;
}

const SizeComparisonDisplay: React.FC<SizeComparisonDisplayProps> = ({
  example,
  showOriginalSize,
  onImageClick,
}) => {
  return (
    <Box 
      sx={{ position: 'relative', cursor: 'pointer' }} 
      onClick={() => onImageClick(example.processedImage, example.title)}
    >
      <Box sx={{
        display: 'flex',
        ...(showOriginalSize ? {
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: 'auto',
          pb: 3
        } : {
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: 100,
          maxHeight: 300,
          pb: 3
        }),
        backgroundColor: '#f8f9fa',
        p: 2,
        borderRadius: 1,
        position: 'relative'
      }}>
        <img
          src={example.processedImage}
          alt={example.title}
          style={getImageStyle(example, showOriginalSize)}
        />
      </Box>
      
      <Box sx={{
        position: 'absolute',
        bottom: 8,
        left: 8,
        bgcolor: 'rgba(76, 175, 80, 0.9)',
        color: 'white',
        px: 1,
        py: 0.5,
        borderRadius: 1,
        fontSize: '0.8rem',
        fontWeight: 'bold',
        zIndex: 2,
        boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
      }}>
        {getImageDimensionsText(example)}
      </Box>
      
      <Box sx={{
        position: 'absolute',
        top: 8,
        right: 8,
        backgroundColor: 'rgba(0,0,0,0.6)',
        color: 'white',
        borderRadius: '50%',
        p: 0.5,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 3,
        transition: 'all 0.2s ease-in-out',
        '&:hover': {
          backgroundColor: 'rgba(0,0,0,0.8)',
          transform: 'scale(1.1)'
        }
      }}>
        <ZoomInIcon fontSize="small" />
      </Box>
    </Box>
  );
};

export default SizeComparisonDisplay;
