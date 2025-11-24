import React, { useState } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Divider,
} from '@mui/material';
import { CodeBlock } from '../CodeBlock';
import { ApiEndpoint } from '../../types/api';
import { BillingInfo } from '../BillingInfo';

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
      id={`api-tabpanel-${index}`}
      aria-labelledby={`api-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

interface ApiDocumentationTabsProps {
  endpoint: ApiEndpoint;
}

export const ApiDocumentationTabs: React.FC<ApiDocumentationTabsProps> = ({
  endpoint,
}) => {
  const [value, setValue] = useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  // 文件上传接口文档
  const fileUploadDoc = {
    title: '文件上传模式',
    method: 'POST',
    path: endpoint.path,
    contentType: 'multipart/form-data',
    description: '上传本地图片文件进行处理',
    parameters: [
      { name: 'file', type: 'File', required: true, description: '要处理的图片文件', example: '(binary)' },
      { name: 'width', type: 'number', required: false, description: '目标宽度（像素）', example: '800' },
      { name: 'height', type: 'number', required: false, description: '目标高度（像素）', example: '600' },
      { name: 'maintain_aspect', type: 'boolean', required: false, description: '保持宽高比', example: 'true' },
      { name: 'quality', type: 'number', required: false, description: '输出质量(1-100)', example: '90' },
    ],
    requestExample: `curl -X POST "${window.location.origin}${endpoint.path}" \\
  -H "Authorization: Bearer YOUR_API_TOKEN" \\
  -F "file=@your_image.jpg" \\
  -F "width=800" \\
  -F "maintain_aspect=true" \\
  -F "quality=90"`,
    responseExample: `Content-Type: image/jpeg
Content-Length: 245760

(二进制图片数据)`,
    errorExample: `{
  "detail": "文件格式不支持，请上传 JPG、PNG、GIF、BMP、WebP 格式的图片"
}`
  };

  // URL输入接口文档
  const urlInputDoc = {
    title: 'URL输入模式',
    method: 'POST',
    path: endpoint.urlPath || '/api/v1/resize-by-url',
    contentType: 'multipart/form-data',
    description: '通过图片URL进行处理',
    parameters: [
      { name: 'image_url', type: 'string', required: true, description: '图片URL地址', example: 'https://example.com/image.jpg' },
      { name: 'width', type: 'number', required: false, description: '目标宽度（像素）', example: '800' },
      { name: 'height', type: 'number', required: false, description: '目标高度（像素）', example: '600' },
      { name: 'maintain_aspect', type: 'boolean', required: false, description: '保持宽高比', example: 'true' },
      { name: 'quality', type: 'number', required: false, description: '输出质量(1-100)', example: '90' },
    ],
    requestExample: `curl -X POST "${window.location.origin}${endpoint.urlPath || '/api/v1/resize-by-url'}" \\
  -H "Authorization: Bearer YOUR_API_TOKEN" \\
  -F "image_url=https://example.com/image.jpg" \\
  -F "width=800" \\
  -F "maintain_aspect=true" \\
  -F "quality=90"`,
    responseExample: `Content-Type: image/jpeg
Content-Length: 245760

(二进制图片数据)`,
    errorExample: `{
  "detail": "无法下载图片，请检查URL是否正确"
}`
  };

  const renderApiDoc = (doc: typeof fileUploadDoc, isUrlMode: boolean = false) => (
    <Box>
      {/* 接口基本信息 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          接口信息
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Chip label={doc.method} color="primary" size="small" />
          <Typography variant="body1" component="code" sx={{ 
            backgroundColor: '#f5f5f5', 
            padding: '4px 8px', 
            borderRadius: 1,
            fontFamily: 'monospace'
          }}>
            {doc.path}
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary">
          {doc.description}
        </Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>
          <strong>Content-Type:</strong> {doc.contentType}
        </Typography>
      </Box>

      <Divider sx={{ my: 3 }} />

      {/* 计费说明 */}
      <BillingInfo billingType={isUrlMode ? 'url' : 'upload'} defaultExpanded={false} />

      <Divider sx={{ my: 3 }} />

      {/* 请求参数 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          请求参数
        </Typography>
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell><strong>参数名</strong></TableCell>
                <TableCell><strong>类型</strong></TableCell>
                <TableCell><strong>必需</strong></TableCell>
                <TableCell><strong>说明</strong></TableCell>
                <TableCell><strong>示例</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {doc.parameters.map((param) => (
                <TableRow key={param.name}>
                  <TableCell component="code" sx={{ fontFamily: 'monospace' }}>
                    {param.name}
                  </TableCell>
                  <TableCell>
                    <Chip label={param.type} size="small" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={param.required ? '是' : '否'} 
                      size="small" 
                      color={param.required ? 'error' : 'default'}
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>{param.description}</TableCell>
                  <TableCell component="code" sx={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>
                    {param.example}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>

      <Divider sx={{ my: 3 }} />

      {/* 请求示例 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          请求示例
        </Typography>
        <CodeBlock
          code={doc.requestExample}
          language="bash"
          title="cURL 请求示例"
        />
      </Box>

      <Divider sx={{ my: 3 }} />

      {/* 响应示例 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          成功响应
        </Typography>
        <CodeBlock
          code={doc.responseExample}
          language="http"
          title="HTTP 200 OK"
        />
      </Box>

      {/* 错误响应 */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          错误响应
        </Typography>
        <CodeBlock
          code={doc.errorExample}
          language="json"
          title="HTTP 400/500 Error"
        />
      </Box>
    </Box>
  );

  return (
    <Box sx={{ mb: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
        📚 API 文档
      </Typography>
      
      <Paper sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={value} onChange={handleChange} aria-label="API文档标签">
            <Tab label="文件上传模式" id="api-tab-0" aria-controls="api-tabpanel-0" />
            <Tab label="URL输入模式" id="api-tab-1" aria-controls="api-tabpanel-1" />
          </Tabs>
        </Box>
        
        <TabPanel value={value} index={0}>
          {renderApiDoc(fileUploadDoc, false)}
        </TabPanel>
        
        <TabPanel value={value} index={1}>
          {renderApiDoc(urlInputDoc, true)}
        </TabPanel>
      </Paper>
    </Box>
  );
};
