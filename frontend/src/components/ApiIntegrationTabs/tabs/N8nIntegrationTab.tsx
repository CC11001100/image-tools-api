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
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import HttpIcon from '@mui/icons-material/Http';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import LinkIcon from '@mui/icons-material/Link';
import { ApiEndpoint } from '../../../types/api';
import { CodeBlock } from '../../CodeBlock';
import { API_BASE_URL } from '../../../config/constants';

interface N8nIntegrationTabProps {
  endpoint: ApiEndpoint;
}

export const N8nIntegrationTab: React.FC<N8nIntegrationTabProps> = ({
  endpoint,
}) => {
  const n8nNodeConfig = {
    name: `图片处理-${endpoint.description}`,
    description: `${endpoint.description}功能节点`,
    endpoint: endpoint.path,
    urlEndpoint: endpoint.urlPath,
  };

  const httpNodeConfig = `{
  "method": "POST",
  "url": "${API_BASE_URL}${endpoint.path}",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "Content-Type",
        "value": "multipart/form-data"
      }
    ]
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "file",
        "value": "={{$binary.data}}",
        "type": "file"
      }
    ]
  },
  "options": {
    "timeout": 30000,
    "redirect": "follow"
  }
}`;

  const workflowExample = `{
  "nodes": [
    {
      "parameters": {},
      "name": "开始触发",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [240, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "${API_BASE_URL}${endpoint.path}",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "multipart/form-data"
            }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "file",
              "value": "={{$binary.data}}"
            }
          ]
        }
      },
      "name": "${n8nNodeConfig.name}",
      "type": "n8n-nodes-base.httpRequest",
      "position": [460, 300]
    }
  ],
  "connections": {
    "开始触发": {
      "main": [
        [
          {
            "node": "${n8nNodeConfig.name}",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}`;

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        <AccountTreeIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
        n8n接入
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          n8n是一个开源的工作流自动化平台。通过HTTP Request节点，
          您可以将图片处理功能集成到自动化工作流中，实现批量处理、定时任务等功能。
        </Typography>
      </Alert>

      {/* 集成方式 */}
      <Typography variant="subtitle1" gutterBottom sx={{ mt: 3 }}>
        集成方式
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <UploadFileIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">文件上传模式</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                使用HTTP Request节点的multipart/form-data方式上传图片文件进行处理
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <LinkIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">URL输入模式</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                使用HTTP Request节点的JSON方式传入图片URL地址进行处理
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Divider sx={{ my: 3 }} />

      {/* 应用场景 */}
      <Typography variant="subtitle1" gutterBottom>
        应用场景
      </Typography>
      <List dense>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="批量图片处理"
            secondary="自动处理文件夹中的所有图片"
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="定时任务处理"
            secondary="定期处理新上传的图片"
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="工作流集成"
            secondary="与其他服务组合形成完整的自动化流程"
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="API监控和通知"
            secondary="处理完成后自动发送通知或保存结果"
          />
        </ListItem>
      </List>

      <Divider sx={{ my: 3 }} />

      {/* HTTP Request节点配置 */}
      <Typography variant="subtitle1" gutterBottom>
        HTTP Request节点配置
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        在n8n中添加HTTP Request节点，使用以下配置：
      </Typography>
      <CodeBlock
        code={httpNodeConfig}
        language="json"
        title="HTTP Request节点配置"
      />

      <Divider sx={{ my: 3 }} />

      {/* 工作流示例 */}
      <Typography variant="subtitle1" gutterBottom>
        工作流示例
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        完整的n8n工作流配置示例：
      </Typography>
      <CodeBlock
        code={workflowExample}
        language="json"
        title="n8n-workflow.json"
      />

      <Divider sx={{ my: 3 }} />

      {/* 使用步骤 */}
      <Typography variant="subtitle1" gutterBottom>
        使用步骤
      </Typography>
      <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
        <Typography variant="body2" component="div">
          <ol>
            <li>在n8n中创建新的工作流</li>
            <li>添加触发器节点（Manual Trigger、Webhook等）</li>
            <li>添加HTTP Request节点并配置API参数</li>
            <li>配置图片输入方式（文件或URL）</li>
            <li>添加后续处理节点（保存文件、发送通知等）</li>
            <li>测试并激活工作流</li>
          </ol>
        </Typography>
      </Paper>

      <Divider sx={{ my: 3 }} />

      {/* 相关链接 */}
      <Typography variant="subtitle1" gutterBottom>
        相关资源
      </Typography>
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip
          label="n8n官网"
          component={Link}
          href="https://n8n.io/"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
        <Chip
          label="HTTP Request节点文档"
          component={Link}
          href="https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
        <Chip
          label="工作流示例"
          component={Link}
          href="https://n8n.io/workflows/"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
      </Box>
    </Box>
  );
};
