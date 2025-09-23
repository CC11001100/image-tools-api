import React from 'react';
import {
  Typography,
  Box,
  Button,
  Paper,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DescriptionIcon from '@mui/icons-material/Description';
import { ImageInput } from './ImageInput';
import { useImageProcessing } from '../hooks/useImageProcessing';
import { TransformApiDocumentation } from './documentation/TransformApiDocumentation';
import { DEFAULT_SAMPLE_IMAGE, API_BASE_URL } from '../config/constants';
import { ClickableImage } from './ClickableImage';

interface UniversalTransformPageProps {
  title: string;
  description: string;
}

export const UniversalTransformPage: React.FC<UniversalTransformPageProps> = ({
  title,
  description,
}) => {
  const {
    selectedFile,
    selectedImageUrl,
    previewUrl,
    resultImage,
    isLoading,
    error,
    handleImageSelect,
    handleUseDefaultImage,
    setResultImage,
    setError,
    setIsLoading,
  } = useImageProcessing();

  const [settings, setSettings] = React.useState<any>({
    transform_type: 'rotate',
    angle: 0,
    expand: true,
    fill_color: '#ffffff',
    quality: 90,
  });

  const getApiPath = (transformType: string, isUrl: boolean) => {
    const basePath = transformType === 'rotate' 
      ? '/transform/rotate' 
      : `/transform/${transformType}`;
    return isUrl ? `${basePath}-url` : basePath;
  };

  const handleProcess = async () => {
    if (!selectedFile && !selectedImageUrl && !previewUrl) {
      setError('请先选择图片或使用示例图片');
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      const isUrl = !selectedFile;
      const apiPath = getApiPath(settings.transform_type, isUrl);

      if (selectedFile) {
        formData.append('file', selectedFile);
      } else {
        formData.append('image_url', selectedImageUrl || previewUrl || DEFAULT_SAMPLE_IMAGE);
      }

      // 添加参数
      formData.append('quality', settings.quality.toString());
      
      if (settings.transform_type === 'rotate') {
        formData.append('angle', settings.angle.toString());
        formData.append('expand', settings.expand.toString());
        formData.append('fill_color', settings.fill_color);
      }

      const response = await fetch(`${API_BASE_URL}${apiPath}`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setResultImage(url);
      } else {
        const errorText = await response.text();
        setError(`处理失败: ${errorText}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setError('网络错误或服务器异常');
    } finally {
      setIsLoading(false);
    }
  };

  const updateSettings = (newSettings: any) => {
    setSettings({ ...settings, ...newSettings });
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body1" paragraph>
        {description}
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">选择图片</Typography>
              <Button 
                variant="outlined" 
                size="small"
                onClick={handleUseDefaultImage}
              >
                使用示例图片
              </Button>
            </Box>
            
            <ImageInput onImageSelect={handleImageSelect} />
            
            {previewUrl && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  当前图片预览:
                </Typography>
                <ClickableImage
                  src={previewUrl}
                  alt="当前图片"
                  title="当前图片预览"
                  style={{ 
                    maxWidth: '100%', 
                    height: 'auto', 
                    border: '1px solid #ddd'
                  }}
                  downloadFileName="current-image.jpg"
                />
              </Box>
            )}
          </Paper>

          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              参数设置
            </Typography>
            
            {/* 这里应该有设置组件，暂时使用简单的设置 */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" gutterBottom>
                变换类型: {settings.transform_type}
              </Typography>
              {settings.transform_type === 'rotate' && (
                <Typography variant="body2" gutterBottom>
                  旋转角度: {settings.angle}°
                </Typography>
              )}
            </Box>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Button
              fullWidth
              variant="contained"
              color="primary"
              onClick={handleProcess}
              disabled={isLoading}
              size="large"
            >
              {isLoading ? '处理中...' : '开始处理'}
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          {resultImage && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                处理结果
              </Typography>
              <ClickableImage
                src={resultImage}
                alt="处理后图片"
                title="变换处理结果"
                style={{ 
                  maxWidth: '100%', 
                  height: 'auto', 
                  border: '1px solid #ddd'
                }}
                downloadFileName="transformed-image.jpg"
              />
              <Button 
                fullWidth
                variant="outlined" 
                color="primary" 
                sx={{ mt: 2 }}
                href={resultImage}
                download="processed-image.jpg"
              >
                下载图片
              </Button>
            </Paper>
          )}

          <Paper sx={{ p: 3 }}>
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">
                  <DescriptionIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
                  API 文档
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <TransformApiDocumentation settings={settings} />
              </AccordionDetails>
            </Accordion>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}; 