/**
 * Layout组件 - 重构版本
 * 将原来的538行大文件拆分为多个小组件，提高可维护性
 */

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Box,
  Toolbar,
} from '@mui/material';

import GlobalSearch from '../GlobalSearch';
import { AIGroupFloat } from '../AIGroupFloat';
import AppBar from './AppBar';
import Sidebar from './Sidebar';
import Footer from './Footer';
import { drawerWidth, menuItems } from './menuConfig';
import { LayoutProps } from './types';

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>({});
  const location = useLocation();

  // 从localStorage读取保存的展开状态
  useEffect(() => {
    const savedOpenGroups = localStorage.getItem('menuOpenGroups');
    if (savedOpenGroups) {
      try {
        const parsed = JSON.parse(savedOpenGroups);
        setOpenGroups(parsed);
      } catch (e) {
        console.error('Failed to parse saved menu state:', e);
      }
    } else {
      // 如果没有保存的状态，初始化时展开包含当前路径的分组
      const initialOpenGroups: Record<string, boolean> = {};
      menuItems.forEach(item => {
        if (item.children) {
          const hasActiveChild = item.children.some(child => child.path === location.pathname);
          if (hasActiveChild) {
            initialOpenGroups[item.text] = true;
          }
        }
      });
      setOpenGroups(initialOpenGroups);
    }
  }, [location.pathname]);

  // 当展开状态改变时保存到localStorage
  useEffect(() => {
    if (Object.keys(openGroups).length > 0) {
      localStorage.setItem('menuOpenGroups', JSON.stringify(openGroups));
    }
  }, [openGroups]);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleGroupClick = (groupText: string) => {
    setOpenGroups(prev => ({
      ...prev,
      [groupText]: !prev[groupText],
    }));
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <AppBar
        drawerWidth={drawerWidth}
        onDrawerToggle={handleDrawerToggle}
      />

      <Sidebar
        drawerWidth={drawerWidth}
        mobileOpen={mobileOpen}
        onDrawerToggle={handleDrawerToggle}
        openGroups={openGroups}
        onGroupClick={handleGroupClick}
        currentPath={location.pathname}
      />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          width: { sm: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar /> {/* 添加工具栏的空白空间 */}
        <Box sx={{ flexGrow: 1, p: 3 }}>
          {children}
        </Box>
        <Footer />
      </Box>

      {/* 全局搜索组件 */}
      <GlobalSearch />

      {/* AI交流群悬浮组件 */}
      <AIGroupFloat />
    </Box>
  );
};

export default Layout;
