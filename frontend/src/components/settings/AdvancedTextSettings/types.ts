/**
 * 高级文字设置组件相关的类型定义
 */

export interface TextSettings {
  text: string;
  font_family: string;
  font_size: number;
  font_color: string;
  position: string;
  x_offset: number;
  y_offset: number;
  rotation: number;
  opacity: number;
  quality: number;
  line_spacing: number;
  stroke_width?: number;
  stroke_color?: string;
  shadow_offset_x?: number;
  shadow_offset_y?: number;
  shadow_blur?: number;
  shadow_color?: string;
  max_width?: number;
  letter_spacing?: number;
  line_height?: number;
  text_align?: string;
  bold?: boolean;
  italic?: boolean;
  underline?: boolean;
}

export interface BaseSettingsProps {
  isLoading: boolean;
  onSettingsChange: (settings: any) => void;
}

export interface BasicTextSettingsProps extends BaseSettingsProps {
  text: string;
  setText: (text: string) => void;
  fontFamily: string;
  setFontFamily: (fontFamily: string) => void;
  fontSize: number;
  setFontSize: (fontSize: number) => void;
  fontColor: string;
  setFontColor: (fontColor: string) => void;
  bold: boolean;
  setBold: (bold: boolean) => void;
  italic: boolean;
  setItalic: (italic: boolean) => void;
  underline: boolean;
  setUnderline: (underline: boolean) => void;
}

export interface PositionSettingsProps extends BaseSettingsProps {
  position: string;
  setPosition: (position: string) => void;
  xOffset: number;
  setXOffset: (xOffset: number) => void;
  yOffset: number;
  setYOffset: (yOffset: number) => void;
  rotation: number;
  setRotation: (rotation: number) => void;
}

export interface EffectSettingsProps extends BaseSettingsProps {
  opacity: number;
  setOpacity: (opacity: number) => void;
  quality: number;
  setQuality: (quality: number) => void;
}

export interface StrokeSettingsProps extends BaseSettingsProps {
  strokeWidth: number;
  setStrokeWidth: (strokeWidth: number) => void;
  strokeColor: string;
  setStrokeColor: (strokeColor: string) => void;
}

export interface ShadowSettingsProps extends BaseSettingsProps {
  shadowOffsetX: number;
  setShadowOffsetX: (shadowOffsetX: number) => void;
  shadowOffsetY: number;
  setShadowOffsetY: (shadowOffsetY: number) => void;
  shadowBlur: number;
  setShadowBlur: (shadowBlur: number) => void;
  shadowColor: string;
  setShadowColor: (shadowColor: string) => void;
}

export interface MultilineTextSettingsProps extends BaseSettingsProps {
  lineSpacing: number;
  setLineSpacing: (lineSpacing: number) => void;
  maxWidth: string;
  setMaxWidth: (maxWidth: string) => void;
  lineHeight: number;
  setLineHeight: (lineHeight: number) => void;
  textAlign: string;
  setTextAlign: (textAlign: string) => void;
  letterSpacing: number;
  setLetterSpacing: (letterSpacing: number) => void;
}

export interface UnifiedTextSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
  appliedParams?: Record<string, any> | null;
}
