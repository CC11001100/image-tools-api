import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';

interface FileUploadTabProps {
  onFileSelect: (file: File) => void;
}

export const FileUploadTab: React.FC<FileUploadTabProps> = ({ onFileSelect }) => {
  const onDrop = React.useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp', '.svg']
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  return (
    <Box sx={{ p: 3 }}>
      <Paper
        {...getRootProps()}
        elevation={0}
        sx={{
          border: 2,
          borderStyle: 'dashed',
          borderColor: isDragActive 
            ? 'primary.main' 
            : isDragReject 
              ? 'error.main' 
              : 'grey.300',
          backgroundColor: isDragActive 
            ? 'primary.50' 
            : isDragReject 
              ? 'error.50' 
              : 'grey.50',
          p: 4,
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: 'primary.main',
            backgroundColor: 'primary.50',
          },
        }}
      >
        <input {...getInputProps()} />
        <CloudUploadIcon 
          sx={{ 
            fontSize: 48, 
            color: isDragActive ? 'primary.main' : 'grey.400',
            mb: 2 
          }} 
        />
        
        {isDragActive ? (
          <Typography variant="h6" color="primary">
            松开鼠标上传图片
          </Typography>
        ) : isDragReject ? (
          <Typography variant="h6" color="error">
            不支持的文件类型
          </Typography>
        ) : (
          <>
            <Typography variant="h6" gutterBottom>
              拖拽图片到这里，或点击选择文件
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              支持 JPG、PNG、GIF、BMP、WebP、SVG 格式
            </Typography>
            <Button 
              variant="outlined" 
              size="large"
              startIcon={<CloudUploadIcon />}
            >
              选择文件
            </Button>
          </>
        )}
      </Paper>
    </Box>
  );
};
