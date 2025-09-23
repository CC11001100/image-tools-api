import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
  Box,
} from '@mui/material';

interface FilterSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const FilterSettingsComponent: React.FC<FilterSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [filterType, setFilterType] = useState('grayscale');
  const [intensity, setIntensity] = useState(1.0);

  const filterOptions = [
    // 基础滤镜
    { value: 'grayscale', label: '灰度' },
    { value: 'sepia', label: '褐色' },
    { value: 'blur', label: '模糊' },
    { value: 'sharpen', label: '锐化' },
    { value: 'brightness', label: '亮度' },
    { value: 'contrast', label: '对比度' },
    
    // 色彩效果
    { value: 'saturate', label: '饱和度增强' },
    { value: 'desaturate', label: '去饱和' },
    { value: 'warm', label: '暖色调' },
    { value: 'cool', label: '冷色调' },
    { value: 'vintage', label: '复古色彩' },
    { value: 'hueshift', label: '色调偏移' },
    { value: 'gamma', label: '伽马校正' },
    { value: 'levels', label: '色阶调整' },
    
    // 艺术效果
    { value: 'emboss', label: '浮雕效果' },
    { value: 'posterize', label: '色调分离' },
    { value: 'solarize', label: '曝光过度' },
    { value: 'invert', label: '反色' },
    { value: 'edge_enhance', label: '边缘增强' },
    { value: 'smooth', label: '平滑' },
    { value: 'detail', label: '细节增强' },
    
    // 黑白效果
    { value: 'monochrome', label: '单色黑白' },
    { value: 'dramatic_bw', label: '戏剧性黑白' },
    { value: 'infrared', label: '红外效果' },
    { value: 'high_contrast_bw', label: '高对比度黑白' },
    
    // 复古和胶片效果
    { value: 'film_grain', label: '胶片颗粒' },
    { value: 'retro', label: '复古风格' },
    { value: 'polaroid', label: '宝丽来效果' },
    { value: 'lomo', label: 'LOMO风格' },
    { value: 'analog', label: '模拟胶片' },
    { value: 'crossprocess', label: '交叉处理' },
    
    // 特殊效果
    { value: 'dream', label: '梦幻效果' },
    { value: 'glow', label: '发光效果' },
    { value: 'soft_focus', label: '柔焦' },
    { value: 'noise', label: '噪点' },
    { value: 'vignette', label: '暗角效果' },
    { value: 'mosaic', label: '马赛克' },
    
    // 滤镜效果
    { value: 'find_edges', label: '边缘检测' },
    { value: 'contour', label: '轮廓' },
    { value: 'edge_enhance_more', label: '强边缘增强' },
    { value: 'smooth_more', label: '强平滑' },
    { value: 'unsharp_mask', label: '反锐化遮罩' },
    
    // 创意效果
    { value: 'pencil', label: '铅笔画' },
    { value: 'sketch', label: '素描' },
    { value: 'cartoon', label: '卡通效果' },
    { value: 'hdr', label: 'HDR效果' },
    { value: 'cyberpunk', label: '赛博朋克' },
    { value: 'noir', label: '黑色电影' },
    { value: 'faded', label: '褪色效果' },
    { value: 'pastel', label: '柔和色彩' },
  ];

  useEffect(() => {
    onSettingsChange({
      filter_type: filterType,
      intensity: intensity,
    });
  }, [filterType, intensity, onSettingsChange]);

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>滤镜类型</InputLabel>
        <Select
          value={filterType}
          label="滤镜类型"
          onChange={(e) => setFilterType(e.target.value)}
          disabled={isLoading}
        >
          {filterOptions.map((filter) => (
            <MenuItem key={filter.value} value={filter.value}>
              {filter.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Typography gutterBottom>效果强度: {intensity.toFixed(1)}</Typography>
      <Slider
        value={intensity}
        min={0.1}
        max={2.0}
        step={0.1}
        onChange={(_, value) => setIntensity(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
      />
    </Box>
  );
};

export default FilterSettingsComponent; 