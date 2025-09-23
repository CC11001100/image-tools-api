/**
 * 手机框架组件的样式定义
 */

import { Box, styled } from '@mui/material';

// 手机外框样式
export const PhoneContainer = styled(Box)(({ theme }) => ({
  position: 'relative',
  background: 'linear-gradient(145deg, #2c3e50, #34495e)',
  borderRadius: '32px',
  padding: '6px',
  boxShadow: `
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    inset 0 -1px 0 rgba(0, 0, 0, 0.2)
  `,
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: '3px',
    left: '3px',
    right: '3px',
    bottom: '3px',
    borderRadius: '29px',
    background: 'linear-gradient(145deg, #1a252f, #2c3e50)',
    zIndex: 0,
  },
}));

// 屏幕容器样式
export const ScreenContainer = styled(Box)(({ theme }) => ({
  position: 'relative',
  background: '#000',
  borderRadius: '26px',
  overflow: 'hidden',
  zIndex: 1,
  boxShadow: 'inset 0 0 0 2px rgba(255, 255, 255, 0.1)',
}));

// 侧边按键样式
export const SideButton = styled(Box)<{ side: 'left' | 'right'; top: string; height: string }>(
  ({ theme, side, top, height }) => ({
    position: 'absolute',
    [side]: '-3px',
    top,
    width: '3px',
    height,
    background: 'linear-gradient(90deg, #2c3e50, #34495e)',
    borderRadius: side === 'left' ? '3px 0 0 3px' : '0 3px 3px 0',
    boxShadow: side === 'left' 
      ? '-2px 0 4px rgba(0, 0, 0, 0.2)' 
      : '2px 0 4px rgba(0, 0, 0, 0.2)',
  })
);

// Home键样式
export const HomeButton = styled(Box)(({ theme }) => ({
  position: 'absolute',
  bottom: '12px',
  left: '50%',
  transform: 'translateX(-50%)',
  width: '50px',
  height: '4px',
  background: 'rgba(255, 255, 255, 0.3)',
  borderRadius: '2px',
  zIndex: 3,
}));

// 图片容器样式
export const ImageContainer = styled(Box)(({ theme }) => ({
  width: '100%',
  height: '100%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  background: '#000',
  borderRadius: '18px',
  overflow: 'hidden',
  '& img': {
    width: '100%',
    height: '100%',
    objectFit: 'contain',
    borderRadius: '18px',
  },
}));
