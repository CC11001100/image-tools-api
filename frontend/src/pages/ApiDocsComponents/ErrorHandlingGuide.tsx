/**
 * 错误处理指南组件
 */

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
} from '@mui/material';

export const ErrorHandlingGuide: React.FC = () => {
  return (
    <>
      <Typography variant="h6" gutterBottom>
        错误处理
      </Typography>
      <Typography variant="body2" paragraph>
        当API调用失败时，将返回对应的HTTP状态码和JSON格式的错误信息：
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
{`{
  "detail": "错误信息描述"
}`}
      </Box>

      <Typography variant="subtitle2" gutterBottom sx={{ mt: 3 }}>
        常见错误码说明：
      </Typography>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>状态码</strong></TableCell>
              <TableCell><strong>说明</strong></TableCell>
              <TableCell><strong>可能原因</strong></TableCell>
              <TableCell><strong>处理建议</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>400</TableCell>
              <TableCell>请求参数错误</TableCell>
              <TableCell>参数格式不正确、必需参数缺失等</TableCell>
              <TableCell>检查参数格式、必需参数是否提供、参数值是否在有效范围内</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>404</TableCell>
              <TableCell>资源不存在</TableCell>
              <TableCell>URL地址错误、图片不存在等</TableCell>
              <TableCell>检查URL地址是否正确、图片是否存在</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>415</TableCell>
              <TableCell>不支持的媒体类型</TableCell>
              <TableCell>上传了不支持的图片格式</TableCell>
              <TableCell>检查上传的图片格式是否支持、Content-Type是否正确设置</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>422</TableCell>
              <TableCell>处理失败</TableCell>
              <TableCell>图片处理过程中出错</TableCell>
              <TableCell>检查图片大小、分辨率是否符合要求，调整参数后重试</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>500</TableCell>
              <TableCell>服务器错误</TableCell>
              <TableCell>服务器内部错误</TableCell>
              <TableCell>请稍后重试或联系管理员</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};
