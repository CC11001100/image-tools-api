import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
  Box,
  Button,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';

interface StitchSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const StitchSettingsComponent: React.FC<StitchSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [direction, setDirection] = useState('horizontal');
  const [gap, setGap] = useState(0);
  const [backgroundColor, setBackgroundColor] = useState('#FFFFFF');
  const [additionalImages, setAdditionalImages] = useState<File[]>([]);
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      direction: direction,
      gap: gap,
      background_color: backgroundColor,
      additional_images: additionalImages,
      quality: quality,
    };

    onSettingsChange(settings);
  }, [direction, gap, backgroundColor, additionalImages, quality, onSettingsChange]);

  const handleAddImages = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const newFiles = Array.from(event.target.files);
      setAdditionalImages([...additionalImages, ...newFiles]);
    }
  };

  const handleRemoveImage = (index: number) => {
    const newImages = [...additionalImages];
    newImages.splice(index, 1);
    setAdditionalImages(newImages);
  };

  return (
    <Box>
      <Alert severity="info" sx={{ mb: 3 }}>
        拼接功能需要至少两张图片：基础图片和要拼接的图片
      </Alert>

      <Typography variant="subtitle1" gutterBottom>
        添加要拼接的图片
      </Typography>
      <Button
        variant="outlined"
        component="label"
        startIcon={<CloudUploadIcon />}
        fullWidth
        sx={{ mb: 2 }}
        disabled={isLoading}
      >
        选择图片（可多选）
        <input
          type="file"
          hidden
          multiple
          accept="image/*"
          onChange={handleAddImages}
          disabled={isLoading}
        />
      </Button>

      {additionalImages.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            已选择 {additionalImages.length} 张图片
          </Typography>
          <List dense>
            {additionalImages.map((file, index) => (
              <ListItem key={index}>
                <ListItemText primary={file.name} />
                <ListItemSecondaryAction>
                  <IconButton 
                    edge="end" 
                    onClick={() => handleRemoveImage(index)}
                    disabled={isLoading}
                  >
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Box>
      )}

      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>拼接方向</InputLabel>
        <Select
          value={direction}
          label="拼接方向"
          onChange={(e) => setDirection(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="horizontal">水平拼接</MenuItem>
          <MenuItem value="vertical">垂直拼接</MenuItem>
          <MenuItem value="grid">网格拼接</MenuItem>
        </Select>
      </FormControl>

      <TextField
        fullWidth
        label="间隙大小（像素）"
        type="number"
        value={gap}
        onChange={(e) => setGap(parseInt(e.target.value) || 0)}
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <TextField
        fullWidth
        label="背景颜色"
        type="color"
        value={backgroundColor}
        onChange={(e) => setBackgroundColor(e.target.value)}
        disabled={isLoading}
        sx={{ mb: 3 }}
      />

      <TextField
        fullWidth
        label="输出质量"
        type="number"
        value={quality}
        onChange={(e) => setQuality(parseInt(e.target.value) || 90)}
        disabled={isLoading}
        inputProps={{ min: 10, max: 100 }}
      />
    </Box>
  );
};

export default StitchSettingsComponent; 