import React from 'react';
import { Typography, Box } from '@mui/material';
import { API_BASE_URL } from '../../config/constants';

export const ApiExamples: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        使用示例
      </Typography>
      
      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        文件上传模式
      </Typography>
      <Box 
        component="pre" 
        sx={{ 
          backgroundColor: 'grey.100',
          p: 2,
          borderRadius: 1,
          overflow: 'auto',
          fontSize: '0.875rem',
          mb: 3,
        }}
      >
{`# 基础滤镜应用
curl -X POST "${API_BASE_URL}/filter/apply" \\
  -F "file=@image.jpg" \\
  -F "filter_type=grayscale" \\
  -F "intensity=1.0"

# 添加水印
curl -X POST "${API_BASE_URL}/watermark/add" \\
  -F "file=@image.jpg" \\
  -F "text=Copyright 2024" \\
  -F "position=bottom-right" \\
  -F "opacity=0.5"

# 调整大小
curl -X POST "${API_BASE_URL}/resize/resize" \\
  -F "file=@image.jpg" \\
  -F "width=800" \\
  -F "height=600" \\
  -F "keep_aspect_ratio=true"`}
      </Box>

      <Typography variant="h6" gutterBottom>
        URL输入模式
      </Typography>
      <Box 
        component="pre" 
        sx={{ 
          backgroundColor: 'grey.100',
          p: 2,
          borderRadius: 1,
          overflow: 'auto',
          fontSize: '0.875rem',
          mb: 3,
        }}
      >
{`# 基础滤镜应用（URL模式）
curl -X POST "${API_BASE_URL}/filter/apply-url" \\
  -F "image_url=https://example.com/image.jpg" \\
  -F "filter_type=grayscale" \\
  -F "intensity=1.0"

# 添加水印（URL模式）
curl -X POST "${API_BASE_URL}/watermark/add-url" \\
  -F "image_url=https://example.com/image.jpg" \\
  -F "text=Copyright 2024" \\
  -F "position=bottom-right" \\
  -F "opacity=0.5"

# 调整大小（URL模式）
curl -X POST "${API_BASE_URL}/resize/resize-url" \\
  -F "image_url=https://example.com/image.jpg" \\
  -F "width=800" \\
  -F "height=600" \\
  -F "keep_aspect_ratio=true"`}
      </Box>


    </Box>
  );
}; 