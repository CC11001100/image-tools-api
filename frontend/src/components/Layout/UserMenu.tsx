/**
 * 用户菜单组件
 */

import React from 'react';
import {
  Menu,
  MenuItem,
} from '@mui/material';
import {
  AccountCircle as AccountCircleIcon,
  Logout as LogoutIcon,
  Store as StoreIcon,
  AccountBalanceWallet as AccountBalanceWalletIcon,
} from '@mui/icons-material';

import { UserMenuProps } from './types';

const UserMenu: React.FC<UserMenuProps> = ({
  anchorEl,
  onClose,
  onLogout,
}) => {
  // 用户中心点击处理
  const handleUserCenter = () => {
    window.open('https://usersystem.aigchub.vip/', '_blank');
    onClose();
  };

  // 产品中心点击处理
  const handleProductCenter = () => {
    window.open('https://www.aigchub.vip/products', '_blank');
    onClose();
  };

  // Token充值点击处理
  const handleTokenRecharge = () => {
    window.open('https://usersystem.aigchub.vip/dashboard/recharge', '_blank');
    onClose();
  };

  const handleLogout = () => {
    onLogout();
    onClose();
  };

  return (
    <Menu
      anchorEl={anchorEl}
      open={Boolean(anchorEl)}
      onClose={onClose}
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'right',
      }}
      transformOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
    >
      <MenuItem onClick={handleUserCenter}>
        <AccountCircleIcon sx={{ mr: 1 }} />
        用户中心
      </MenuItem>
      <MenuItem onClick={handleTokenRecharge}>
        <AccountBalanceWalletIcon sx={{ mr: 1 }} />
        Token充值
      </MenuItem>
      <MenuItem onClick={handleProductCenter}>
        <StoreIcon sx={{ mr: 1 }} />
        产品中心
      </MenuItem>
      <MenuItem onClick={handleLogout}>
        <LogoutIcon sx={{ mr: 1 }} />
        退出登录
      </MenuItem>
    </Menu>
  );
};

export default UserMenu;
