import React, { useState } from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  Button,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  Chip,
  Tab,
  Tabs,
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { ApiEndpoint } from '../../types/api';
import ImageUpload from '../ImageUpload';
import { ApiIntegrationTabs } from '../ApiIntegrationTabs';
import { imageInfoExamples } from '../../config/examples/imageInfoExamples';

interface ImageInfoLayoutProps {
  title: string;
  description: string;
  endpoint: ApiEndpoint;
}

interface ImageInfo {
  format: string;
  width: number;
  height: number;
  mode: string;
  size_bytes: number;
  size_formatted: string;
  dpi: [number, number] | null;
  has_alpha: boolean;
  color_space: string;
  frame_count?: number;
  is_animated?: boolean;
  duration?: number;
  loop?: number;
  aspect_ratio: number;
  megapixels: number;
  exif?: any;
  icc_profile?: any;
}

interface BillingInfo {
  base_cost: number;
  total_cost: number;
  call_id: string;
  tokens_consumed: number;
}

export const ImageInfoLayout: React.FC<ImageInfoLayoutProps> = ({
  title,
  description,
  endpoint,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string>('');
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [imageInfo, setImageInfo] = useState<ImageInfo | null>(null);
  const [billingInfo, setBillingInfo] = useState<BillingInfo | null>(null);
  const [inputMode, setInputMode] = useState<'file' | 'url'>('file');

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError('');
    setImageInfo(null);
    setBillingInfo(null);
    
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleUrlChange = (url: string) => {
    setImageUrl(url);
    setPreviewUrl(url);
    setError('');
    setImageInfo(null);
    setBillingInfo(null);
  };

  const handleExampleClick = (exampleImageUrl: string) => {
    setInputMode('url');
    setImageUrl(exampleImageUrl);
    setPreviewUrl(exampleImageUrl);
    setError('');
    setImageInfo(null);
    setBillingInfo(null);
  };

  const handleSubmit = async () => {
    if (!selectedFile && !imageUrl) {
      setError('请选择图片或输入图片URL');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      
      let apiUrl = '';
      if (inputMode === 'file' && selectedFile) {
        formData.append('file', selectedFile);
        apiUrl = 'http://localhost:58888/api/v1/image-info';
      } else if (inputMode === 'url' && imageUrl) {
        apiUrl = 'http://localhost:58888/api/v1/image-info-by-url';
        // URL模式使用JSON格式
      }

      const isUrlMode = inputMode === 'url' && imageUrl;
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: isUrlMode ? {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer aigc-hub-fb54649282924869b1b8f4df9afac833',
        } : {
          'Authorization': 'Bearer aigc-hub-fb54649282924869b1b8f4df9afac833',
        },
        body: isUrlMode ? JSON.stringify({ image_url: imageUrl }) : formData,
      });

      const result = await response.json();

      if (result.code === 200 && result.data) {
        setImageInfo(result.data.image_info);
        setBillingInfo(result.data.billing_info);
      } else {
        setError(result.message || '获取图片信息失败');
      }
    } catch (err) {
      setError('请求失败: ' + (err instanceof Error ? err.message : '未知错误'));
    } finally {
      setLoading(false);
    }
  };

  const renderInfoField = (label: string, value: any) => {
    if (value === null || value === undefined) {
      return null;
    }

    let displayValue = value;
    if (typeof value === 'boolean') {
      displayValue = value ? '是' : '否';
    } else if (Array.isArray(value)) {
      displayValue = value.join(' × ');
    } else if (typeof value === 'object') {
      displayValue = JSON.stringify(value, null, 2);
    }

    return (
      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {label}
        </Typography>
        <Typography variant="body1" sx={{ fontWeight: 500 }}>
          {displayValue}
        </Typography>
      </Box>
    );
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
          {title}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {description}
        </Typography>
      </Box>

      <ApiIntegrationTabs endpoint={endpoint} />

      <Box sx={{ mt: 4 }}>
        {/* 示例展示 */}
        <Paper elevation={0} sx={{ p: 3, mb: 4, backgroundColor: '#f5f5f5' }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <InfoIcon color="primary" />
            效果示例
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            点击示例图片快速测试
          </Typography>
          
          <Grid container spacing={2}>
            {imageInfoExamples.map((example, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card 
                  sx={{ 
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 3,
                    }
                  }}
                  onClick={() => handleExampleClick(example.originalImage)}
                >
                  <Box
                    component="img"
                    src={example.originalImage}
                    alt={example.title}
                    sx={{
                      width: '100%',
                      height: 150,
                      objectFit: 'cover',
                    }}
                  />
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>
                      {example.title}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {example.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>

        {/* 输入区域 */}
        <Paper elevation={1} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            上传图片
          </Typography>
          
          <Tabs 
            value={inputMode} 
            onChange={(_, value) => setInputMode(value)}
            sx={{ mb: 3 }}
          >
            <Tab icon={<UploadFileIcon />} label="上传文件" value="file" />
            <Tab icon={<InfoIcon />} label="使用URL" value="url" />
          </Tabs>

          {inputMode === 'file' ? (
            <ImageUpload
              onImageSelected={handleFileSelect}
              isLoading={loading}
            />
          ) : (
            <Box>
              <input
                type="text"
                placeholder="输入图片URL"
                value={imageUrl}
                onChange={(e) => handleUrlChange(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  fontSize: '16px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                }}
              />
            </Box>
          )}

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}

          <Button
            variant="contained"
            size="large"
            onClick={handleSubmit}
            disabled={loading || (!selectedFile && !imageUrl)}
            sx={{ mt: 3 }}
          >
            {loading ? <CircularProgress size={24} /> : '查询图片信息'}
          </Button>
        </Paper>

        {/* 结果展示 */}
        {(previewUrl || imageInfo) && (
          <Grid container spacing={3}>
            {/* 左侧：输入图片 */}
            {previewUrl && (
              <Grid item xs={12} md={6}>
                <Paper elevation={1} sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    输入图片
                  </Typography>
                  <Box
                    component="img"
                    src={previewUrl}
                    alt="Preview"
                    sx={{
                      width: '100%',
                      maxHeight: 400,
                      objectFit: 'contain',
                      borderRadius: 1,
                      backgroundColor: '#f5f5f5',
                    }}
                  />
                </Paper>
              </Grid>
            )}

            {/* 右侧：JSON结果 */}
            {imageInfo && (
              <Grid item xs={12} md={6}>
                <Paper elevation={1} sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <InfoIcon color="primary" />
                    图片信息
                  </Typography>
                  
                  <Divider sx={{ mb: 2 }} />

                  {/* 基础信息 */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      基础信息
                    </Typography>
                    {renderInfoField('格式', imageInfo.format)}
                    {renderInfoField('尺寸', `${imageInfo.width} × ${imageInfo.height}`)}
                    {renderInfoField('文件大小', imageInfo.size_formatted)}
                    {renderInfoField('颜色模式', imageInfo.mode)}
                    {renderInfoField('色彩空间', imageInfo.color_space)}
                    {renderInfoField('宽高比', imageInfo.aspect_ratio.toFixed(2))}
                    {renderInfoField('百万像素', imageInfo.megapixels.toFixed(2))}
                  </Box>

                  {/* 高级信息 */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      高级信息
                    </Typography>
                    {renderInfoField('透明通道', imageInfo.has_alpha)}
                    {imageInfo.dpi && renderInfoField('DPI', imageInfo.dpi)}
                  </Box>

                  {/* GIF动画信息 */}
                  {imageInfo.is_animated && (
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        动画信息
                      </Typography>
                      {renderInfoField('帧数', imageInfo.frame_count)}
                      {renderInfoField('动画', imageInfo.is_animated)}
                      {renderInfoField('持续时间', imageInfo.duration ? `${imageInfo.duration}ms` : null)}
                      {renderInfoField('循环', imageInfo.loop === 0 ? '无限循环' : `${imageInfo.loop}次`)}
                    </Box>
                  )}

                  {/* 计费信息 */}
                  {billingInfo && (
                    <Box>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        计费信息
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        <Chip 
                          label={`消费: ${billingInfo.tokens_consumed} Token`} 
                          color="primary" 
                          size="small" 
                        />
                        <Chip 
                          label={`调用ID: ${billingInfo.call_id.substring(0, 8)}...`} 
                          size="small" 
                          variant="outlined"
                        />
                      </Box>
                    </Box>
                  )}

                  {/* 原始JSON */}
                  <Box sx={{ mt: 3 }}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      完整JSON
                    </Typography>
                    <Paper 
                      elevation={0} 
                      sx={{ 
                        p: 2, 
                        backgroundColor: '#f5f5f5',
                        maxHeight: 300,
                        overflow: 'auto',
                      }}
                    >
                      <pre style={{ margin: 0, fontSize: '12px', lineHeight: 1.5 }}>
                        {JSON.stringify(imageInfo, null, 2)}
                      </pre>
                    </Paper>
                  </Box>
                </Paper>
              </Grid>
            )}
          </Grid>
        )}
      </Box>
    </Box>
  );
};
