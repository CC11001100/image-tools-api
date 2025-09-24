import React from 'react';
import {
  Box,
  Typography,
  Alert,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Link,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CodeIcon from '@mui/icons-material/Code';
import IntegrationInstructionsIcon from '@mui/icons-material/IntegrationInstructions';
import { ApiEndpoint } from '../../../types/api';
import { CodeBlock } from '../../CodeBlock';
import { API_BASE_URL } from '../../../config/constants';

interface McpIntegrationTabProps {
  endpoint: ApiEndpoint;
}

export const McpIntegrationTab: React.FC<McpIntegrationTabProps> = ({
  endpoint,
}) => {
  const mcpConfig = {
    name: `image-tools-${endpoint.path.split('/').pop()}`,
    description: endpoint.description,
    version: "1.0.0",
    endpoint: endpoint.path,
    urlEndpoint: endpoint.urlPath,
  };

  const mcpServerConfig = `{
  "mcpServers": {
    "${mcpConfig.name}": {
      "command": "node",
      "args": ["mcp-server.js"],
      "env": {
        "API_BASE_URL": "${API_BASE_URL}",
        "ENDPOINT_PATH": "${endpoint.path}",
        "ENDPOINT_URL_PATH": "${endpoint.urlPath}"
      }
    }
  }
}`;

  const mcpToolDefinition = `{
  "name": "${mcpConfig.name}",
  "description": "${endpoint.description}",
  "inputSchema": {
    "type": "object",
    "properties": {
      "image": {
        "type": "string",
        "description": "图片文件路径或URL"
      },
      "settings": {
        "type": "object",
        "description": "处理参数设置"
      }
    },
    "required": ["image"]
  }
}`;

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        <IntegrationInstructionsIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
        MCP (Model Context Protocol) 接入
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          MCP是一个开放协议，允许AI助手与外部工具和数据源安全连接。
          通过MCP接入，您可以在Claude、ChatGPT等AI助手中直接使用本图片处理功能。
        </Typography>
      </Alert>

      {/* 功能特性 */}
      <Typography variant="subtitle1" gutterBottom sx={{ mt: 3 }}>
        功能特性
      </Typography>
      <List dense>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="支持文件上传和URL输入两种模式"
            secondary="灵活的图片输入方式"
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="完整的参数配置支持"
            secondary="所有API参数都可通过MCP工具配置"
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="标准化的错误处理"
            secondary="统一的错误信息和状态码"
          />
        </ListItem>
      </List>

      <Divider sx={{ my: 3 }} />

      {/* MCP服务器配置 */}
      <Typography variant="subtitle1" gutterBottom>
        MCP服务器配置
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        将以下配置添加到您的MCP客户端配置文件中：
      </Typography>
      <CodeBlock
        code={mcpServerConfig}
        language="json"
        title="mcp-config.json"
      />

      <Divider sx={{ my: 3 }} />

      {/* 工具定义 */}
      <Typography variant="subtitle1" gutterBottom>
        工具定义
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        MCP工具的标准定义格式：
      </Typography>
      <CodeBlock
        code={mcpToolDefinition}
        language="json"
        title="tool-definition.json"
      />

      <Divider sx={{ my: 3 }} />

      {/* 使用示例 */}
      <Typography variant="subtitle1" gutterBottom>
        使用示例
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        在支持MCP的AI助手中使用：
      </Typography>
      <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
        <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
{`用户: 请帮我处理这张图片 [上传图片]
AI: 我来帮您处理这张图片。

[调用MCP工具: ${mcpConfig.name}]
参数: {
  "image": "uploaded_image.jpg",
  "settings": { /* 根据需要配置参数 */ }
}

处理完成！图片已成功处理。`}
        </Typography>
      </Paper>

      <Divider sx={{ my: 3 }} />

      {/* 相关链接 */}
      <Typography variant="subtitle1" gutterBottom>
        相关资源
      </Typography>
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip
          label="MCP官方文档"
          component={Link}
          href="https://modelcontextprotocol.io/"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
        <Chip
          label="Claude MCP指南"
          component={Link}
          href="https://docs.anthropic.com/claude/docs/mcp"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
        <Chip
          label="GitHub示例"
          component={Link}
          href="https://github.com/modelcontextprotocol/servers"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
      </Box>
    </Box>
  );
};
