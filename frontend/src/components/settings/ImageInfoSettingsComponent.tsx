import React, { useEffect } from 'react';
import { Box, Typography, Alert } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

interface ImageInfoSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const ImageInfoSettingsComponent: React.FC<ImageInfoSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  useEffect(() => {
    // 图片信息查询不需要参数，传递空对象
    onSettingsChange({});
  }, [onSettingsChange]);

  return (
    <Box>
      <Alert severity="info" icon={<InfoIcon />} sx={{ mb: 3 }}>
        <Typography variant="body2">
          上传图片即可获取详细信息，无需额外设置参数
        </Typography>
      </Alert>

      <Box sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 1, border: 1, borderColor: 'divider' }}>
        <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
          📊 可获取的信息
        </Typography>
        <Box component="ul" sx={{ mt: 1, pl: 2, '& li': { mb: 0.5 } }}>
          <li>
            <Typography variant="body2">图片格式（JPEG、PNG、GIF等）</Typography>
          </li>
          <li>
            <Typography variant="body2">图片尺寸（宽度 × 高度）</Typography>
          </li>
          <li>
            <Typography variant="body2">文件大小（字节及格式化显示）</Typography>
          </li>
          <li>
            <Typography variant="body2">颜色模式（RGB、RGBA等）</Typography>
          </li>
          <li>
            <Typography variant="body2">DPI信息（如果有）</Typography>
          </li>
          <li>
            <Typography variant="body2">是否包含透明通道</Typography>
          </li>
          <li>
            <Typography variant="body2">GIF动画信息（帧数、持续时间等）</Typography>
          </li>
          <li>
            <Typography variant="body2">宽高比、百万像素等</Typography>
          </li>
        </Box>
      </Box>

      <Box sx={{ mt: 3, p: 2, bgcolor: 'success.lighter', borderRadius: 1, border: 1, borderColor: 'success.main' }}>
        <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600, color: 'success.dark' }}>
          💰 计费说明
        </Typography>
        <Typography variant="body2" color="text.secondary">
          每次查询仅需 <strong>10 Token</strong>，快速获取图片完整信息
        </Typography>
      </Box>
    </Box>
  );
};

export default ImageInfoSettingsComponent;
