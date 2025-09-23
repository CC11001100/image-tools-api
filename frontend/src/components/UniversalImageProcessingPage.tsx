import React from 'react';
import {
  Typography,
  Box,
  Button,
  Paper,
  Grid,
  Alert,
} from '@mui/material';
import { ImageInput } from './ImageInput';
import { useImageProcessing } from '../hooks/useImageProcessing';
import { ApiIntegrationTabs } from './ApiIntegrationTabs';
import { DEFAULT_SAMPLE_IMAGE, API_BASE_URL } from '../config/constants';
import { ClickableImage } from './ClickableImage';

export interface EndpointConfig {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  urlPath: string;
  description: string;
  category: string;
  requestType: {
    file: string;
    url: string;
  };
  responseType: string;
  parameters: Array<{
    name: string;
    type: 'string' | 'number' | 'boolean' | 'select' | 'file';
    description: string;
    required?: boolean;
    defaultValue?: any;
    options?: string[];
    min?: number;
    max?: number;
    step?: number;
  }>;
}

export interface UniversalImageProcessingPageProps {
  title: string;
  description: string;
  endpoint: EndpointConfig;
  settingsComponent?: React.ComponentType<{
    onSettingsChange: (settings: any) => void;
    isLoading: boolean;
  }>;
  defaultSettings?: any;
  showImagePreview?: boolean;
}

export const UniversalImageProcessingPage: React.FC<UniversalImageProcessingPageProps> = ({
  title,
  description,
  endpoint,
  settingsComponent: SettingsComponent,
  defaultSettings = {},
  showImagePreview = true,
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

  const [settings, setSettings] = React.useState(defaultSettings);

  const handleProcess = async () => {
    if (!selectedFile && !selectedImageUrl && !previewUrl) {
      setError('请先选择图片或使用示例图片');
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      let apiPath = endpoint.path;

      if (selectedFile) {
        formData.append('file', selectedFile);
      } else {
        const urlToUse = selectedImageUrl || previewUrl || DEFAULT_SAMPLE_IMAGE;
        formData.append('image_url', urlToUse);
        apiPath = endpoint.urlPath || endpoint.path + '-url';
      }

      Object.entries(settings).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          formData.append(key, value.toString());
        }
      });

      const response = await fetch(`${API_BASE_URL}${apiPath}`, {
        method: endpoint.method,
        body: formData,
      });

      if (response.ok) {
        const contentType = response.headers.get('content-type');
        if (contentType?.includes('image')) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          setResultImage(url);
        } else {
          setError('服务器返回了非图片格式的数据');
        }
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
            
            {showImagePreview && previewUrl && (
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

          {SettingsComponent && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                参数设置
              </Typography>
              <SettingsComponent
                onSettingsChange={setSettings}
                isLoading={isLoading}
              />
            </Paper>
          )}

          <Paper sx={{ p: 3, mb: 3 }}>
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

          {/* 处理结果显示在按钮下方 */}
          {resultImage && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                处理结果
              </Typography>
              <ClickableImage
                src={resultImage}
                alt="处理后图片"
                title="处理结果"
                style={{ 
                  maxWidth: '100%', 
                  height: 'auto', 
                  border: '1px solid #ddd'
                }}
                downloadFileName="processed-image.jpg"
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
        </Grid>

        <Grid item xs={12} md={6}>
          <ApiIntegrationTabs
            endpoint={endpoint}
            settings={settings}
          />
        </Grid>
      </Grid>
    </Box>
  );
}; 