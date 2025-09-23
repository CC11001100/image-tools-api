/**
 * 菜单项组件
 */

import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  List,
  ListItemIcon,
  ListItemText,
  Collapse,
  ListItemButton,
} from '@mui/material';
import {
  ExpandLess,
  ExpandMore,
} from '@mui/icons-material';

import { MenuItemProps } from './types';

const MenuItemComponent: React.FC<MenuItemProps> = ({
  item,
  depth = 0,
  openGroups,
  onGroupClick,
  currentPath,
}) => {
  const hasChildren = item.children && item.children.length > 0;
  const isOpen = openGroups[item.text] ?? false;
  const isActive = item.path === currentPath;
  const isGroupActive = item.children?.some(child => child.path === currentPath);

  if (hasChildren) {
    return (
      <React.Fragment key={item.text}>
        <ListItemButton
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            onGroupClick(item.text);
          }}
          disableRipple={false}
          sx={{
            pl: depth * 2 + 2,
            backgroundColor: isGroupActive ? 'rgba(25, 118, 210, 0.08)' : 'transparent',
            '&:hover': {
              backgroundColor: isGroupActive ? 'rgba(25, 118, 210, 0.12)' : 'rgba(0, 0, 0, 0.04)',
            },
            borderLeft: isGroupActive ? '3px solid #1976d2' : '3px solid transparent',
            cursor: 'pointer',
          }}
        >
          <ListItemIcon sx={{ minWidth: 40, color: isGroupActive ? 'primary.main' : 'inherit' }}>
            {item.icon}
          </ListItemIcon>
          <ListItemText 
            primary={item.text} 
            primaryTypographyProps={{
              fontWeight: isGroupActive ? 600 : 400,
              color: isGroupActive ? 'primary.main' : 'inherit',
            }}
          />
          {isOpen ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={isOpen} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {item.children?.map(child => (
              <MenuItemComponent
                key={child.path || child.text}
                item={child}
                depth={depth + 1}
                openGroups={openGroups}
                onGroupClick={onGroupClick}
                currentPath={currentPath}
              />
            ))}
          </List>
        </Collapse>
      </React.Fragment>
    );
  }

  return (
    <ListItemButton
      key={item.path}
      component={RouterLink}
      to={item.path!}
      selected={isActive}
      disableRipple={false}
      sx={{
        pl: depth === 0 ? 2 : 4,
        py: depth === 0 ? 1 : 0.75,
        backgroundColor: isActive ? 'rgba(25, 118, 210, 0.12)' : 'transparent',
        borderLeft: isActive ? '3px solid #1976d2' : '3px solid transparent',
        '&:hover': {
          backgroundColor: isActive ? 'rgba(25, 118, 210, 0.16)' : 'rgba(0, 0, 0, 0.04)',
        },
        '&.Mui-selected': {
          backgroundColor: 'rgba(25, 118, 210, 0.12)',
          '&:hover': {
            backgroundColor: 'rgba(25, 118, 210, 0.16)',
          },
        },
        textDecoration: 'none',
        color: 'inherit',
      }}
    >
      <ListItemIcon sx={{ 
        minWidth: depth === 0 ? 40 : 35,
        color: isActive ? 'primary.main' : 'inherit',
        pl: depth === 0 ? 0 : 2,
      }}>
        {item.icon}
      </ListItemIcon>
      <ListItemText 
        primary={item.text} 
        primaryTypographyProps={{
          fontSize: depth === 0 ? '1rem' : '0.875rem',
          fontWeight: isActive ? 600 : 400,
          color: isActive ? 'primary.main' : 'inherit',
        }}
      />
    </ListItemButton>
  );
};

export default MenuItemComponent;
