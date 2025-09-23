/**
 * Layout组件相关的类型定义
 */

import { ReactNode } from 'react';

export interface LayoutProps {
  children: ReactNode;
}

export interface MenuItem {
  text: string;
  path?: string;
  icon: React.ReactElement;
  children?: MenuItem[];
}

export interface MenuItemProps {
  item: MenuItem;
  depth?: number;
  openGroups: Record<string, boolean>;
  onGroupClick: (groupText: string) => void;
  currentPath: string;
}

export interface AppBarProps {
  drawerWidth: number;
  onDrawerToggle: () => void;
}

export interface SidebarProps {
  drawerWidth: number;
  mobileOpen: boolean;
  onDrawerToggle: () => void;
  openGroups: Record<string, boolean>;
  onGroupClick: (groupText: string) => void;
  currentPath: string;
}

export interface UserMenuProps {
  anchorEl: HTMLElement | null;
  onClose: () => void;
  onLogout: () => void;
}
