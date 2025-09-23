/**
 * 页脚组件
 */

import React from 'react';
import {
  Box,
  Typography,
} from '@mui/material';

const Footer: React.FC = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 1,
        px: 2,
        mt: 'auto',
        backgroundColor: '#f5f5f5',
        borderTop: '1px solid #e0e0e0',
        textAlign: 'center',
      }}
    >
      <Typography 
        variant="caption" 
        color="text.secondary"
        sx={{ fontSize: '0.75rem' }}
      >
        京ICP备2025135212号-2
      </Typography>
    </Box>
  );
};

export default Footer;
