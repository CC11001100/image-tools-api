/**
 * 手机框架组件相关的类型定义
 */

export interface PhoneFrameProps {
  children: React.ReactNode;
  width?: number | string;
  height?: number | string;
  scale?: number; // 缩放比例，默认1.0
  maxWidth?: string; // 最大宽度，如 '100%' 或 '300px'
  variant?: 'iphone' | 'android';
  showNotch?: boolean;
  showHomeButton?: boolean;
  batteryLevel?: number;
  isCharging?: boolean;
  carrierName?: string;
  networkType?: '5G' | '4G' | 'WiFi';
  showBluetooth?: boolean;
}

export interface StatusBarProps {
  carrierName: string;
  networkType: '5G' | '4G' | 'WiFi';
  showBluetooth: boolean;
  batteryLevel: number;
  isCharging: boolean;
}

export interface NotchProps {
  showNotch: boolean;
}

export interface SideButtonsProps {
  variant: 'iphone' | 'android';
}

export interface FrameContainerProps {
  width: number | string;
  height: number;
  maxWidth: string;
  children: React.ReactNode;
}
