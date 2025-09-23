/**
 * 前后对比显示组件
 */

import React from 'react';
import { Box, Typography } from '@mui/material';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import PhoneFrame from '../PhoneFrame';
import MultiImagePhoneFrame from '../MultiImagePhoneFrame';
import { EffectExample, MultiImageEffectExample } from '../../types/api';

interface BeforeAfterDisplayProps {
  example: EffectExample | MultiImageEffectExample;
  originalImage?: string;
  onImageClick: (imageSrc: string, imageTitle: string) => void;
}

const BeforeAfterDisplay: React.FC<BeforeAfterDisplayProps> = ({
  example,
  originalImage,
  onImageClick,
}) => {
  // 检查是否为多图示例
  const isMultiImage = 'originalImages' in example;
  const originalImages = isMultiImage
    ? (example as MultiImageEffectExample).originalImages
    : [(example as EffectExample).originalImage || originalImage || ''];

  return (
    <Box sx={{
      border: '2px solid rgba(25, 118, 210, 0.15)',
      borderRadius: '40px 40px 0 0',
      overflow: 'hidden',
      backgroundColor: 'rgba(25, 118, 210, 0.02)'
    }}>
      {/* 原图部分 */}
      {originalImages.length > 1 ? (
        // 多图显示
        <MultiImagePhoneFrame
          images={originalImages}
          title="原图"
          onImageClick={onImageClick}
          scale={2.0}
          maxWidth="100%"
          showNotch={true}
          showHomeButton={false}
        />
      ) : (
        // 单图显示
        <Box sx={{
          position: 'relative',
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          p: 0
        }} onClick={() => onImageClick(originalImages[0] || '', '原图')}>
          <PhoneFrame
            scale={2.0}
            maxWidth="100%"
            showNotch={true}
            showHomeButton={false}
          >
            <img
              src={originalImages[0] || ''}
              alt="原图"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'contain',
                transition: 'opacity 0.2s',
              }}
            />
          </PhoneFrame>
          <Box
            sx={{
              position: 'absolute',
              top: 8,
              left: 8,
              backgroundColor: 'rgba(25, 118, 210, 0.9)',
              color: 'white',
              px: 1,
              py: 0.5,
              borderRadius: 1,
              fontSize: '0.7rem',
              fontWeight: 'bold',
              zIndex: 10,
              boxShadow: '0 1px 3px rgba(0,0,0,0.2)'
            }}
          >
            原图
          </Box>
          <Box
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              backgroundColor: 'rgba(0,0,0,0.6)',
              color: 'white',
              borderRadius: '50%',
              p: 0.3,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 10,
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
      )}
      
      {/* 箭头分隔 */}
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          py: 2,
          backgroundColor: 'rgba(25, 118, 210, 0.1)',
          borderTop: '2px solid rgba(25, 118, 210, 0.2)',
          borderBottom: '2px solid rgba(25, 118, 210, 0.2)',
          position: 'relative'
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
            color: 'primary.main',
            fontSize: '0.9rem'
          }}>
            ⬇️ {example.title}
          </Typography>
        </Box>
      </Box>
      
      {/* 处理后图片 */}
      <Box sx={{
        position: 'relative',
        cursor: 'pointer',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        p: 0
      }} onClick={() => onImageClick(example.processedImage, example.title)}>
        <PhoneFrame
          scale={2.0}
          maxWidth="100%"
          showNotch={true}
          showHomeButton={false}
        >
          <img
            src={example.processedImage}
            alt={example.title}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'contain',
              transition: 'opacity 0.2s',
            }}
          />
        </PhoneFrame>
        <Box
          sx={{
            position: 'absolute',
            top: 8,
            left: 8,
            backgroundColor: 'rgba(76, 175, 80, 0.9)',
            color: 'white',
            px: 1,
            py: 0.5,
            borderRadius: 1,
            fontSize: '0.7rem',
            fontWeight: 'bold',
            zIndex: 10,
            boxShadow: '0 1px 3px rgba(0,0,0,0.2)'
          }}
        >
          处理后
        </Box>
        <Box
          sx={{
            position: 'absolute',
            top: 8,
            right: 8,
            backgroundColor: 'rgba(0,0,0,0.6)',
            color: 'white',
            borderRadius: '50%',
            p: 0.3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 10,
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

export default BeforeAfterDisplay;
