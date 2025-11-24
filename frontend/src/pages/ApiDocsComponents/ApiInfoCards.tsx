/**
 * API信息卡片组件
 */

import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Link,
  Button,
  Box,
  Chip,
} from '@mui/material';
import CalculateIcon from '@mui/icons-material/Calculate';
import { API_BASE_URL } from '../../config/constants';
import { apiEndpoints } from '../../config/apiEndpoints';

export const ApiInfoCards: React.FC = () => {
  return (
    <Grid container spacing={3} sx={{ mb: 4 }}>
      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              API 基础信息
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>基础URL：</strong> <code>{API_BASE_URL}</code>
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>API版本：</strong> <code>v1</code>
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>认证方式：</strong> API Token
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              在线调试
            </Typography>
            <Typography variant="body2" paragraph>
              使用Swagger UI在线测试所有API接口：
            </Typography>
            <Link href={`${API_BASE_URL}/docs`} target="_blank" rel="noopener">
              {API_BASE_URL}/docs
            </Link>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              接口统计
            </Typography>
            <Typography variant="body2">
              <strong>总接口数：</strong> {apiEndpoints.length * 2} 个
            </Typography>
            <Typography variant="body2">
              <strong>文件上传接口：</strong> {apiEndpoints.length} 个
            </Typography>
            <Typography variant="body2">
              <strong>URL输入接口：</strong> {apiEndpoints.length} 个
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={3}>
        <Card sx={{ bgcolor: 'primary.50', borderColor: 'primary.main', borderWidth: 2, borderStyle: 'solid' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              💰 计费说明
            </Typography>
            <Typography variant="body2" paragraph>
              所有API接口按使用量计费，费用透明公开
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Chip label="基础: 100 Token/次" size="small" sx={{ mb: 1, mr: 1 }} />
              <Chip label="下载: 100 Token/MB" size="small" color="warning" sx={{ mb: 1, mr: 1 }} />
              <Chip label="上传: 50 Token/MB" size="small" color="success" sx={{ mb: 1 }} />
            </Box>
            <Button
              variant="contained"
              size="small"
              fullWidth
              startIcon={<CalculateIcon />}
              href="https://token-calc.aigchub.vip/"
              target="_blank"
              rel="noopener noreferrer"
            >
              Token计算器
            </Button>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};
