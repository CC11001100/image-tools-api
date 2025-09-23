import React, { useState } from 'react';
import { Box, IconButton, Tooltip, Typography } from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';

interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
  maxHeight?: string;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language = 'text',
  title,
  maxHeight = '400px'
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('复制失败:', err);
    }
  };

  return (
    <Box sx={{ position: 'relative', mb: 2 }}>
      {title && (
        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
          {title}
        </Typography>
      )}
      
      <Box
        sx={{
          position: 'relative',
          backgroundColor: '#f5f5f5',
          border: '1px solid #e0e0e0',
          borderRadius: 1,
          overflow: 'hidden',
        }}
      >
        {/* 复制按钮 */}
        <Box
          sx={{
            position: 'absolute',
            top: 8,
            right: 8,
            zIndex: 1,
          }}
        >
          <Tooltip title={copied ? '已复制!' : '复制代码'}>
            <IconButton
              size="small"
              onClick={handleCopy}
              sx={{
                backgroundColor: 'rgba(255, 255, 255, 0.8)',
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                },
              }}
            >
              {copied ? (
                <CheckIcon fontSize="small" color="success" />
              ) : (
                <ContentCopyIcon fontSize="small" />
              )}
            </IconButton>
          </Tooltip>
        </Box>

        {/* 代码内容 */}
        <Box
          component="pre"
          sx={{
            margin: 0,
            padding: 2,
            paddingRight: 6, // 为复制按钮留出空间
            fontSize: '0.875rem',
            fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace',
            lineHeight: 1.5,
            overflow: 'auto',
            maxHeight,
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
          }}
        >
          <code>{code}</code>
        </Box>
      </Box>
    </Box>
  );
};
