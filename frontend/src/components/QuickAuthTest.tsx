import React from 'react';
import { Box, Button, Typography, Alert } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { setCookie, getCookie } from '../utils/cookieUtils';

const QuickAuthTest: React.FC = () => {
  const { isAuthenticated, user, refreshAuthStatus } = useAuth();
  
  // 您提供的JWT token
  const YOUR_JWT_TOKEN = 'eyJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOjEsInBob25lIjoiMTM3OTE0ODY5MzEiLCJuaWNrbmFtZSI6IkNDMTEwMDExMDAiLCJzdWIiOiIxMzc5MTQ4NjkzMSIsImlhdCI6MTc1MjgzNDA5NywiZXhwIjo0OTA2NDM0MDk3fQ.04ls9TXrOe_hLoboEOb9Zme9WLfgKdi40AlM7C7LGkXfRhfufYHmyTI4JPFSe8rZ_bvcwPR61rrkrtlZ-6Pn6Q';

  const handleSetCookie = () => {
    console.log('设置您的JWT token到cookie...');
    setCookie('jwt_token', YOUR_JWT_TOKEN, 7);
    console.log('Cookie已设置，刷新认证状态...');
    refreshAuthStatus();
  };

  const handleCheckCookie = () => {
    const token = getCookie('jwt_token');
    console.log('当前jwt_token cookie:', token);
    console.log('是否匹配您的token:', token === YOUR_JWT_TOKEN);
    console.log('所有cookies:', document.cookie);
  };

  const handleManualTest = () => {
    console.log('=== 手动测试JWT解析 ===');
    
    // 手动解析JWT
    try {
      const parts = YOUR_JWT_TOKEN.split('.');
      const payload = parts[1];
      const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
      const padded = base64.padEnd(base64.length + (4 - base64.length % 4) % 4, '=');
      const decoded = atob(padded);
      const parsed = JSON.parse(decoded);
      
      console.log('解析结果:', parsed);
      console.log('nickname:', parsed.nickname);
      console.log('过期时间:', new Date(parsed.exp * 1000).toLocaleString());
      console.log('是否过期:', parsed.exp < Math.floor(Date.now() / 1000));
    } catch (error) {
      console.error('手动解析失败:', error);
    }
  };

  return (
    <Box sx={{ p: 2, border: '1px solid #ccc', borderRadius: 1, mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        快速认证测试
      </Typography>
      
      <Alert severity={isAuthenticated ? "success" : "warning"} sx={{ mb: 2 }}>
        当前状态: {isAuthenticated ? `已登录 (${user?.nickname})` : '未登录'}
      </Alert>
      
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Button variant="contained" onClick={handleSetCookie}>
          设置您的JWT Token
        </Button>
        <Button variant="outlined" onClick={handleCheckCookie}>
          检查Cookie
        </Button>
        <Button variant="outlined" onClick={handleManualTest}>
          手动测试解析
        </Button>
        <Button variant="outlined" onClick={refreshAuthStatus}>
          刷新认证状态
        </Button>
      </Box>
      
      {user && (
        <Box sx={{ mt: 2, p: 1, backgroundColor: 'grey.100', borderRadius: 1 }}>
          <Typography variant="body2">
            用户信息: {JSON.stringify(user, null, 2)}
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default QuickAuthTest;
