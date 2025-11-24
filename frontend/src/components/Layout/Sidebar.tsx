/**
 * 侧边栏组件
 */

import React from 'react';
import {
  Box,
  Drawer,
  Toolbar,
  Typography,
  Divider,
  List,
} from '@mui/material';

import { menuItems } from './menuConfig';
import MenuItemComponent from './MenuItem';
import { SidebarProps } from './types';

const Sidebar: React.FC<SidebarProps> = ({
  drawerWidth,
  mobileOpen,
  onDrawerToggle,
  openGroups,
  onGroupClick,
  currentPath,
}) => {
  const drawer = (
    <div>
      <Toolbar sx={{ backgroundColor: 'primary.main', color: 'white' }}>
        <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 600 }}>
          AI图像工具箱 v5.3.7
        </Typography>
      </Toolbar>
      <Divider />
      <List sx={{ pt: 0 }}>
        {menuItems.map(item => (
          <MenuItemComponent
            key={item.path || item.text}
            item={item}
            openGroups={openGroups}
            onGroupClick={onGroupClick}
            currentPath={currentPath}
          />
        ))}
      </List>
    </div>
  );

  return (
    <Box
      component="nav"
      sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
    >
      {/* 移动端抽屉 */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onDrawerToggle}
        ModalProps={{
          keepMounted: true, // 提升移动端性能
        }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
      >
        {drawer}
      </Drawer>
      {/* 桌面端抽屉 */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
        open
      >
        {drawer}
      </Drawer>
    </Box>
  );
};

export default Sidebar;
