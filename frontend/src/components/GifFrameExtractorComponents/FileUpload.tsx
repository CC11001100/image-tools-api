/**
 * 文件上传组件
 */

import React, { useCallback } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
} from '@mui/icons-material';

import { FileUploadProps } from './types';

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  fileInputRef,
}) => {
  // 拖拽处理
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onFileSelect(files[0]);
    }
  }, [onFileSelect]);

  // 文件输入处理
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onFileSelect(files[0]);
    }
  }, [onFileSelect]);

  return (
    <Paper
      sx={{
        p: 4,
        textAlign: 'center',
        border: '2px dashed #ccc',
        cursor: 'pointer',
        '&:hover': {
          borderColor: 'primary.main',
          backgroundColor: 'rgba(25, 118, 210, 0.05)',
        },
      }}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept=".gif,image/gif"
        onChange={handleInputChange}
        style={{ display: 'none' }}
      />
      
      <UploadIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
      
      <Typography variant="h5" gutterBottom>
        上传GIF文件
      </Typography>
      
      <Typography variant="body1" color="text.secondary" paragraph>
        拖拽GIF文件到此处或点击选择文件
      </Typography>
      
      <Typography variant="body2" color="text.secondary">
        支持最大50MB的GIF文件
      </Typography>
      
      <Button
        variant="contained"
        startIcon={<UploadIcon />}
        sx={{ mt: 2 }}
        onClick={(e) => {
          e.stopPropagation();
          fileInputRef.current?.click();
        }}
      >
        选择GIF文件
      </Button>
    </Paper>
  );
};

export default FileUpload;
