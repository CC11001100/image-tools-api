import React from 'react';
import { FilterOption } from '../../types/api';
import { Box } from '@mui/material';
import { BillingInfo } from '../BillingInfo';

interface ArtFilterApiDocumentationProps {
  filterOptions: FilterOption[];
  settings: any;
}

const ArtFilterApiDocumentation: React.FC<ArtFilterApiDocumentationProps> = ({ filterOptions, settings }) => {
  const renderParameters = () => {
    return Object.entries(settings)
      .filter(([key]) => key !== 'filter_type')
      .map(([key, value]) => `- ${key}: ${typeof value} (可选)`)
      .join('\n          ');
  };

  const renderJsonParameters = () => {
    return Object.entries(settings)
      .filter(([key]) => key !== 'filter_type')
      .map(([key, value]) => `"${key}": "${typeof value} (可选)"`)
      .join(',\n            ');
  };

  return (
    <Box>
      <div className="api-documentation">
        <h3>API 文档</h3>
        
        {/* 计费说明 */}
        <BillingInfo billingType="upload" defaultExpanded={false} />
        
        <div className="endpoint-section">
          <h4>文件上传接口</h4>
          <pre>
            {`POST /api/v1/art-filter
Content-Type: multipart/form-data

参数：
- image: File (必需)
- filter_type: string (必需) - 可选值: ${filterOptions.map(opt => opt.value).join(', ')}
${renderParameters()}`}
          </pre>
        </div>
        <div className="endpoint-section">
          <h4>URL 上传接口</h4>
          <pre>
            {`POST /api/v1/art-filter-by-url
Content-Type: application/json

{
  "image_url": "string (必需)",
  "filter_type": "string (必需) - 可选值: ${filterOptions.map(opt => opt.value).join(', ')}",
  ${renderJsonParameters()}
}`}
          </pre>
        </div>
      </div>
    </Box>
  );
};

export default ArtFilterApiDocumentation; 