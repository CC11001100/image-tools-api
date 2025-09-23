import React from 'react';
import { Box } from '@mui/material';
import { UniversalApiDocumentation } from '../../documentation/UniversalApiDocumentation';
import { ApiEndpoint } from '../../../types/api';

interface HttpApiDocTabProps {
  endpoint: ApiEndpoint;
  settings?: any;
  additionalContent?: React.ReactNode;
}

export const HttpApiDocTab: React.FC<HttpApiDocTabProps> = ({
  endpoint,
  settings = {},
  additionalContent,
}) => {
  return (
    <Box>
      {/* 额外内容（如果有的话） */}
      {additionalContent}
      
      {/* 标准API文档 */}
      <UniversalApiDocumentation 
        endpoint={endpoint} 
        settings={settings}
      />
    </Box>
  );
};
