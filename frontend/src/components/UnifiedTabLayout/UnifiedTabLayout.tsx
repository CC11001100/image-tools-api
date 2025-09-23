import React, { useState } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
} from '@mui/material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`unified-tabpanel-${index}`}
      aria-labelledby={`unified-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

interface TabConfig {
  label: string;
  icon?: React.ReactElement;
  content: React.ReactNode;
}

interface UnifiedTabLayoutProps {
  title?: string;
  tabs: TabConfig[];
  defaultTab?: number;
  variant?: 'standard' | 'scrollable' | 'fullWidth';
  orientation?: 'horizontal' | 'vertical';
}

export const UnifiedTabLayout: React.FC<UnifiedTabLayoutProps> = ({
  title,
  tabs,
  defaultTab = 0,
  variant = 'scrollable',
  orientation = 'horizontal',
}) => {
  const [value, setValue] = useState(defaultTab);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const tabsProps = {
    value,
    onChange: handleChange,
    'aria-label': title ? `${title}标签页` : '标签页',
    variant: variant === 'scrollable' ? 'scrollable' as const : variant,
    scrollButtons: variant === 'scrollable' ? 'auto' as const : false,
    orientation,
  };

  return (
    <Box sx={{ width: '100%' }}>
      {title && (
        <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
          {title}
        </Typography>
      )}
      
      <Paper sx={{ width: '100%', boxShadow: 1 }}>
        <Box sx={{
          borderBottom: orientation === 'horizontal' ? 1 : 0,
          borderRight: orientation === 'vertical' ? 1 : 0,
          borderColor: 'divider',
          display: orientation === 'vertical' ? 'flex' : 'block'
        }}>
          {orientation === 'vertical' && (
            <Box sx={{ minWidth: 200, borderRight: 1, borderColor: 'divider' }}>
              <Tabs {...tabsProps}>
                {tabs.map((tab, index) => (
                  <Tab
                    key={index}
                    label={tab.label}
                    icon={tab.icon}
                    iconPosition="start"
                    id={`unified-tab-${index}`}
                    aria-controls={`unified-tabpanel-${index}`}
                    sx={{ 
                      justifyContent: 'flex-start',
                      minHeight: 48,
                      textAlign: 'left'
                    }}
                  />
                ))}
              </Tabs>
            </Box>
          )}
          
          {orientation === 'horizontal' && (
            <Tabs {...tabsProps} sx={{ minHeight: 48 }}>
              {tabs.map((tab, index) => (
                <Tab
                  key={index}
                  label={tab.label}
                  icon={tab.icon}
                  iconPosition="start"
                  id={`unified-tab-${index}`}
                  aria-controls={`unified-tabpanel-${index}`}
                  sx={{
                    minHeight: 48,
                    fontWeight: 500,
                    '&.Mui-selected': {
                      fontWeight: 600,
                    }
                  }}
                />
              ))}
            </Tabs>
          )}
        </Box>
        
        <Box sx={{ flex: 1 }}>
          {tabs.map((tab, index) => (
            <TabPanel key={index} value={value} index={index}>
              {tab.content}
            </TabPanel>
          ))}
        </Box>
      </Paper>
    </Box>
  );
};
