import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
  Box,
  FormControlLabel,
  Checkbox,
} from '@mui/material';

interface NoiseSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const NoiseSettingsComponent: React.FC<NoiseSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [noiseType, setNoiseType] = useState('gaussian');
  const [amount, setAmount] = useState(10);
  const [monochrome, setMonochrome] = useState(false);
  const [seed, setSeed] = useState<number | null>(null);
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      noise_type: noiseType,
      amount: amount,
      monochrome: monochrome,
      quality: quality,
    };

    if (seed !== null) {
      settings.seed = seed;
    }

    onSettingsChange(settings);
  }, [noiseType, amount, monochrome, seed, quality, onSettingsChange]);

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>噪点类型</InputLabel>
        <Select
          value={noiseType}
          label="噪点类型"
          onChange={(e) => setNoiseType(e.target.value)}
          disabled={isLoading}
        >
          <MenuItem value="gaussian">高斯噪点</MenuItem>
          <MenuItem value="salt_pepper">椒盐噪点</MenuItem>
          <MenuItem value="poisson">泊松噪点</MenuItem>
          <MenuItem value="speckle">斑点噪点</MenuItem>
          <MenuItem value="uniform">均匀噪点</MenuItem>
        </Select>
      </FormControl>

      <Typography gutterBottom>噪点强度: {amount}%</Typography>
      <Slider
        value={amount}
        min={0}
        max={100}
        onChange={(_, value) => setAmount(value as number)}
        valueLabelDisplay="auto"
        disabled={isLoading}
        marks={[
          { value: 0, label: '0%' },
          { value: 50, label: '50%' },
          { value: 100, label: '100%' },
        ]}
        sx={{ mb: 3 }}
      />

      <FormControlLabel
        control={
          <Checkbox
            checked={monochrome}
            onChange={(e) => setMonochrome(e.target.checked)}
            disabled={isLoading}
          />
        }
        label="单色噪点"
        sx={{ mb: 2 }}
      />

      <FormControlLabel
        control={
          <Checkbox
            checked={seed !== null}
            onChange={(e) => setSeed(e.target.checked ? 42 : null)}
            disabled={isLoading}
          />
        }
        label="使用固定随机种子"
        sx={{ mb: 3 }}
      />

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

export default NoiseSettingsComponent; 