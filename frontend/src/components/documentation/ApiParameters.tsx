import React from 'react';
import {
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Alert,
} from '@mui/material';

export const ApiParameters: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        通用参数说明
      </Typography>
      
      <TableContainer component={Paper} variant="outlined" sx={{ mt: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>参数名</TableCell>
              <TableCell>类型</TableCell>
              <TableCell>必需</TableCell>
              <TableCell>说明</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell><code>file</code></TableCell>
              <TableCell>file</TableCell>
              <TableCell>
                <Chip label="文件上传模式" size="small" color="primary" />
              </TableCell>
              <TableCell>要处理的图片文件</TableCell>
            </TableRow>
            <TableRow>
              <TableCell><code>image_url</code></TableCell>
              <TableCell>string</TableCell>
              <TableCell>
                <Chip label="URL模式" size="small" color="secondary" />
              </TableCell>
              <TableCell>要处理的图片URL地址</TableCell>
            </TableRow>
            <TableRow>
              <TableCell><code>quality</code></TableCell>
              <TableCell>number</TableCell>
              <TableCell>否</TableCell>
              <TableCell>输出质量 (10-100)，默认90</TableCell>
            </TableRow>
            <TableRow>
              <TableCell><code>output_format</code></TableCell>
              <TableCell>string</TableCell>
              <TableCell>否</TableCell>
              <TableCell>输出格式 (JPEG/PNG/WEBP等)</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      <Alert severity="warning" sx={{ mt: 3 }}>
        <Typography variant="subtitle2">
          <strong>注意事项：</strong>
        </Typography>
        <Typography variant="body2" component="div">
          <ul style={{ margin: '8px 0', paddingLeft: '20px' }}>
            <li>文件上传模式和URL模式不能同时使用</li>
            <li>URL必须是可公开访问的图片地址</li>
            <li>支持的图片格式：JPEG, PNG, GIF, BMP, WebP</li>
            <li>单个文件大小限制：10MB</li>
            <li>批量处理返回ZIP压缩包</li>
          </ul>
        </Typography>
      </Alert>
    </Box>
  );
}; 