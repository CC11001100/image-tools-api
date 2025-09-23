import React, { useState } from 'react';
import {
  Box,
  Typography,
  Fade,
  Paper
} from '@mui/material';
import { styled } from '@mui/material/styles';

const FloatContainer = styled(Box)(({ theme }) => ({
  position: 'fixed',
  bottom: '20px',
  right: '20px',
  zIndex: 1000,
  cursor: 'pointer',
}));

const FloatButton = styled(Paper)(({ theme }) => ({
  padding: '12px 16px',
  backgroundColor: theme.palette.primary.main,
  color: 'white',
  borderRadius: '25px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  transition: 'all 0.3s ease',
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
    transform: 'translateY(-2px)',
    boxShadow: '0 6px 16px rgba(0,0,0,0.2)',
  },
}));

const QRCodeContainer = styled(Box)(({ theme }) => ({
  position: 'absolute',
  bottom: '60px',
  right: '0',
  backgroundColor: 'white',
  padding: '16px',
  borderRadius: '12px',
  boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
  border: '1px solid #e0e0e0',
  minWidth: '360px',
  textAlign: 'center',
}));

export const AIGroupFloat: React.FC = () => {
  const [showQRCode, setShowQRCode] = useState(false);

  return (
    <FloatContainer
      onMouseEnter={() => setShowQRCode(true)}
      onMouseLeave={() => setShowQRCode(false)}
    >
      <Fade in={showQRCode} timeout={300}>
        <QRCodeContainer>
          <Typography variant="subtitle2" gutterBottom color="primary">
            遇到问题找客服
          </Typography>
          <img
            src="https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/common/wechat-group-qr.png"
            alt="微信群二维码"
            style={{
              width: '320px',
              height: '320px',
              border: '1px solid #ddd',
              borderRadius: '8px'
            }}
          />
          <Typography variant="caption" sx={{ mt: 1, display: 'block', color: 'text.secondary' }}>
            扫码加入微信群
          </Typography>
        </QRCodeContainer>
      </Fade>
      
      <FloatButton elevation={3}>
        <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
          遇到问题找客服
        </Typography>
      </FloatButton>
    </FloatContainer>
  );
};
