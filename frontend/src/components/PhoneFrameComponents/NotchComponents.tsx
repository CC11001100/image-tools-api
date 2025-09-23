/**
 * 刘海区域相关组件
 */

import React from 'react';
import { Box, styled } from '@mui/material';
import { NotchProps } from './types';

// 刘海样式
const Notch = styled(Box)(({ theme }) => ({
  position: 'absolute',
  top: '6px',
  left: '50%',
  transform: 'translateX(-50%)',
  width: '120px',
  height: '12px', // 减小刘海高度让状态栏可见
  background: 'linear-gradient(145deg, #0a0a0a, #1a1a1a)',
  borderRadius: '0 0 8px 8px', // 相应调整圆角
  zIndex: 4,
  boxShadow: 'inset 0 -2px 4px rgba(0, 0, 0, 0.5)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '6px',
}));

// 前置摄像头
const FrontCamera = styled(Box)(({ theme }) => ({
  width: '8px',
  height: '8px',
  borderRadius: '50%',
  background: 'radial-gradient(circle at 30% 30%, #444 0%, #222 40%, #000 100%)',
  boxShadow: 'inset 0 1px 2px rgba(0, 0, 0, 0.9), 0 0 0 1px rgba(255, 255, 255, 0.1)',
  position: 'relative',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: '1.5px',
    left: '1.5px',
    width: '5px',
    height: '5px',
    borderRadius: '50%',
    background: 'radial-gradient(circle at 30% 30%, #666 0%, #333 60%, #111 100%)',
  },
  '&::after': {
    content: '""',
    position: 'absolute',
    top: '2.5px',
    left: '2.5px',
    width: '1.5px',
    height: '1.5px',
    borderRadius: '50%',
    background: 'rgba(100, 150, 255, 0.3)',
  },
}));

// 环境光传感器
const AmbientSensor = styled(Box)(({ theme }) => ({
  width: '3px',
  height: '3px',
  borderRadius: '50%',
  background: 'radial-gradient(circle, #333 0%, #111 100%)',
  boxShadow: 'inset 0 1px 1px rgba(0, 0, 0, 0.8)',
}));

// 距离传感器
const ProximitySensor = styled(Box)(({ theme }) => ({
  width: '2px',
  height: '2px',
  borderRadius: '50%',
  background: '#222',
  boxShadow: 'inset 0 1px 1px rgba(0, 0, 0, 0.9)',
}));

// 扬声器网格
const SpeakerGrill = styled(Box)(({ theme }) => ({
  width: '30px',
  height: '3px',
  background: 'linear-gradient(90deg, transparent 0%, #333 20%, #333 80%, transparent 100%)',
  borderRadius: '1.5px',
  position: 'relative',
  '&::before, &::after': {
    content: '""',
    position: 'absolute',
    width: '1.5px',
    height: '1.5px',
    background: '#222',
    borderRadius: '50%',
    top: '0.75px',
  },
  '&::before': {
    left: '6px',
  },
  '&::after': {
    right: '6px',
  },
}));

const NotchComponent: React.FC<NotchProps> = ({ showNotch }) => {
  if (!showNotch) {
    return null;
  }

  return (
    <Notch>
      <ProximitySensor />
      <AmbientSensor />
      <SpeakerGrill />
      <FrontCamera />
    </Notch>
  );
};

export default NotchComponent;
