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
  Step,
  Stepper,
  StepLabel,
  StepContent,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import { ApiEndpoint } from '../../../types/api';
import { CodeBlock } from '../../CodeBlock';

interface CozeIntegrationTabProps {
  endpoint: ApiEndpoint;
}

export const CozeIntegrationTab: React.FC<CozeIntegrationTabProps> = ({
  endpoint,
}) => {
  const cozePluginConfig = {
    name: `图片处理-${endpoint.description}`,
    description: `${endpoint.description}功能插件`,
    api_endpoint: endpoint.path,
    url_endpoint: endpoint.urlPath,
  };

  const cozeApiSchema = `{
  "openapi": "3.0.0",
  "info": {
    "title": "${cozePluginConfig.name}",
    "description": "${cozePluginConfig.description}",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "http://localhost:58888",
      "description": "本地开发服务器"
    }
  ],
  "paths": {
    "${endpoint.path}": {
      "post": {
        "summary": "${endpoint.description}",
        "description": "${endpoint.description}功能接口",
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "file": {
                    "type": "string",
                    "format": "binary",
                    "description": "要处理的图片文件"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "处理成功",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "processed_image_url": {
                      "type": "string",
                      "description": "处理后的图片URL"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}`;

  const steps = [
    {
      label: '创建Coze插件',
      content: '在Coze平台创建新的API插件，选择"自定义API"类型。',
    },
    {
      label: '配置API Schema',
      content: '将上面的OpenAPI Schema配置到插件中，设置正确的服务器地址。',
    },
    {
      label: '测试插件功能',
      content: '在Coze平台测试插件，确保API调用正常工作。',
    },
    {
      label: '发布并使用',
      content: '发布插件后，在Bot中添加该插件即可使用图片处理功能。',
    },
  ];

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        <SmartToyIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
        扣子（Coze）接入
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          Coze是字节跳动推出的AI Bot开发平台。通过创建自定义插件，
          您可以在Coze Bot中集成本图片处理功能，为用户提供智能图片处理服务。
        </Typography>
      </Alert>

      {/* 功能特性 */}
      <Typography variant="subtitle1" gutterBottom sx={{ mt: 3 }}>
        集成优势
      </Typography>
      <List dense>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="无缝集成到Coze Bot"
            secondary="用户可以通过对话直接处理图片"
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="支持多种输入方式"
            secondary="文件上传、URL链接、图片消息等"
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="success" />
          </ListItemIcon>
          <ListItemText 
            primary="智能参数识别"
            secondary="Bot可以根据用户描述自动设置处理参数"
          />
        </ListItem>
      </List>

      <Divider sx={{ my: 3 }} />

      {/* 接入步骤 */}
      <Typography variant="subtitle1" gutterBottom>
        接入步骤
      </Typography>
      <Stepper orientation="vertical">
        {steps.map((step, index) => (
          <Step key={index} active={true}>
            <StepLabel>{step.label}</StepLabel>
            <StepContent>
              <Typography variant="body2" color="text.secondary">
                {step.content}
              </Typography>
            </StepContent>
          </Step>
        ))}
      </Stepper>

      <Divider sx={{ my: 3 }} />

      {/* API Schema配置 */}
      <Typography variant="subtitle1" gutterBottom>
        OpenAPI Schema配置
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        在Coze插件配置中使用以下OpenAPI Schema：
      </Typography>
      <CodeBlock
        code={cozeApiSchema}
        language="json"
        title="coze-plugin-schema.json"
      />

      <Divider sx={{ my: 3 }} />

      {/* 使用示例 */}
      <Typography variant="subtitle1" gutterBottom>
        Bot对话示例
      </Typography>
      <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
        <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
{`用户: 帮我处理一下这张图片 [发送图片]
Bot: 我来帮您处理这张图片。请问您需要什么样的处理效果？

用户: ${endpoint.description}
Bot: 好的，我来为您进行${endpoint.description}处理。

[调用插件: ${cozePluginConfig.name}]
[处理中...]

Bot: 处理完成！这是处理后的图片：[返回处理后的图片]
您还需要其他处理吗？`}
        </Typography>
      </Paper>

      <Divider sx={{ my: 3 }} />

      {/* 相关链接 */}
      <Typography variant="subtitle1" gutterBottom>
        相关资源
      </Typography>
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip
          label="Coze官网"
          component={Link}
          href="https://www.coze.cn/"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
        <Chip
          label="插件开发文档"
          component={Link}
          href="https://www.coze.cn/docs/developer_guides/custom_connector"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
        <Chip
          label="API插件教程"
          component={Link}
          href="https://www.coze.cn/docs/developer_guides/api_plugin"
          target="_blank"
          clickable
          color="primary"
          variant="outlined"
        />
      </Box>
    </Box>
  );
};
