import React from 'react';
import { 
  Paper, 
  Box, 
  Typography,
  Chip,
} from '@mui/material';

export const HeroBanner: React.FC = () => {
  return (
    <Paper
      sx={{
        position: 'relative',
        backgroundColor: 'grey.800',
        color: '#fff',
        mb: 4,
        background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
        p: 6,
      }}
    >
      <Box
        sx={{
          position: 'relative',
          p: { xs: 3, md: 6 },
        }}
      >
        <Typography component="h1" variant="h2" color="inherit" gutterBottom>
          图像处理工具
        </Typography>
        <Typography variant="h5" color="inherit" paragraph>
          一站式图像处理解决方案，支持水印添加、尺寸调整、滤镜应用等多种功能
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Chip 
            label="100+ API端点" 
            sx={{ mr: 1, backgroundColor: 'rgba(255,255,255,0.2)', color: 'white' }} 
          />
          <Chip 
            label="150+ 处理效果" 
            sx={{ mr: 1, backgroundColor: 'rgba(255,255,255,0.2)', color: 'white' }} 
          />
          <Chip 
            label="在线测试" 
            sx={{ backgroundColor: 'rgba(255,255,255,0.2)', color: 'white' }} 
          />
        </Box>
      </Box>
    </Paper>
  );
}; 