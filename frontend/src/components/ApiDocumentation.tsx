import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DescriptionIcon from '@mui/icons-material/Description';
import { UniversalApiDocumentation } from './documentation/UniversalApiDocumentation';
import { ApiEndpoint } from '../types/api';

interface ApiDocumentationProps {
  endpoint: ApiEndpoint;
  title?: string;
  additionalInfo?: React.ReactNode;
}

export const ApiDocumentation: React.FC<ApiDocumentationProps> = ({
  endpoint,
  title,
  additionalInfo,
}) => {
  return (
    <Paper sx={{ p: 3 }}>
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">
            <DescriptionIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
            API 文档
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box>
            {title && (
              <Typography variant="subtitle1" gutterBottom>
                {title}
              </Typography>
            )}
            
            {additionalInfo}

            <UniversalApiDocumentation endpoint={endpoint} />
          </Box>
        </AccordionDetails>
      </Accordion>
    </Paper>
  );
}; 