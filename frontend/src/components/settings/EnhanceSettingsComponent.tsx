import React, { useState, useEffect } from 'react';
import {
  Slider,
  Typography,
  Box,
  Grid,
} from '@mui/material';

interface EnhanceSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const EnhanceSettingsComponent: React.FC<EnhanceSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [brightness, setBrightness] = useState(1.0);
  const [contrast, setContrast] = useState(1.0);
  const [saturation, setSaturation] = useState(1.0);
  const [sharpness, setSharpness] = useState(1.0);
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    onSettingsChange({
      brightness,
      contrast,
      saturation,
      sharpness,
      quality,
    });
  }, [brightness, contrast, saturation, sharpness, quality, onSettingsChange]);

  return (
    <Box>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography gutterBottom>亮度: {brightness.toFixed(2)}</Typography>
          <Slider
            value={brightness}
            min={0}
            max={2}
            step={0.05}
            onChange={(_, value) => setBrightness(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            marks={[
              { value: 0, label: '0' },
              { value: 1, label: '1' },
              { value: 2, label: '2' },
            ]}
          />
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>对比度: {contrast.toFixed(2)}</Typography>
          <Slider
            value={contrast}
            min={0}
            max={2}
            step={0.05}
            onChange={(_, value) => setContrast(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            marks={[
              { value: 0, label: '0' },
              { value: 1, label: '1' },
              { value: 2, label: '2' },
            ]}
          />
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>饱和度: {saturation.toFixed(2)}</Typography>
          <Slider
            value={saturation}
            min={0}
            max={2}
            step={0.05}
            onChange={(_, value) => setSaturation(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            marks={[
              { value: 0, label: '0' },
              { value: 1, label: '1' },
              { value: 2, label: '2' },
            ]}
          />
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>锐度: {sharpness.toFixed(2)}</Typography>
          <Slider
            value={sharpness}
            min={0}
            max={2}
            step={0.05}
            onChange={(_, value) => setSharpness(value as number)}
            valueLabelDisplay="auto"
            disabled={isLoading}
            marks={[
              { value: 0, label: '0' },
              { value: 1, label: '1' },
              { value: 2, label: '2' },
            ]}
          />
        </Grid>

        <Grid item xs={12}>
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
        </Grid>
      </Grid>
    </Box>
  );
};

export default EnhanceSettingsComponent; 