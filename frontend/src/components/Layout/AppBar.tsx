/**
 * 应用栏组件
 */

import React, { useState } from 'react';
import {
  AppBar as MuiAppBar,
  Toolbar,
  IconButton,
  Typography,
  Box,
  Button,
  Avatar,
  Chip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Search as SearchIcon,
  Login as LoginIcon,
  PersonAdd as PersonAddIcon,
  AccountCircle as AccountCircleIcon,
} from '@mui/icons-material';

import { useSearch } from '../../contexts/SearchContext';
import { useAuth } from '../../contexts/AuthContext';
import { generateLoginUrl, generateRegisterUrl } from '../../utils/authUtils';
import UserMenu from './UserMenu';
import UserBalanceComponent from '../UserBalance';
import { AppBarProps } from './types';

const AppBar: React.FC<AppBarProps> = ({ drawerWidth, onDrawerToggle }) => {
  const [userMenuAnchor, setUserMenuAnchor] = useState<null | HTMLElement>(null);
  const { openSearch } = useSearch();
  const { isAuthenticated, user, logout } = useAuth();

  // 登录按钮点击处理
  const handleLogin = () => {
    window.location.href = generateLoginUrl();
  };

  // 注册按钮点击处理
  const handleRegister = () => {
    window.location.href = generateRegisterUrl();
  };

  // 用户菜单打开处理
  const handleUserMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setUserMenuAnchor(event.currentTarget);
  };

  // 用户菜单关闭处理
  const handleUserMenuClose = () => {
    setUserMenuAnchor(null);
  };

  // 生成用户头像的首字母
  const getUserInitials = (nickname: string): string => {
    return nickname.charAt(0).toUpperCase();
  };

  return (
    <>
      <MuiAppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={onDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            图像处理工具演示
          </Typography>
          
          {/* 搜索按钮 */}
          <IconButton
            color="inherit"
            onClick={openSearch}
            sx={{
              mr: 2,
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
            title="搜索 (Ctrl+K)"
          >
            <SearchIcon />
          </IconButton>
          
          {/* 用户认证区域 */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {isAuthenticated && user ? (
              // 已登录状态 - 显示用户信息、余额和菜单
              <>
                {/* 用户余额 */}
                <UserBalanceComponent />
                
                <Chip
                  avatar={
                    <Avatar sx={{ bgcolor: 'primary.main', width: 24, height: 24, fontSize: '0.75rem' }}>
                      {getUserInitials(user.nickname)}
                    </Avatar>
                  }
                  label={user.nickname}
                  variant="outlined"
                  sx={{
                    color: 'white',
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                    '& .MuiChip-label': {
                      color: 'white',
                    },
                  }}
                />
                <IconButton
                  color="inherit"
                  onClick={handleUserMenuOpen}
                  sx={{
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    },
                  }}
                >
                  <AccountCircleIcon />
                </IconButton>
              </>
            ) : (
              // 未登录状态 - 显示登录和注册按钮
              <>
                <Button
                  color="inherit"
                  startIcon={<LoginIcon />}
                  onClick={handleLogin}
                  sx={{
                    textTransform: 'none',
                    fontSize: '0.875rem',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    },
                  }}
                >
                  登录
                </Button>
                <Button
                  color="inherit"
                  startIcon={<PersonAddIcon />}
                  onClick={handleRegister}
                  variant="outlined"
                  sx={{
                    textTransform: 'none',
                    fontSize: '0.875rem',
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      borderColor: 'rgba(255, 255, 255, 0.7)',
                    },
                  }}
                >
                  注册
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </MuiAppBar>
      
      {/* 用户菜单 */}
      <UserMenu
        anchorEl={userMenuAnchor}
        onClose={handleUserMenuClose}
        onLogout={logout}
      />
    </>
  );
};

export default AppBar;
