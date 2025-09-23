/**
 * 高级文字设置组件 - 重构版本
 * 将原来的507行大文件拆分为多个小组件，提高可维护性
 */

import React, { useState, useEffect } from 'react';
import { Box } from '@mui/material';

import BasicTextSettings from './BasicTextSettings';
import PositionSettings from './PositionSettings';
import EffectSettings from './EffectSettings';
import StrokeSettings from './StrokeSettings';
import ShadowSettings from './ShadowSettings';
import MultilineTextSettings from './MultilineTextSettings';
import { UnifiedTextSettingsComponentProps } from './types';

const UnifiedTextSettingsComponent: React.FC<UnifiedTextSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
  appliedParams,
}) => {
  // 基础文字设置
  const [text, setText] = useState('Hello World');
  const [fontFamily, setFontFamily] = useState('Arial');
  const [fontSize, setFontSize] = useState(48);
  const [fontColor, setFontColor] = useState('#000000');
  
  // 位置设置
  const [position, setPosition] = useState('center');
  const [xOffset, setXOffset] = useState(0);
  const [yOffset, setYOffset] = useState(0);
  
  // 效果设置
  const [rotation, setRotation] = useState(0);
  const [opacity, setOpacity] = useState(1.0);
  const [quality, setQuality] = useState(90);
  
  // 描边设置
  const [strokeWidth, setStrokeWidth] = useState(0);
  const [strokeColor, setStrokeColor] = useState('#FFFFFF');
  
  // 阴影设置
  const [shadowOffsetX, setShadowOffsetX] = useState(0);
  const [shadowOffsetY, setShadowOffsetY] = useState(0);
  const [shadowBlur, setShadowBlur] = useState(0);
  const [shadowColor, setShadowColor] = useState('#000000');
  
  // 多行文字设置
  const [lineSpacing, setLineSpacing] = useState(5);
  const [maxWidth, setMaxWidth] = useState('');
  
  // 高级设置
  const [letterSpacing, setLetterSpacing] = useState(0);
  const [lineHeight, setLineHeight] = useState(1.2);
  const [textAlign, setTextAlign] = useState('left');
  const [bold, setBold] = useState(false);
  const [italic, setItalic] = useState(false);
  const [underline, setUnderline] = useState(false);

  // 处理应用参数的变化
  useEffect(() => {
    if (appliedParams) {
      console.log('🎯 UnifiedTextSettingsComponent: 应用参数', appliedParams);
      
      // 基础文字设置
      if (appliedParams.text !== undefined) setText(appliedParams.text);
      if (appliedParams.font_family !== undefined) setFontFamily(appliedParams.font_family);
      if (appliedParams.font_size !== undefined) setFontSize(appliedParams.font_size);
      if (appliedParams.font_color !== undefined) setFontColor(appliedParams.font_color);
      
      // 位置设置
      if (appliedParams.position !== undefined) setPosition(appliedParams.position);
      if (appliedParams.x_offset !== undefined) setXOffset(appliedParams.x_offset);
      if (appliedParams.y_offset !== undefined) setYOffset(appliedParams.y_offset);
      
      // 效果设置
      if (appliedParams.rotation !== undefined) setRotation(appliedParams.rotation);
      if (appliedParams.opacity !== undefined) setOpacity(appliedParams.opacity);
      if (appliedParams.quality !== undefined) setQuality(appliedParams.quality);
      
      // 描边设置
      if (appliedParams.stroke_width !== undefined) setStrokeWidth(appliedParams.stroke_width);
      if (appliedParams.stroke_color !== undefined) setStrokeColor(appliedParams.stroke_color);
      
      // 阴影设置
      if (appliedParams.shadow_offset_x !== undefined) setShadowOffsetX(appliedParams.shadow_offset_x);
      if (appliedParams.shadow_offset_y !== undefined) setShadowOffsetY(appliedParams.shadow_offset_y);
      if (appliedParams.shadow_blur !== undefined) setShadowBlur(appliedParams.shadow_blur);
      if (appliedParams.shadow_color !== undefined) setShadowColor(appliedParams.shadow_color);
      
      // 多行文字设置
      if (appliedParams.line_spacing !== undefined) setLineSpacing(appliedParams.line_spacing);
      if (appliedParams.max_width !== undefined) setMaxWidth(appliedParams.max_width.toString());
      
      // 高级设置
      if (appliedParams.letter_spacing !== undefined) setLetterSpacing(appliedParams.letter_spacing);
      if (appliedParams.line_height !== undefined) setLineHeight(appliedParams.line_height);
      if (appliedParams.text_align !== undefined) setTextAlign(appliedParams.text_align);
      if (appliedParams.bold !== undefined) setBold(appliedParams.bold);
      if (appliedParams.italic !== undefined) setItalic(appliedParams.italic);
      if (appliedParams.underline !== undefined) setUnderline(appliedParams.underline);
    }
  }, [appliedParams]);

  useEffect(() => {
    const settings: any = {
      text: text,
      font_family: fontFamily,
      font_size: fontSize,
      font_color: fontColor,
      position: position,
      x_offset: xOffset,
      y_offset: yOffset,
      rotation: rotation,
      opacity: opacity,
      quality: quality,
      line_spacing: lineSpacing,
    };

    // 添加条件参数
    if (strokeWidth > 0) {
      settings.stroke_width = strokeWidth;
      settings.stroke_color = strokeColor;
    }
    
    if (shadowOffsetX !== 0 || shadowOffsetY !== 0 || shadowBlur > 0) {
      settings.shadow_offset_x = shadowOffsetX;
      settings.shadow_offset_y = shadowOffsetY;
      settings.shadow_blur = shadowBlur;
      settings.shadow_color = shadowColor;
    }
    
    if (maxWidth && parseInt(maxWidth) > 0) {
      settings.max_width = parseInt(maxWidth);
    }
    
    if (letterSpacing !== 0) settings.letter_spacing = letterSpacing;
    if (lineHeight !== 1.2) settings.line_height = lineHeight;
    if (textAlign !== 'left') settings.text_align = textAlign;
    if (bold) settings.bold = bold;
    if (italic) settings.italic = italic;
    if (underline) settings.underline = underline;

    onSettingsChange(settings);
  }, [
    text, fontFamily, fontSize, fontColor, position, xOffset, yOffset, rotation,
    strokeWidth, strokeColor, shadowOffsetX, shadowOffsetY, shadowBlur, shadowColor,
    opacity, lineSpacing, maxWidth, letterSpacing, lineHeight, textAlign, 
    bold, italic, underline, quality, onSettingsChange
  ]);

  return (
    <Box>
      <BasicTextSettings
        isLoading={isLoading}
        onSettingsChange={onSettingsChange}
        text={text}
        setText={setText}
        fontFamily={fontFamily}
        setFontFamily={setFontFamily}
        fontSize={fontSize}
        setFontSize={setFontSize}
        fontColor={fontColor}
        setFontColor={setFontColor}
        bold={bold}
        setBold={setBold}
        italic={italic}
        setItalic={setItalic}
        underline={underline}
        setUnderline={setUnderline}
      />

      <PositionSettings
        isLoading={isLoading}
        onSettingsChange={onSettingsChange}
        position={position}
        setPosition={setPosition}
        xOffset={xOffset}
        setXOffset={setXOffset}
        yOffset={yOffset}
        setYOffset={setYOffset}
        rotation={rotation}
        setRotation={setRotation}
      />

      <MultilineTextSettings
        isLoading={isLoading}
        onSettingsChange={onSettingsChange}
        lineSpacing={lineSpacing}
        setLineSpacing={setLineSpacing}
        maxWidth={maxWidth}
        setMaxWidth={setMaxWidth}
        lineHeight={lineHeight}
        setLineHeight={setLineHeight}
        textAlign={textAlign}
        setTextAlign={setTextAlign}
        letterSpacing={letterSpacing}
        setLetterSpacing={setLetterSpacing}
      />

      <StrokeSettings
        isLoading={isLoading}
        onSettingsChange={onSettingsChange}
        strokeWidth={strokeWidth}
        setStrokeWidth={setStrokeWidth}
        strokeColor={strokeColor}
        setStrokeColor={setStrokeColor}
      />

      <ShadowSettings
        isLoading={isLoading}
        onSettingsChange={onSettingsChange}
        shadowOffsetX={shadowOffsetX}
        setShadowOffsetX={setShadowOffsetX}
        shadowOffsetY={shadowOffsetY}
        setShadowOffsetY={setShadowOffsetY}
        shadowBlur={shadowBlur}
        setShadowBlur={setShadowBlur}
        shadowColor={shadowColor}
        setShadowColor={setShadowColor}
      />

      <EffectSettings
        isLoading={isLoading}
        onSettingsChange={onSettingsChange}
        opacity={opacity}
        setOpacity={setOpacity}
        quality={quality}
        setQuality={setQuality}
      />
    </Box>
  );
};

export default UnifiedTextSettingsComponent;
