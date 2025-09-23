import React from 'react';
import {
  Box,
  Typography,
  Slider,
  TextField,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import { FilterParameter } from '../config/filterConfig';

interface FilterParameterControlProps {
  parameter: FilterParameter;
  value: any;
  onChange: (value: any) => void;
}

const FilterParameterControl: React.FC<FilterParameterControlProps> = ({
  parameter,
  value,
  onChange,
}) => {
  const currentValue = value !== undefined ? value : parameter.defaultValue;

  const renderControl = () => {
    switch (parameter.type) {
      case 'slider':
        return (
          <Box sx={{ mb: 2 }}>
            <Typography id={`${parameter.name}-slider`} gutterBottom>
              {parameter.label}: {currentValue}
            </Typography>
            <Slider
              value={currentValue}
              min={parameter.min}
              max={parameter.max}
              step={parameter.step}
              onChange={(_, newValue) => onChange(newValue)}
              valueLabelDisplay="auto"
              aria-labelledby={`${parameter.name}-slider`}
            />
          </Box>
        );

      case 'color':
        return (
          <TextField
            fullWidth
            label={parameter.label}
            type="color"
            value={currentValue}
            onChange={(e) => onChange(e.target.value)}
            sx={{ mb: 2 }}
          />
        );

      case 'number':
        return (
          <TextField
            fullWidth
            label={parameter.label}
            type="number"
            value={currentValue}
            onChange={(e) => onChange(Number(e.target.value))}
            inputProps={{ 
              min: parameter.min, 
              max: parameter.max, 
              step: parameter.step 
            }}
            sx={{ mb: 2 }}
          />
        );

      case 'select':
        return (
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>{parameter.label}</InputLabel>
            <Select
              value={currentValue}
              label={parameter.label}
              onChange={(e) => onChange(e.target.value)}
            >
              {parameter.options?.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );

      default:
        return null;
    }
  };

  return renderControl();
};

export default FilterParameterControl; 