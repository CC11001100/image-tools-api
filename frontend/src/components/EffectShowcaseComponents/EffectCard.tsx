/**
 * 效果卡片组件
 */

import React from 'react';
import { Card } from '@mui/material';
import SizeComparisonDisplay from './SizeComparisonDisplay';
import BeforeAfterDisplay from './BeforeAfterDisplay';
import EffectCardContent from './EffectCardContent';
import { EffectCardProps } from './types';

const EffectCard: React.FC<EffectCardProps> = ({
  example,
  originalImage,
  enableSizeComparison,
  showOriginalSize,
  onImageClick,
  onApplyParams,
}) => {
  return (
    <Card sx={{
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      minHeight: '1200px',
      borderRadius: '40px 40px 0 0',
      overflow: 'hidden',
      transition: 'all 0.2s ease-in-out',
      '&:hover': {
        transform: 'translateY(-2px)',
        boxShadow: 3
      }
    }}>
      {enableSizeComparison ? (
        <SizeComparisonDisplay
          example={example}
          showOriginalSize={showOriginalSize}
          onImageClick={onImageClick}
        />
      ) : (
        <BeforeAfterDisplay
          example={example}
          originalImage={originalImage}
          onImageClick={onImageClick}
        />
      )}
      
      <EffectCardContent
        example={example}
        onApplyParams={onApplyParams}
      />
    </Card>
  );
};

export default EffectCard;
