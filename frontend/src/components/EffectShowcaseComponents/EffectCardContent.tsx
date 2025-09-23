/**
 * 效果卡片内容组件
 */

import React from 'react';
import {
  CardContent,
  Typography,
  Divider,
  Box,
  Chip,
  Button,
} from '@mui/material';
import { EffectExample, MultiImageEffectExample } from '../../types/api';

interface EffectCardContentProps {
  example: EffectExample | MultiImageEffectExample;
  onApplyParams?: (example: EffectExample | MultiImageEffectExample) => void;
}

const EffectCardContent: React.FC<EffectCardContentProps> = ({
  example,
  onApplyParams,
}) => {
  const handleApplyParams = () => {
    if (onApplyParams) {
      onApplyParams(example);
    }
  };

  return (
    <CardContent sx={{ 
      flexGrow: 1, 
      pt: 2,
      display: 'flex',
      flexDirection: 'column',
      gap: 1
    }}>
      <Typography variant="h6" gutterBottom sx={{ 
        fontSize: '1rem',
        lineHeight: 1.3,
        mb: 1
      }}>
        {example.title}
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ 
        fontSize: '0.875rem',
        lineHeight: 1.4,
        mb: 1
      }}>
        {example.description}
      </Typography>
      <Divider sx={{ my: 1 }} />
      <Box sx={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: 0.5, 
        mb: 2,
        minHeight: '2rem'
      }}>
        {example.parameters.map((param, paramIndex) => (
          <Chip
            key={paramIndex}
            label={`${param.label}: ${param.value}`}
            size="small"
            variant="outlined"
            color="primary"
            sx={{ fontSize: '0.7rem' }}
          />
        ))}
      </Box>
      {onApplyParams && example.apiParams && (
        <Button
          size="small"
          variant="contained"
          color="primary"
          fullWidth
          onClick={handleApplyParams}
          sx={{ 
            fontSize: '0.75rem',
            mt: 'auto'
          }}
        >
          应用参数
        </Button>
      )}
    </CardContent>
  );
};

export default EffectCardContent;
