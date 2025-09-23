/**
 * 通用参数表格组件
 */

import React from 'react';
import {
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material';

export const CommonParametersTable: React.FC = () => {
  return (
    <>
      <Typography variant="h6" gutterBottom>
        通用参数说明
      </Typography>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>参数名</strong></TableCell>
              <TableCell><strong>类型</strong></TableCell>
              <TableCell><strong>必需</strong></TableCell>
              <TableCell><strong>说明</strong></TableCell>
              <TableCell><strong>适用于</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell><code>file</code></TableCell>
              <TableCell>file</TableCell>
              <TableCell>
                <Chip label="必需*" size="small" color="error" />
              </TableCell>
              <TableCell>要处理的图片文件</TableCell>
              <TableCell>
                <Chip label="文件上传" size="small" color="success" />
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell><code>image_url</code></TableCell>
              <TableCell>string</TableCell>
              <TableCell>
                <Chip label="必需*" size="small" color="error" />
              </TableCell>
              <TableCell>要处理的图片URL地址</TableCell>
              <TableCell>
                <Chip label="URL模式" size="small" color="info" />
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell><code>quality</code></TableCell>
              <TableCell>number</TableCell>
              <TableCell>
                <Chip label="可选" size="small" />
              </TableCell>
              <TableCell>输出质量(10-100)，默认90</TableCell>
              <TableCell>
                <Chip label="通用" size="small" />
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell><code>output_format</code></TableCell>
              <TableCell>string</TableCell>
              <TableCell>
                <Chip label="可选" size="small" />
              </TableCell>
              <TableCell>输出格式(jpeg/png/webp)，默认与输入格式相同</TableCell>
              <TableCell>
                <Chip label="通用" size="small" />
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};
