/**
 * 侧边按键组件
 */

import React from 'react';
import { SideButton } from './styles';
import { SideButtonsProps } from './types';

const SideButtons: React.FC<SideButtonsProps> = ({ variant }) => {
  return (
    <>
      {/* 左侧按键 */}
      <SideButton side="left" top="60px" height="30px" />
      <SideButton side="left" top="100px" height="50px" />
      <SideButton side="left" top="160px" height="50px" />
      
      {/* 右侧按键 */}
      <SideButton side="right" top="80px" height="80px" />
    </>
  );
};

export default SideButtons;
