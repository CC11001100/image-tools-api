import React from 'react';
import { Box } from '@mui/material';
import { BillingInfo } from '../BillingInfo';

interface BlendApiDocumentationProps {
  settings: any;
}

const BlendApiDocumentation: React.FC<BlendApiDocumentationProps> = ({ settings }) => {
  const renderParameters = () => {
    return Object.entries(settings)
      .map(([key, value]) => `- ${key}: ${typeof value} (${key === 'blend_mode' ? '必需' : '可选'})`)
      .join('\n          ');
  };

  const renderJsonParameters = () => {
    return Object.entries(settings)
      .map(([key, value]) => `"${key}": "${typeof value} (${key === 'blend_mode' ? '必需' : '可选'})"`)
      .join(',\n            ');
  };

  return (
    <Box>
      <div className="api-documentation">
        <h3>API 文档</h3>
        
        {/* 计费说明 - 双文件上传模式 */}
        <BillingInfo billingType="dual" defaultExpanded={false} />
        
        <div className="endpoint-section">
          <h4>文件上传接口</h4>
          <pre>
            {`POST /api/v1/blend
Content-Type: multipart/form-data

参数：
- image1: File (必需) - 底图
- image2: File (必需) - 上层图片
${renderParameters()}`}
          </pre>
        </div>
        <div className="endpoint-section">
          <h4>URL 上传接口</h4>
          <pre>
            {`POST /api/v1/blend-by-url
Content-Type: application/json

{
  "image1_url": "string (必需) - 底图URL",
  "image2_url": "string (必需) - 上层图片URL",
  ${renderJsonParameters()}
}`}
          </pre>
        </div>
      </div>
    </Box>
  );
};

export default BlendApiDocumentation; 