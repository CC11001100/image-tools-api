import React from 'react';
import {
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Divider,
  Chip,
  Alert,
  Paper,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useApiRequest } from '../../hooks/useApiRequest';
import { ApiEndpoint } from '../../types/api';

interface UniversalApiDocumentationProps {
  endpoint: ApiEndpoint;
  settings?: any;
}

export const UniversalApiDocumentation: React.FC<UniversalApiDocumentationProps> = ({
  endpoint,
  settings = {},
}) => {
  const { generateCurlCommand } = useApiRequest();

  const generateFileCurlCommand = () => {
    return generateCurlCommand(endpoint.path, settings, false);
  };

  const generateUrlCurlCommand = () => {
    return generateCurlCommand(endpoint.urlPath, settings, true);
  };

  return (
    <Box>
      {/* 接口基本信息 */}
      <Typography variant="subtitle1" gutterBottom>
        接口说明
      </Typography>
      <Typography variant="body2" paragraph>
        {endpoint.description}
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          本接口支持两种调用方式：
          <br />• <strong>文件上传模式</strong>：使用multipart/form-data格式上传本地图片文件
          <br />• <strong>URL模式</strong>：使用application/json格式，传入图片URL地址
        </Typography>
      </Alert>

      {/* 接口端点信息 */}
      <Typography variant="subtitle1" gutterBottom>
        请求端点
      </Typography>
      <Table size="small" sx={{ mb: 3 }}>
        <TableHead>
          <TableRow>
            <TableCell><strong>调用方式</strong></TableCell>
            <TableCell><strong>请求方法</strong></TableCell>
            <TableCell><strong>接口路径</strong></TableCell>
            <TableCell><strong>Content-Type</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>文件上传</TableCell>
            <TableCell>
              <Chip label={endpoint.method} color="primary" size="small" />
            </TableCell>
            <TableCell>
              <code>{endpoint.path}</code>
            </TableCell>
            <TableCell>
              <code>{endpoint.requestType.file}</code>
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell>URL输入</TableCell>
            <TableCell>
              <Chip label={endpoint.method} color="primary" size="small" />
            </TableCell>
            <TableCell>
              <code>{endpoint.urlPath}</code>
            </TableCell>
            <TableCell>
              <code>{endpoint.requestType.url}</code>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>

      {/* 参数说明 */}
      <Typography variant="subtitle1" gutterBottom>
        参数说明
      </Typography>
      <Table size="small" sx={{ mb: 3 }}>
        <TableHead>
          <TableRow>
            <TableCell><strong>参数名</strong></TableCell>
            <TableCell><strong>类型</strong></TableCell>
            <TableCell><strong>必需</strong></TableCell>
            <TableCell><strong>说明</strong></TableCell>
            <TableCell><strong>默认值</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {endpoint.parameters?.map((param, index) => (
            <TableRow key={index}>
              <TableCell>
                <code>{param.name}</code>
              </TableCell>
              <TableCell>
                <Chip label={param.type} size="small" />
              </TableCell>
              <TableCell>
                {param.required ? (
                  <Chip label="是" color="error" size="small" />
                ) : (
                  <Chip label="否" color="default" size="small" />
                )}
              </TableCell>
              <TableCell>
                {param.description}
                {param.options && (
                  <div>
                    <small>
                      可选值：{param.options.join('、')}
                    </small>
                  </div>
                )}
                {(param.min !== undefined || param.max !== undefined) && (
                  <div>
                    <small>
                      取值范围：{param.min !== undefined ? param.min : '∞'} ~ {param.max !== undefined ? param.max : '∞'}
                    </small>
                  </div>
                )}
              </TableCell>
              <TableCell>
                {param.defaultValue !== undefined ? (
                  <code>{JSON.stringify(param.defaultValue)}</code>
                ) : (
                  '-'
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* 响应格式 */}
      <Typography variant="subtitle1" gutterBottom>
        响应格式
      </Typography>
      <Box sx={{ mb: 3 }}>
        <Typography variant="body2" gutterBottom>
          成功响应：
        </Typography>
        <code>Content-Type: {endpoint.responseType}</code>
        
        <Typography variant="body2" sx={{ mt: 2 }} gutterBottom>
          错误响应：
        </Typography>
        <code>Content-Type: application/json</code>
        <pre style={{ margin: '10px 0' }}>
{`{
  "detail": "错误信息描述"
}`}
        </pre>
      </Box>

      {/* 错误码说明 */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1">错误码说明</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell><strong>状态码</strong></TableCell>
                <TableCell><strong>说明</strong></TableCell>
                <TableCell><strong>处理建议</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>400</TableCell>
                <TableCell>请求参数错误</TableCell>
                <TableCell>检查参数格式、必需参数是否提供、参数值是否在有效范围内</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>404</TableCell>
                <TableCell>资源不存在</TableCell>
                <TableCell>检查URL地址是否正确、图片是否存在</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>415</TableCell>
                <TableCell>不支持的媒体类型</TableCell>
                <TableCell>检查上传的图片格式是否支持、Content-Type是否正确设置</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>422</TableCell>
                <TableCell>处理失败</TableCell>
                <TableCell>检查图片大小、分辨率是否符合要求，调整参数后重试</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>500</TableCell>
                <TableCell>服务器错误</TableCell>
                <TableCell>服务器内部错误，请稍后重试或联系管理员</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </AccordionDetails>
      </Accordion>

      {/* 最佳实践 */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1">最佳实践</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" gutterBottom>
            1. 图片上传建议：
          </Typography>
          <ul>
            <li>推荐使用文件上传模式处理本地图片</li>
            <li>使用URL模式处理网络图片</li>
            <li>支持的图片格式：JPEG、PNG、WebP、GIF</li>
            <li>建议图片大小不超过10MB</li>
          </ul>

          <Typography variant="body2" gutterBottom>
            2. 参数设置建议：
          </Typography>
          <ul>
            <li>设置合适的参数值，避免过度处理</li>
            <li>注意参数之间的依赖关系</li>
            <li>使用默认值作为起点逐步调整</li>
          </ul>

          <Typography variant="body2" gutterBottom>
            3. 性能优化建议：
          </Typography>
          <ul>
            <li>可以预先压缩大图片</li>
            <li>批量处理时建议使用URL模式</li>
            <li>合理设置输出质量参数</li>
          </ul>

          <Typography variant="body2" gutterBottom>
            4. 错误处理建议：
          </Typography>
          <ul>
            <li>实现错误重试机制</li>
            <li>添加超时处理</li>
            <li>做好用户提示</li>
          </ul>
        </AccordionDetails>
      </Accordion>

      {/* 请求示例 */}
      <Typography variant="subtitle1" sx={{ mt: 3, mb: 2 }}>
        请求示例
      </Typography>
      
      <Typography variant="body2" gutterBottom>
        <strong>文件上传模式：</strong>
      </Typography>
      <Paper sx={{ p: 2, bgcolor: 'grey.100', mb: 2 }}>
        <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
          {generateFileCurlCommand()}
        </pre>
      </Paper>

      <Typography variant="body2" gutterBottom>
        <strong>URL输入模式：</strong>
      </Typography>
      <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
        <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
          {generateUrlCurlCommand()}
        </pre>
      </Paper>
    </Box>
  );
}; 