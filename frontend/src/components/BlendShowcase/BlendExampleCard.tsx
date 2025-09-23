import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Box,
} from '@mui/material';
import { BlendExample } from './types';
import { ImageSelector } from './ImageSelector';
import { ResultImage } from './ResultImage';

interface BlendExampleCardProps {
  example: BlendExample;
  index: number;
  currentBaseIndex: number;
  currentOverlayIndex: number;
  onBaseImageChange: (direction: 'prev' | 'next') => void;
  onOverlayImageChange: (direction: 'prev' | 'next') => void;
  onImageClick: (src: string, title: string) => void;
  onApplyParams?: (example: BlendExample) => void;
  enableLargeDisplay?: boolean;
}

export const BlendExampleCard: React.FC<BlendExampleCardProps> = ({
  example,
  index,
  currentBaseIndex,
  currentOverlayIndex,
  onBaseImageChange,
  onOverlayImageChange,
  onImageClick,
  onApplyParams,
  enableLargeDisplay = false,
}) => {
  const currentBaseImage = example.baseImages[currentBaseIndex];
  const currentOverlayImage = example.overlayImages[currentOverlayIndex];
  const currentResultImage = example.resultImages[currentBaseIndex * example.overlayImages.length + currentOverlayIndex];

  // 处理参数显示
  const getDisplayParams = () => {
    if (!example.apiParams) return [];
    
    return Object.entries(example.apiParams)
      .filter(([key, value]) => key !== 'base_image' && key !== 'overlay_image')
      .map(([key, value]) => ({
        label: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        value: typeof value === 'object' ? JSON.stringify(value) : String(value)
      }));
  };

  const displayParams = getDisplayParams();

  return (
    <Card 
      elevation={3} 
      sx={{ 
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'all 0.3s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 6
        }
      }}
    >
      <CardContent sx={{ 
        p: 1.5, 
        display: 'flex', 
        flexDirection: 'column', 
        height: '100%',
        '&:last-child': { pb: 1.5 }
      }}>
        {/* 标题和描述 */}
        <Typography variant="h6" component="h3" gutterBottom sx={{ 
          fontSize: '1rem',
          fontWeight: 'bold',
          color: 'primary.main',
          textAlign: 'center',
          mb: 1
        }}>
          {example.title}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ 
          mb: 2, 
          textAlign: 'center',
          fontSize: '0.8rem',
          lineHeight: 1.3
        }}>
          {example.description}
        </Typography>

        {/* 图片展示区域 */}
        <Box sx={{ mb: 2 }}>
          {/* 基础图片展示区域 */}
          <ImageSelector
            images={example.baseImages}
            currentIndex={currentBaseIndex}
            onImageChange={onBaseImageChange}
            onImageClick={onImageClick}
            title="基础图"
            type="base"
            enableLargeDisplay={enableLargeDisplay}
          />

          {/* 叠加图片展示区域 */}
          <ImageSelector
            images={example.overlayImages}
            currentIndex={currentOverlayIndex}
            onImageChange={onOverlayImageChange}
            onImageClick={onImageClick}
            title="叠加图"
            type="overlay"
            enableLargeDisplay={enableLargeDisplay}
          />
          
          {/* 混合结果 */}
          <ResultImage
            image={currentResultImage}
            title={example.title}
            onImageClick={onImageClick}
            enableLargeDisplay={enableLargeDisplay}
          />
        </Box>

        {/* API参数显示 */}
        {displayParams.length > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="caption" color="text.secondary" sx={{ 
              display: 'block', 
              mb: 1,
              fontWeight: 'bold'
            }}>
              API参数:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {displayParams.map((param, paramIndex) => (
                <Chip
                  key={paramIndex}
                  label={`${param.label}: ${param.value}`}
                  size="small"
                  variant="outlined"
                  color="secondary"
                  sx={{ fontSize: '0.7rem' }}
                />
              ))}
            </Box>
          </Box>
        )}

        {/* 应用参数按钮 */}
        {onApplyParams && example.apiParams && (
          <Button
            size="small"
            variant="contained"
            color="secondary"
            fullWidth
            onClick={() => onApplyParams(example)}
            sx={{ 
              fontSize: '0.75rem',
              mt: 'auto'
            }}
          >
            应用参数
          </Button>
        )}
      </CardContent>
    </Card>
  );
};
