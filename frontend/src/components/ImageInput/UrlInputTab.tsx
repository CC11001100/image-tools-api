import React from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Chip,
  CircularProgress,
} from '@mui/material';
import {
  Link as LinkIcon,
} from '@mui/icons-material';
import { quickTestUrls, generateRandomTestUrl } from '../../config/quickTestUrls';

interface UrlInputTabProps {
  imageUrl: string;
  loading: boolean;
  onUrlChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onUrlSubmit: () => void;
  onKeyPress: (e: React.KeyboardEvent) => void;
  setImageUrl: (url: string) => void;
  setError: (error: string | null) => void;
}

export const UrlInputTab: React.FC<UrlInputTabProps> = ({
  imageUrl,
  loading,
  onUrlChange,
  onUrlSubmit,
  onKeyPress,
  setImageUrl,
  setError,
}) => {
  return (
    <Box sx={{ p: 3 }}>
      <TextField
        fullWidth
        label="图片URL地址"
        placeholder="https://example.com/image.jpg"
        value={imageUrl}
        onChange={onUrlChange}
        onKeyPress={onKeyPress}
        variant="outlined"
        InputProps={{
          endAdornment: (
            <Button
              onClick={onUrlSubmit}
              disabled={loading || !imageUrl.trim()}
              variant="contained"
              sx={{ ml: 1, minWidth: 'auto' }}
            >
              {loading ? <CircularProgress size={20} /> : '加载'}
            </Button>
          ),
        }}
        helperText="支持 JPG、PNG、GIF、BMP、WebP、SVG 格式的图片URL"
      />

      <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip label="JPG" size="small" variant="outlined" />
        <Chip label="PNG" size="small" variant="outlined" />
        <Chip label="GIF" size="small" variant="outlined" />
        <Chip label="WebP" size="small" variant="outlined" />
        <Chip label="SVG" size="small" variant="outlined" />
      </Box>

      {/* 快捷测试链接 */}
      <Box sx={{ mt: 3, p: 2, bgcolor: 'info.50', borderRadius: 1, border: '1px solid', borderColor: 'info.200' }}>
        <Typography variant="subtitle2" color="info.main" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <LinkIcon fontSize="small" />
          快捷测试链接
        </Typography>
        <Typography variant="caption" color="text.secondary" sx={{ mb: 2, display: 'block' }}>
          点击下方按钮快速填入随机图片链接，仅用于测试效果
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {quickTestUrls.map((testUrl, index) => (
            <Button
              key={index}
              size="small"
              variant="outlined"
              color="info"
              onClick={() => {
                const randomUrl = generateRandomTestUrl(testUrl.url);
                setImageUrl(randomUrl);
                setError(null);
              }}
              sx={{ textTransform: 'none' }}
            >
              {testUrl.name}
            </Button>
          ))}
        </Box>
      </Box>
    </Box>
  );
};
