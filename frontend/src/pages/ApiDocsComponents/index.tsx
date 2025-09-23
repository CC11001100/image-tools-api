/**
 * API文档页面 - 重构版本
 * 将原来的418行大文件拆分为多个小组件，提高可维护性
 */

import React from 'react';
import {
  Typography,
  Box,
  Paper,
  Tabs,
  Tab,
  Alert,
} from '@mui/material';
import { TabPanel } from './TabPanel';
import { ApiInfoCards } from './ApiInfoCards';
import { ApiEndpointsTable } from './ApiEndpointsTable';
import { CommonParametersTable } from './CommonParametersTable';
import { RequestFormatGuide } from './RequestFormatGuide';
import { ErrorHandlingGuide } from './ErrorHandlingGuide';

export const ApiDocs: React.FC = () => {
  const [tabValue, setTabValue] = React.useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        API 文档
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        图像处理工具完整的API接口文档。所有接口都支持文件上传和URL输入两种方式。
      </Typography>

      <Alert severity="info" sx={{ mb: 4 }}>
        <Typography variant="subtitle2" gutterBottom>
          <strong>重要说明：</strong>
        </Typography>
        <Typography variant="body2">
          所有API接口都提供两种调用方式：
          <br />• <strong>文件上传模式</strong>：使用原始端点路径，通过multipart/form-data格式上传本地图片文件
          <br />• <strong>URL模式</strong>：使用带 <code>-by-url</code> 后缀的端点路径，通过application/json格式传入图片URL
        </Typography>
      </Alert>

      <ApiInfoCards />

      <Paper elevation={3}>
        <Tabs value={tabValue} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
          <Tab label="接口列表" />
          <Tab label="通用说明" />
          <Tab label="错误处理" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <ApiEndpointsTable />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <CommonParametersTable />
          <RequestFormatGuide />
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <ErrorHandlingGuide />
        </TabPanel>
      </Paper>
    </Box>
  );
};
