import React from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Chip,
} from '@mui/material';
import {
  PhotoLibrary as PhotoLibraryIcon,
} from '@mui/icons-material';
import GifFrameExtractor from '../components/GifFrameExtractor';

const GifExtractPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* 页面标题 */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mb: 2 }}>
          <PhotoLibraryIcon sx={{ fontSize: 48, color: 'primary.main', mr: 2 }} />
          <Typography variant="h3" component="h1">
            GIF拆图工具
          </Typography>
        </Box>
        <Typography variant="h6" color="text.secondary" paragraph>
          将GIF动图按帧拆分成单独的图片文件
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, flexWrap: 'wrap' }}>
          <Chip label="选择性提取" size="small" variant="outlined" />
          <Chip label="批量下载" size="small" variant="outlined" />
          <Chip label="高质量输出" size="small" variant="outlined" />
          <Chip label="支持大文件" size="small" variant="outlined" />
        </Box>
      </Box>

      {/* 功能介绍 */}
      <Paper elevation={1} sx={{ p: 3, mb: 4, bgcolor: 'background.paper' }}>
        <Typography variant="h6" gutterBottom>
          功能特点
        </Typography>
        <Typography variant="body1" paragraph>
          我们的GIF拆图工具让您轻松地将动态GIF文件分解为单独的静态图片。您可以选择提取所有帧或仅提取需要的特定帧。
        </Typography>
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2 }}>
          <Box>
            <Typography variant="subtitle2" color="primary.main" gutterBottom>
              ✨ 智能提取
            </Typography>
            <Typography variant="body2" color="text.secondary">
              自动识别GIF中的所有帧，提供可视化的帧选择界面
            </Typography>
          </Box>
          <Box>
            <Typography variant="subtitle2" color="primary.main" gutterBottom>
              📦 灵活下载
            </Typography>
            <Typography variant="body2" color="text.secondary">
              单帧下载PNG文件，多帧自动打包为ZIP文件
            </Typography>
          </Box>
          <Box>
            <Typography variant="subtitle2" color="primary.main" gutterBottom>
              🎯 精确控制
            </Typography>
            <Typography variant="body2" color="text.secondary">
              可以选择提取特定帧或全部帧，满足不同需求
            </Typography>
          </Box>
          <Box>
            <Typography variant="subtitle2" color="primary.main" gutterBottom>
              💎 高品质输出
            </Typography>
            <Typography variant="body2" color="text.secondary">
              保持原始图片质量，输出标准PNG格式图片
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* 主要功能组件 */}
      <GifFrameExtractor />

      {/* 使用说明 */}
      <Paper elevation={1} sx={{ p: 3, mt: 4, bgcolor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          使用说明
        </Typography>
        <Box component="ol" sx={{ pl: 2 }}>
          <Typography component="li" variant="body2" paragraph>
            上传您的GIF文件（支持拖拽或点击选择）
          </Typography>
          <Typography component="li" variant="body2" paragraph>
            预览GIF内容，查看文件信息和预估帧数
          </Typography>
          <Typography component="li" variant="body2" paragraph>
            在帧选择器中选择要提取的帧（可以单选、多选或全选）
          </Typography>
          <Typography component="li" variant="body2" paragraph>
            点击提取按钮，系统将自动处理并开始下载
          </Typography>
          <Typography component="li" variant="body2" paragraph>
            如果选择多帧，将下载ZIP压缩包；单帧直接下载PNG文件
          </Typography>
        </Box>
        
        <Typography variant="subtitle2" sx={{ mt: 2, color: 'warning.main' }}>
          注意事项：
        </Typography>
        <Typography variant="body2" color="text.secondary">
          • 支持最大50MB的GIF文件
          <br />
          • 建议选择相对较小的GIF文件以获得更好的处理速度
          <br />
          • 提取的PNG文件将保持原始GIF的分辨率
          <br />
          • 文件名格式：单帧为"frame_X.png"，多帧为"gif_frames.zip"
        </Typography>
      </Paper>
    </Container>
  );
};

export default GifExtractPage; 