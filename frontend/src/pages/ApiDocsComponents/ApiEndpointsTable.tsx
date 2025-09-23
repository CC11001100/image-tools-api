/**
 * API端点表格组件
 */

import React from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material';
import { getGroupedEndpoints } from '../../config/apiEndpoints';

export const ApiEndpointsTable: React.FC = () => {
  const groupedEndpoints = getGroupedEndpoints();

  return (
    <>
      {Object.entries(groupedEndpoints).map(([category, endpoints]) => (
        <Box key={category} sx={{ mb: 4 }}>
          <Typography variant="h5" gutterBottom sx={{ px: 3, pt: 2 }}>
            {category}
          </Typography>
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell><strong>功能描述</strong></TableCell>
                  <TableCell><strong>请求方法</strong></TableCell>
                  <TableCell><strong>文件上传端点</strong></TableCell>
                  <TableCell><strong>URL输入端点</strong></TableCell>
                  <TableCell><strong>响应格式</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {endpoints.map((endpoint) => (
                  <TableRow key={endpoint.path}>
                    <TableCell>{endpoint.description}</TableCell>
                    <TableCell>
                      <Chip label={endpoint.method} color="primary" size="small" />
                    </TableCell>
                    <TableCell>
                      <code>{endpoint.path}</code>
                      <br />
                      <Typography variant="caption" color="text.secondary">
                        Content-Type: {endpoint.requestType.file}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <code>{endpoint.urlPath}</code>
                      <br />
                      <Typography variant="caption" color="text.secondary">
                        Content-Type: {endpoint.requestType.url}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <code>{endpoint.responseType}</code>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      ))}
    </>
  );
};
