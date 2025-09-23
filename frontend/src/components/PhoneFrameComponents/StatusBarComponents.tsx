/**
 * 状态栏相关组件
 */

import React from 'react';
import { Box, styled } from '@mui/material';
import { StatusBarProps } from './types';

// 状态栏
const StatusBar = styled(Box)(({ theme }) => ({
  position: 'absolute',
  top: '35px', // 往上调整20px，从55px改为35px
  left: '12px',
  right: '12px',
  height: '18px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  color: 'white',
  fontSize: '11px',
  fontWeight: '600',
  zIndex: 3,
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
}));

// 状态栏左侧（时间）
const StatusBarLeft = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  color: 'white',
}));

// 状态栏右侧（电量、信号等）
const StatusBarRight = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: '4px',
  color: 'white',
}));

// 运营商信号图标
const CellularIcon = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'flex-end',
  gap: '1px',
  height: '10px',
  '& .bar': {
    width: '2px',
    background: 'white',
    borderRadius: '0.5px',
    '&:nth-of-type(1)': { height: '3px' },
    '&:nth-of-type(2)': { height: '5px' },
    '&:nth-of-type(3)': { height: '7px' },
    '&:nth-of-type(4)': { height: '9px' },
  },
}));

// 5G网络图标
const NetworkIcon = styled(Box)(({ theme }) => ({
  fontSize: '9px',
  fontWeight: 'bold',
  color: 'white',
  letterSpacing: '0.5px',
}));

// WiFi图标
const WiFiIcon = styled(Box)(({ theme }) => ({
  width: '13px',
  height: '10px',
  position: 'relative',
  '&::before': {
    content: '""',
    position: 'absolute',
    width: '12px',
    height: '9px',
    border: '2px solid white',
    borderBottom: 'none',
    borderRadius: '12px 12px 0 0',
    top: '0',
    left: '0',
  },
  '&::after': {
    content: '""',
    position: 'absolute',
    width: '8px',
    height: '6px',
    border: '2px solid white',
    borderBottom: 'none',
    borderRadius: '8px 8px 0 0',
    top: '2px',
    left: '2px',
  },
  '& .dot': {
    position: 'absolute',
    width: '2px',
    height: '2px',
    background: 'white',
    borderRadius: '50%',
    bottom: '0',
    left: '5px',
  },
}));

// 蓝牙图标
const BluetoothIcon = styled(Box)(({ theme }) => ({
  width: '8px',
  height: '12px',
  position: 'relative',
  '&::before': {
    content: '""',
    position: 'absolute',
    width: '0',
    height: '0',
    borderLeft: '4px solid white',
    borderTop: '3px solid transparent',
    borderBottom: '3px solid transparent',
    top: '0',
    left: '2px',
  },
  '&::after': {
    content: '""',
    position: 'absolute',
    width: '0',
    height: '0',
    borderLeft: '4px solid white',
    borderTop: '3px solid transparent',
    borderBottom: '3px solid transparent',
    bottom: '0',
    left: '2px',
    transform: 'rotate(180deg)',
  },
}));

// 电池图标
const BatteryIcon = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'charging' && prop !== 'level',
})<{ charging?: boolean; level?: number }>(({ theme, charging = false, level = 100 }) => ({
  width: '22px',
  height: '11px',
  border: '1px solid white',
  borderRadius: '2px',
  position: 'relative',
  display: 'flex',
  alignItems: 'center',
  '&::before': {
    content: '""',
    position: 'absolute',
    right: '-3px',
    top: '3px',
    width: '2px',
    height: '5px',
    background: 'white',
    borderRadius: '0 1px 1px 0',
  },
  '&::after': {
    content: '""',
    position: 'absolute',
    left: '1px',
    top: '1px',
    width: `${(level / 100) * 18}px`,
    height: '9px',
    background: level > 20 ? '#4CAF50' : '#F44336',
    borderRadius: '1px',
    transition: 'width 0.3s ease',
  },
  ...(charging && {
    '& .lightning': {
      position: 'absolute',
      left: '50%',
      top: '50%',
      transform: 'translate(-50%, -50%)',
      width: '0',
      height: '0',
      borderLeft: '3px solid transparent',
      borderRight: '3px solid transparent',
      borderBottom: '6px solid #FFD700',
      zIndex: 1,
      '&::after': {
        content: '""',
        position: 'absolute',
        top: '3px',
        left: '-3px',
        width: '0',
        height: '0',
        borderLeft: '3px solid transparent',
        borderRight: '3px solid transparent',
        borderTop: '3px solid #FFD700',
      },
    },
  }),
}));

const StatusBarComponent: React.FC<StatusBarProps> = ({
  carrierName,
  networkType,
  showBluetooth,
  batteryLevel,
  isCharging,
}) => {
  // 获取当前时间
  const currentTime = new Date().toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });

  return (
    <StatusBar>
      <StatusBarLeft>
        <Box sx={{ fontSize: '14px', fontWeight: '600', letterSpacing: '-0.5px' }}>
          {currentTime}
        </Box>
      </StatusBarLeft>
      <StatusBarRight>
        <Box sx={{ fontSize: '11px', fontWeight: '600' }}>{carrierName}</Box>
        <CellularIcon>
          <Box className="bar" />
          <Box className="bar" />
          <Box className="bar" />
          <Box className="bar" />
        </CellularIcon>
        <NetworkIcon>{networkType}</NetworkIcon>
        <WiFiIcon>
          <Box className="dot" />
        </WiFiIcon>
        {showBluetooth && <BluetoothIcon />}
        <Box sx={{ fontSize: '11px', fontWeight: '600' }}>{batteryLevel}%</Box>
        <BatteryIcon charging={isCharging} level={batteryLevel}>
          {isCharging && <Box className="lightning" />}
        </BatteryIcon>
      </StatusBarRight>
    </StatusBar>
  );
};

export default StatusBarComponent;
