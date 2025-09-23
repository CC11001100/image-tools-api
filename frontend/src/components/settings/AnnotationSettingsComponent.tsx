import React, { useState, useEffect } from 'react';
import {
  TextField,
  Slider,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
} from '@mui/material';

interface Annotation {
  type: string;
  x: number;
  y: number;
  width?: number;
  height?: number;
  text?: string;
  color: string;
  thickness: number;
}

interface AnnotationSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const AnnotationSettingsComponent: React.FC<AnnotationSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [annotation, setAnnotation] = useState<Annotation>({
    type: 'rectangle',
    x: 100,
    y: 100,
    width: 200,
    height: 150,
    text: '',
    color: '#FF0000',
    thickness: 3,
  });
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    // 构建符合后端API的参数结构
    const settings: any = {
      annotation_type: annotation.type,
      color: annotation.color,
      position: `${annotation.x},${annotation.y}`,
      size: 1.0, // 默认大小
      quality: quality,
    };

    // 添加文字内容（如果是文字标注）
    if (annotation.type === 'text' && annotation.text) {
      settings.text = annotation.text;
    }

    onSettingsChange(settings);
  }, [annotation, quality, onSettingsChange]);

  const updateAnnotation = (field: string, value: any) => {
    setAnnotation({ ...annotation, [field]: value });
  };

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom>
        标注设置
      </Typography>

      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>标注类型</InputLabel>
        <Select
          value={annotation.type}
          label="标注类型"
          onChange={(e) => updateAnnotation('type', e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="rectangle">矩形</MenuItem>
          <MenuItem value="circle">圆形</MenuItem>
          <MenuItem value="arrow">箭头</MenuItem>
          <MenuItem value="text">文字</MenuItem>
          <MenuItem value="highlight">高亮</MenuItem>
        </Select>
      </FormControl>

      <Grid container spacing={2}>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="X坐标"
            type="number"
            value={annotation.x}
            onChange={(e) => updateAnnotation('x', parseInt(e.target.value) || 0)}
            disabled={isLoading}
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="Y坐标"
            type="number"
            value={annotation.y}
            onChange={(e) => updateAnnotation('y', parseInt(e.target.value) || 0)}
            disabled={isLoading}
          />
        </Grid>
      </Grid>

      {annotation.type === 'text' && (
        <TextField
          fullWidth
          label="文字内容"
          value={annotation.text}
          onChange={(e) => updateAnnotation('text', e.target.value)}
          disabled={isLoading}
          sx={{ mt: 2 }}
        />
      )}

      <Grid container spacing={2} sx={{ mt: 1 }}>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="颜色"
            type="color"
            value={annotation.color}
            onChange={(e) => updateAnnotation('color', e.target.value)}
            disabled={isLoading}
          />
        </Grid>
      </Grid>

      <Typography variant="subtitle1" gutterBottom sx={{ mt: 3 }}>
        输出设置
      </Typography>

      <Typography gutterBottom>输出质量: {quality}%</Typography>
      <Slider
        value={quality}
        min={10}
        max={100}
        step={5}
        onChange={(_, value) => setQuality(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
      />
    </Box>
  );
};

export default AnnotationSettingsComponent; 