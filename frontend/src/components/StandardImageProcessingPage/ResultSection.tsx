import React from 'react';
import {
  Typography,
  Paper,
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DescriptionIcon from '@mui/icons-material/Description';
import { ApiDocumentation } from '../ApiDocumentation';
import { ClickableImage } from '../ClickableImage';
import { ApiEndpoint } from '../../types/api';

interface ResultSectionProps {
  resultImage: string | null;
  downloadFileName: string;
  endpoint: ApiEndpoint;
}

export const ResultSection: React.FC<ResultSectionProps> = ({
  resultImage,
  downloadFileName,
  endpoint,
}) => {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        处理结果
      </Typography>
      {resultImage && (
        <>
          <ClickableImage
            src={resultImage}
            alt="处理后图片"
            title="处理结果"
            style={{ 
              maxWidth: '100%', 
              height: 'auto', 
              border: '1px solid #ddd'
            }}
            downloadFileName={downloadFileName}
          />
          <Button 
            fullWidth
            variant="outlined" 
            color="primary" 
            sx={{ mt: 2 }}
            href={resultImage}
            download={downloadFileName}
          >
            下载图片
          </Button>
        </>
      )}

      <Accordion defaultExpanded sx={{ mt: 3 }}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">
            <DescriptionIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
            API 文档
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <ApiDocumentation endpoint={endpoint} />
        </AccordionDetails>
      </Accordion>
    </Paper>
  );
}; 