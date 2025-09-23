/**
 * 请求格式指南组件
 */

import React from 'react';
import {
  Typography,
  Box,
} from '@mui/material';

export const RequestFormatGuide: React.FC = () => {
  return (
    <>
      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
        * file和image_url参数二选一，不能同时使用
      </Typography>

      <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
        请求格式说明
      </Typography>
      <Typography variant="subtitle2" gutterBottom>
        文件上传模式：
      </Typography>
      <Box
        component="pre"
        sx={{
          backgroundColor: 'grey.100',
          p: 2,
          borderRadius: 1,
          mb: 2,
          fontSize: '0.875rem',
        }}
      >
{`POST /api/v1/example
Content-Type: multipart/form-data

file: [图片文件]
param1: value1
param2: value2`}
      </Box>

      <Typography variant="subtitle2" gutterBottom>
        URL模式：
      </Typography>
      <Box
        component="pre"
        sx={{
          backgroundColor: 'grey.100',
          p: 2,
          borderRadius: 1,
          mb: 2,
          fontSize: '0.875rem',
        }}
      >
{`POST /api/v1/example-by-url
Content-Type: application/json

{
  "image_url": "https://example.com/image.jpg",
  "param1": "value1",
  "param2": "value2"
}`}
      </Box>

      <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
        最佳实践
      </Typography>
      <Typography variant="body2" gutterBottom>
        1. 图片上传建议：
      </Typography>
      <ul>
        <li>推荐使用文件上传模式处理本地图片</li>
        <li>使用URL模式处理网络图片</li>
        <li>支持的图片格式：JPEG、PNG、WebP、GIF</li>
        <li>建议图片大小不超过10MB</li>
      </ul>

      <Typography variant="body2" gutterBottom>
        2. 参数设置建议：
      </Typography>
      <ul>
        <li>设置合适的参数值，避免过度处理</li>
        <li>注意参数之间的依赖关系</li>
        <li>使用默认值作为起点逐步调整</li>
      </ul>

      <Typography variant="body2" gutterBottom>
        3. 性能优化建议：
      </Typography>
      <ul>
        <li>可以预先压缩大图片</li>
        <li>批量处理时建议使用URL模式</li>
        <li>合理设置输出质量参数</li>
      </ul>

      <Typography variant="body2" gutterBottom>
        4. 错误处理建议：
      </Typography>
      <ul>
        <li>实现错误重试机制</li>
        <li>添加超时处理</li>
        <li>做好用户提示</li>
      </ul>
    </>
  );
};
