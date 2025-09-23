/**
 * 手机框架组件 - 重构版本
 * 将原来的481行大文件拆分为多个小组件，提高可维护性
 */

import React from 'react';
import { PhoneContainer, ScreenContainer, HomeButton, ImageContainer } from './styles';
import StatusBarComponent from './StatusBarComponents';
import NotchComponent from './NotchComponents';
import SideButtons from './SideButtons';
import { PhoneFrameProps } from './types';

export const PhoneFrame: React.FC<PhoneFrameProps> = ({
  children,
  width,
  height,
  scale = 1.0,
  maxWidth = '100%',
  variant = 'iphone',
  showNotch = true,
  showHomeButton = false,
  batteryLevel,
  isCharging = false,
  carrierName = 'AIGC Hub Phone',
  networkType = '5G',
  showBluetooth = true,
}) => {
  // 手机的基础尺寸比例 - 使用1080x1920的实际比例
  const baseAspectRatio = 1920 / 1080; // 高度/宽度 ≈ 1.78 (匹配我们的图片比例)

  // 计算实际尺寸
  const actualWidth = typeof width === 'number' ? width : (200 * scale); // 增加基础宽度
  const actualHeight = typeof height === 'number' ? height : (actualWidth * baseAspectRatio + 20); // 增加20px高度

  // 生成随机电量（如果没有提供）
  const randomBatteryLevel = React.useMemo(() => {
    return batteryLevel !== undefined ? batteryLevel : Math.floor(Math.random() * 100) + 1;
  }, [batteryLevel]);

  return (
    <PhoneContainer
      sx={{
        width: '100%',
        height: actualHeight,
        maxWidth: maxWidth,
        margin: 0,
      }}
    >
      {/* 侧边按键 */}
      <SideButtons variant={variant} />

      <ScreenContainer
        sx={{
          width: '100%',
          height: '100%',
          paddingTop: showNotch ? '32px' : '28px', // 往上调整20px，从52px/48px改为32px/28px
          paddingBottom: showHomeButton ? '24px' : '8px',
          paddingX: '8px',
        }}
      >
        {/* 状态栏 */}
        <StatusBarComponent
          carrierName={carrierName}
          networkType={networkType}
          showBluetooth={showBluetooth}
          batteryLevel={randomBatteryLevel}
          isCharging={isCharging}
        />

        {/* 刘海 */}
        <NotchComponent showNotch={showNotch} />

        {/* 图片内容 */}
        <ImageContainer>
          {children}
        </ImageContainer>

        {/* Home键指示器 */}
        {showHomeButton && <HomeButton />}
      </ScreenContainer>
    </PhoneContainer>
  );
};

export default PhoneFrame;
