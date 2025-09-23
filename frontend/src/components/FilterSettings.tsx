import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Grid,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  Slider,
  Box,
  Divider,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FilterParameterControl from './FilterParameterControl';
import { FilterOption } from '../types/api';
import { 
  FILTER_GROUPS, 
  FILTER_PARAMETERS 
} from '../config/filterConfig';
import styles from './FilterSettings.module.css';

interface FilterSettingsProps {
  selectedFilter: string;
  currentTabIndex: number;
  intensity: number;
  paramValues: { [key: string]: any };
  filterOptions: FilterOption[];
  isLoading: boolean;
  onTabChange: (index: number) => void;
  onFilterChange: (filterType: string) => void;
  onIntensityChange: (intensity: number) => void;
  onParameterChange: (paramName: string, value: any) => void;
  onApplyFilter: () => void;
}

const FilterSettings: React.FC<FilterSettingsProps> = ({
  selectedFilter,
  currentTabIndex,
  intensity,
  paramValues,
  filterOptions,
  isLoading,
  onTabChange,
  onFilterChange,
  onIntensityChange,
  onParameterChange,
  onApplyFilter,
}) => {
  const getCurrentTabFilters = () => {
    if (currentTabIndex >= 0 && currentTabIndex < FILTER_GROUPS.length) {
      const groupFilters = FILTER_GROUPS[currentTabIndex].filters;
      return filterOptions.filter(f => groupFilters.includes(f.value));
    }
    return [];
  };

  const handleFilterSelectChange = (event: SelectChangeEvent<string>) => {
    onFilterChange(event.target.value);
  };

  return (
    <Paper elevation={2} className={styles.paramForm}>
      <Typography variant="h6" gutterBottom>
        滤镜设置
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <Tabs
        value={currentTabIndex}
        onChange={(_, newValue) => onTabChange(newValue)}
        variant="scrollable"
        scrollButtons="auto"
        sx={{ mb: 2 }}
      >
        {FILTER_GROUPS.map((group) => (
          <Tab key={group.name} label={group.label} />
        ))}
      </Tabs>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>滤镜类型</InputLabel>
            <Select
              value={selectedFilter}
              label="滤镜类型"
              onChange={handleFilterSelectChange}
            >
              {getCurrentTabFilters().map((filter) => (
                <MenuItem key={filter.value} value={filter.value}>
                  {filter.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <Typography gutterBottom>效果强度: {intensity.toFixed(1)}</Typography>
          <Slider
            value={intensity}
            min={0.1}
            max={2.0}
            step={0.1}
            onChange={(_, value) => onIntensityChange(value as number)}
            valueLabelDisplay="auto"
          />
        </Grid>

        {selectedFilter && FILTER_PARAMETERS[selectedFilter] && (
          <Grid item xs={12}>
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>高级参数</Typography>
              </AccordionSummary>
              <AccordionDetails>
                {FILTER_PARAMETERS[selectedFilter].map((param) => (
                  <FilterParameterControl
                    key={param.name}
                    parameter={param}
                    value={paramValues[param.name]}
                    onChange={(value) => onParameterChange(param.name, value)}
                  />
                ))}
              </AccordionDetails>
            </Accordion>
          </Grid>
        )}

        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            onClick={onApplyFilter}
            disabled={isLoading || !selectedFilter}
            fullWidth
          >
            应用滤镜
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default FilterSettings; 