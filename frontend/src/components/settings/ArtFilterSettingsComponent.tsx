import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { FILTER_PARAMETERS } from '../../config/filterParameters';

interface ArtFilterSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
  filterOptions: Array<{ value: string; label: string; description: string }>;
}

const ArtFilterSettingsComponent: React.FC<ArtFilterSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
  filterOptions,
}) => {
  const [selectedFilter, setSelectedFilter] = useState(filterOptions[0]?.value || 'oil_painting');
  const [intensity, setIntensity] = useState(1.0);
  const [params, setParams] = useState<any>({});

  // 初始化参数
  useEffect(() => {
    if (selectedFilter && FILTER_PARAMETERS[selectedFilter]) {
      const defaultParams: any = {};
      FILTER_PARAMETERS[selectedFilter].forEach(param => {
        defaultParams[param.name] = param.defaultValue;
      });
      setParams(defaultParams);
    }
  }, [selectedFilter]);

  // 更新设置
  useEffect(() => {
    onSettingsChange({
      filter_type: selectedFilter,
      intensity: intensity,
      params: JSON.stringify(params),
    });
  }, [selectedFilter, intensity, params, onSettingsChange]);

  const handleParamChange = (paramName: string, value: any) => {
    setParams((prev: any) => ({
      ...prev,
      [paramName]: value,
    }));
  };

  const renderParameterControl = (param: any) => {
    const value = params[param.name] ?? param.defaultValue;

    switch (param.type) {
      case 'slider':
        return (
          <Box key={param.name} sx={{ mb: 2 }}>
            <Typography gutterBottom>
              {param.label}: {value}
            </Typography>
            <Slider
              value={value}
              min={param.min}
              max={param.max}
              step={param.step}
              onChange={(_, newValue) => handleParamChange(param.name, newValue)}
              valueLabelDisplay="auto"
              disabled={isLoading}
            />
          </Box>
        );
      default:
        return null;
    }
  };

  return (
    <Box>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>滤镜类型</InputLabel>
        <Select
          value={selectedFilter}
          label="滤镜类型"
          onChange={(e) => setSelectedFilter(e.target.value)}
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
        sx={{ mb: 3 }}
      />

      {selectedFilter && FILTER_PARAMETERS[selectedFilter] && (
        <Accordion defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>高级参数</Typography>
          </AccordionSummary>
          <AccordionDetails>
            {FILTER_PARAMETERS[selectedFilter].map(param => 
              renderParameterControl(param)
            )}
          </AccordionDetails>
        </Accordion>
      )}
    </Box>
  );
};

export default ArtFilterSettingsComponent; 