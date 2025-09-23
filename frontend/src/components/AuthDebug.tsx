import React, { useEffect, useState } from 'react';
import { Box, Typography, Card, CardContent, Button, Alert } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { getCookie } from '../utils/cookieUtils';
import { decodeJWTPayload, isJWTValid, extractUserFromJWT } from '../utils/jwtUtils';
import { debugAuth } from '../utils/authDebugUtils';

const AuthDebug: React.FC = () => {
  const { isAuthenticated, user, refreshAuthStatus } = useAuth();
  const [debugInfo, setDebugInfo] = useState<any>(null);

  const runDebug = () => {
    // 使用专门的调试函数
    const debugResult = debugAuth();

    const debug = {
      ...debugResult,
      authState: { isAuthenticated, user },
      timestamp: new Date().toLocaleString()
    };

    setDebugInfo(debug);
  };

  useEffect(() => {
    runDebug();
  }, [isAuthenticated, user]);

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        认证状态调试
      </Typography>
      
      <Box sx={{ mb: 2 }}>
        <Button variant="contained" onClick={runDebug} sx={{ mr: 1 }}>
          刷新调试信息
        </Button>
        <Button variant="outlined" onClick={refreshAuthStatus}>
          刷新认证状态
        </Button>
      </Box>

      {debugInfo && (
        <Card>
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>
              调试信息 ({debugInfo.timestamp})
            </Typography>
            
            <Alert severity={debugInfo.cookieExists ? "success" : "error"} sx={{ mb: 2 }}>
              Cookie状态: {debugInfo.cookieExists ? "存在" : "不存在"}
            </Alert>
            
            <Alert severity={debugInfo.isValid ? "success" : "error"} sx={{ mb: 2 }}>
              JWT状态: {debugInfo.isValid ? "有效" : "无效"}
            </Alert>
            
            <Alert severity={debugInfo.authState.isAuthenticated ? "success" : "error"} sx={{ mb: 2 }}>
              认证状态: {debugInfo.authState.isAuthenticated ? "已登录" : "未登录"}
            </Alert>
            
            <Typography variant="body2" component="pre" sx={{ 
              backgroundColor: 'grey.100', 
              p: 1, 
              borderRadius: 1,
              overflow: 'auto',
              fontSize: '0.75rem',
              whiteSpace: 'pre-wrap'
            }}>
              {JSON.stringify(debugInfo, null, 2)}
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default AuthDebug;
