import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Alert,
  Paper,
  CircularProgress,
  Grid,
  Chip,
} from '@mui/material';
import {
  Gif as GifIcon,
  Download as DownloadIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
} from '@mui/icons-material';
import MultiImageUpload from '../components/MultiImageUpload';
import GifCreationSettings from '../components/settings/GifCreationSettings';
import { useNotification } from '../hooks/useNotification';

const ImageToGifPage: React.FC = () => {
  const [images, setImages] = useState<File[]>([]);
  const [settings, setSettings] = useState<any>({});
  const [isLoading, setIsLoading] = useState(false);
  const [resultGif, setResultGif] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const { showNotification } = useNotification();

  const handleCreateGif = async () => {
    if (images.length < 2) {
      showNotification('请至少选择2张图片', 'warning');
      return;
    }

    setIsLoading(true);
    try {
      const formData = new FormData();
      
      // 添加所有图片文件
      images.forEach((image, index) => {
        formData.append('files', image);
      });
      
      // 添加参数
      formData.append('duration', settings.duration?.toString() || '500');
      formData.append('loop', settings.loop?.toString() || '0');
      formData.append('optimize', settings.optimize?.toString() || 'true');

      const response = await fetch('/api/gif/create', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const gifBlob = await response.blob();
      const gifUrl = URL.createObjectURL(gifBlob);
      setResultGif(gifUrl);
      setIsPlaying(true);
      
      showNotification('GIF创建成功！', 'success');
    } catch (error) {
      console.error('创建GIF失败:', error);
      showNotification(error instanceof Error ? error.message : '创建GIF失败', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!resultGif) return;
    
    const link = document.createElement('a');
    link.href = resultGif;
    link.download = `animated_${Date.now()}.gif`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('GIF下载开始', 'info');
  };

  const handleReset = () => {
    setImages([]);
    setResultGif(null);
    setIsPlaying(true);
  };

  const togglePlayback = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* 页面标题 */}
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mb: 2 }}>
          <GifIcon sx={{ fontSize: 48, color: 'primary.main', mr: 2 }} />
          <Typography variant="h3" component="h1">
            图片合成GIF
          </Typography>
        </Box>
        <Typography variant="h6" color="text.secondary" paragraph>
          上传多张图片，一键生成动态GIF图片
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, flexWrap: 'wrap' }}>
          <Chip label="支持拖拽排序" size="small" variant="outlined" />
          <Chip label="自定义帧率" size="small" variant="outlined" />
          <Chip label="循环控制" size="small" variant="outlined" />
          <Chip label="文件优化" size="small" variant="outlined" />
        </Box>
      </Box>

      <Grid container spacing={4}>
        {/* 左侧：图片上传 */}
        <Grid item xs={12} lg={8}>
          <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              1. 选择图片
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              上传至少2张图片，支持拖拽排序来调整播放顺序
            </Typography>
            <MultiImageUpload
              images={images}
              onImagesChange={setImages}
              maxImages={50}
              maxFileSize={20}
            />
          </Paper>

          {/* 结果预览 */}
          {resultGif && (
            <Paper elevation={2} sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h5">
                  3. 生成结果
                </Typography>
                <Box>
                  <Button
                    variant="outlined"
                    startIcon={isPlaying ? <StopIcon /> : <PlayIcon />}
                    onClick={togglePlayback}
                    sx={{ mr: 1 }}
                  >
                    {isPlaying ? '暂停' : '播放'}
                  </Button>
                  <Button
                    variant="contained"
                    startIcon={<DownloadIcon />}
                    onClick={handleDownload}
                  >
                    下载GIF
                  </Button>
                </Box>
              </Box>
              
              <Box sx={{ textAlign: 'center', bgcolor: 'grey.100', p: 2, borderRadius: 1 }}>
                <img
                  src={resultGif}
                  alt="Generated GIF"
                  style={{
                    maxWidth: '100%',
                    maxHeight: '400px',
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
            </Paper>
          )}
        </Grid>

        {/* 右侧：参数设置 */}
        <Grid item xs={12} lg={4}>
          <Box sx={{ mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              2. 参数设置
            </Typography>
            <GifCreationSettings
              onSettingsChange={setSettings}
              isLoading={isLoading}
              imageCount={images.length}
            />
          </Box>

          {/* 操作按钮 */}
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              操作
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Button
                variant="contained"
                size="large"
                startIcon={isLoading ? <CircularProgress size={20} /> : <GifIcon />}
                onClick={handleCreateGif}
                disabled={isLoading || images.length < 2}
                fullWidth
              >
                {isLoading ? '正在生成...' : '生成GIF'}
              </Button>
              
              <Button
                variant="outlined"
                onClick={handleReset}
                disabled={isLoading}
                fullWidth
              >
                重新开始
              </Button>
            </Box>

            {/* 状态提示 */}
            {images.length === 0 && (
              <Alert severity="info" sx={{ mt: 2 }}>
                请先上传图片文件
              </Alert>
            )}
            
            {images.length === 1 && (
              <Alert severity="warning" sx={{ mt: 2 }}>
                请至少上传2张图片
              </Alert>
            )}
            
            {images.length >= 2 && !isLoading && (
              <Alert severity="success" sx={{ mt: 2 }}>
                准备就绪，可以生成GIF了！
              </Alert>
            )}
          </Paper>

          {/* 使用说明 */}
          <Paper elevation={1} sx={{ p: 2, mt: 3, bgcolor: 'grey.50' }}>
            <Typography variant="subtitle2" gutterBottom>
              使用说明
            </Typography>
            <Typography variant="body2" color="text.secondary">
              1. 支持JPEG、PNG、GIF、WebP格式
              <br />
              2. 图片会自动调整为相同尺寸
              <br />
              3. 可通过拖拽调整播放顺序
              <br />
              4. 帧率越高文件越大
              <br />
              5. 启用优化可减少文件大小
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ImageToGifPage; 