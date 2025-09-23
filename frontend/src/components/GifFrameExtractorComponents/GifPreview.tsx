/**
 * GIF预览组件
 */

import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
} from '@mui/icons-material';

import { GifPreviewProps } from './types';

const GifPreview: React.FC<GifPreviewProps> = ({
  gifFile,
  gifPreviewUrl,
  frames,
  isPlaying,
  setIsPlaying,
  onReset,
}) => {
  return (
    <Paper sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">
          GIF预览
        </Typography>
        <Box>
          <Tooltip title={isPlaying ? '暂停' : '播放'}>
            <IconButton
              onClick={() => setIsPlaying(!isPlaying)}
              size="small"
            >
              {isPlaying ? <PauseIcon /> : <PlayIcon />}
            </IconButton>
          </Tooltip>
          <Button
            variant="outlined"
            size="small"
            onClick={onReset}
            sx={{ ml: 1 }}
          >
            重新选择
          </Button>
        </Box>
      </Box>
      
      <Box sx={{ textAlign: 'center', bgcolor: 'grey.100', p: 2, borderRadius: 1 }}>
        <img
          src={gifPreviewUrl}
          alt="GIF预览"
          style={{
            maxWidth: '100%',
            maxHeight: '300px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            filter: isPlaying ? 'none' : 'brightness(0.7)',
          }}
        />
        {!isPlaying && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            已暂停播放
          </Typography>
        )}
      </Box>
      
      <Box sx={{ mt: 2 }}>
        <Typography variant="body2" color="text.secondary">
          文件名：{gifFile.name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          文件大小：{(gifFile.size / 1024 / 1024).toFixed(2)} MB
        </Typography>
        <Typography variant="body2" color="text.secondary">
          预估帧数：{frames.length}
        </Typography>
      </Box>
    </Paper>
  );
};

export default GifPreview;
