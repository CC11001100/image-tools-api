import React, { useState } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
} from '@mui/material';
import DescriptionIcon from '@mui/icons-material/Description';
import IntegrationInstructionsIcon from '@mui/icons-material/IntegrationInstructions';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import PsychologyIcon from '@mui/icons-material/Psychology';
import FlashOnIcon from '@mui/icons-material/FlashOn';
import { ApiEndpoint } from '../../types/api';
import { HttpApiDocTab } from './tabs/HttpApiDocTab';
import { McpIntegrationTab } from './tabs/McpIntegrationTab';
import { CozeIntegrationTab } from './tabs/CozeIntegrationTab';
import { N8nIntegrationTab } from './tabs/N8nIntegrationTab';
import { DifyIntegrationTab } from './tabs/DifyIntegrationTab';
import { ZapierIntegrationTab } from './tabs/ZapierIntegrationTab';

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
      id={`integration-tabpanel-${index}`}
      aria-labelledby={`integration-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

interface ApiIntegrationTabsProps {
  endpoint: ApiEndpoint;
  title?: string;
  description?: string;
  settings?: any;
  additionalHttpContent?: React.ReactNode;
}

export const ApiIntegrationTabs: React.FC<ApiIntegrationTabsProps> = ({
  endpoint,
  title,
  description,
  settings = {},
  additionalHttpContent,
}) => {
  const [value, setValue] = useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const tabs = [
    {
      label: 'HTTP API文档',
      icon: <DescriptionIcon />,
      content: (
        <HttpApiDocTab 
          endpoint={endpoint} 
          settings={settings}
          additionalContent={additionalHttpContent}
        />
      ),
    },
    {
      label: 'MCP接入',
      icon: <IntegrationInstructionsIcon />,
      content: <McpIntegrationTab endpoint={endpoint} />,
    },
    {
      label: '扣子（Coze）接入',
      icon: <SmartToyIcon />,
      content: <CozeIntegrationTab endpoint={endpoint} />,
    },
    {
      label: 'n8n接入',
      icon: <AccountTreeIcon />,
      content: <N8nIntegrationTab endpoint={endpoint} />,
    },
    {
      label: 'Dify接入',
      icon: <PsychologyIcon />,
      content: <DifyIntegrationTab endpoint={endpoint} />,
    },
    {
      label: 'Zapier接入',
      icon: <FlashOnIcon />,
      content: <ZapierIntegrationTab endpoint={endpoint} />,
    },
  ];

  return (
    <Box sx={{ width: '100%', mb: 4 }}>
      {title && (
        <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
          {title}
        </Typography>
      )}
      
      {description && (
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          {description}
        </Typography>
      )}
      
      <Paper sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs 
            value={value} 
            onChange={handleChange} 
            aria-label="API集成标签页"
            variant="scrollable"
            scrollButtons="auto"
          >
            {tabs.map((tab, index) => (
              <Tab
                key={index}
                label={tab.label}
                icon={tab.icon}
                iconPosition="start"
                id={`integration-tab-${index}`}
                aria-controls={`integration-tabpanel-${index}`}
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
        </Box>
        
        {tabs.map((tab, index) => (
          <TabPanel key={index} value={value} index={index}>
            {tab.content}
          </TabPanel>
        ))}
      </Paper>
    </Box>
  );
};
