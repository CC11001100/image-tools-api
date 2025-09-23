/**
 * 提取控制组件
 */

import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Chip,
} from '@mui/material';
import {
  Download as DownloadIcon,
  SelectAll as SelectAllIcon,
  ClearAll as ClearAllIcon,
} from '@mui/icons-material';

import { ExtractionControlProps } from './types';

const ExtractionControl: React.FC<ExtractionControlProps> = ({
  selectedFrames,
  frames,
  isExtracting,
  onSelectAll,
  onClearSelection,
  onExtractFrames,
}) => {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        提取设置
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
        <Chip 
          label={`已选择 ${selectedFrames.size} 帧`} 
          color={selectedFrames.size > 0 ? 'primary' : 'default'}
          variant="outlined"
        />
        <Chip 
          label={`总计 ${frames.length} 帧`} 
          variant="outlined"
        />
      </Box>
      
      <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
        <Button
          variant="outlined"
          startIcon={<SelectAllIcon />}
          onClick={onSelectAll}
          size="small"
        >
          {selectedFrames.size === frames.length ? '取消全选' : '全选'}
        </Button>
        <Button
          variant="outlined"
          startIcon={<ClearAllIcon />}
          onClick={onClearSelection}
          size="small"
          disabled={selectedFrames.size === 0}
        >
          清空选择
        </Button>
      </Box>

      <Button
        variant="contained"
        size="large"
        fullWidth
        startIcon={isExtracting ? <CircularProgress size={20} /> : <DownloadIcon />}
        onClick={onExtractFrames}
        disabled={isExtracting || selectedFrames.size === 0}
      >
        {isExtracting ? '正在提取...' : 
         selectedFrames.size === 1 ? '提取选中帧' : 
         selectedFrames.size > 1 ? `提取${selectedFrames.size}帧` : '选择要提取的帧'}
      </Button>
      
      {selectedFrames.size > 1 && (
        <Alert severity="info" sx={{ mt: 2 }}>
          将提取{selectedFrames.size}帧并打包为ZIP文件下载
        </Alert>
      )}
      
      {selectedFrames.size === 1 && (
        <Alert severity="info" sx={{ mt: 2 }}>
          将提取单帧并下载为PNG文件
        </Alert>
      )}
    </Paper>
  );
};

export default ExtractionControl;
