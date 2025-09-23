import React, { useState, useCallback } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Paper,
  Chip,
  Fade,
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Link as LinkIcon,
  Image as ImageIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import {
  TabPanel,
  FileUploadTab,
  UrlInputTab,
  SampleImagesSection,
  ImagePreview,
  StatusAlerts
} from './ImageInput/index';
import { sampleImageCategories, type SampleImageUrl } from '../config/sampleImageUrls';

interface ImageInputProps {
  onImageSelect: (file: File | null, imageUrl: string | null) => void;
  label?: string;
  // 用于外部控制的props
  forceTabValue?: number;
  forceImageUrl?: string;
  onTabChange?: (tabValue: number) => void;
}

export const ImageInput: React.FC<ImageInputProps> = ({ 
  onImageSelect, 
  label = "选择图片",
  forceTabValue,
  forceImageUrl,
  onTabChange
}) => {
  const [tabValue, setTabValue] = useState(forceTabValue ?? 0);
  const [imageUrl, setImageUrl] = useState('');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showSampleUrls, setShowSampleUrls] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(sampleImageCategories[0]);

  const clearAll = useCallback(() => {
    setPreviewUrl(null);
    setImageUrl('');
    setSelectedFile(null);
    setError(null);
    setSuccess(false);
    setLoading(false);
    onImageSelect(null, null);
  }, [onImageSelect]);

  // 外部控制逻辑
  React.useEffect(() => {
    if (forceTabValue !== undefined && forceTabValue !== tabValue) {
      setTabValue(forceTabValue);
      clearAll();
    }
  }, [forceTabValue, tabValue, clearAll]);

  React.useEffect(() => {
    if (forceImageUrl && forceImageUrl !== imageUrl) {
      setImageUrl(forceImageUrl);
      setError(null);
      setSuccess(false);
      
      const img = new Image();
      img.onload = () => {
        setPreviewUrl(forceImageUrl);
        setSuccess(true);
        onImageSelect(null, forceImageUrl);
      };
      img.onerror = () => {
        setError('无法加载图片，请检查URL是否正确');
        setPreviewUrl(null);
      };
      img.src = forceImageUrl;
    }
  }, [forceImageUrl, imageUrl, onImageSelect]);

  const handleFileSelect = useCallback((file: File) => {
    setError(null);
    setSuccess(false);
    setSelectedFile(file);

    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
      setSuccess(true);
      onImageSelect(file, null);
    };
    reader.onerror = () => {
      setError('文件读取失败，请重试');
    };
    reader.readAsDataURL(file);
  }, [onImageSelect]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    clearAll();
    onTabChange?.(newValue);
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setImageUrl(e.target.value);
    setError(null);
    setSuccess(false);
  };

  const handleUrlSubmit = async () => {
    if (!imageUrl.trim()) {
      setError('请输入图片URL');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // 简单的URL格式验证
      new URL(imageUrl);
    } catch {
      setError('请输入有效的URL地址');
      setLoading(false);
      return;
    }

    // 检查是否为图片URL
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'];
    const urlLower = imageUrl.toLowerCase();
    const hasImageExtension = imageExtensions.some(ext => urlLower.includes(ext));
    
    if (!hasImageExtension) {
      setError('URL似乎不是图片文件，请确认链接指向图片');
      setLoading(false);
      return;
    }

    // 尝试加载图片
    try {
      const img = new Image();
      img.onload = () => {
        setPreviewUrl(imageUrl);
        setSuccess(true);
        setLoading(false);
        onImageSelect(null, imageUrl);
      };
      img.onerror = () => {
        setError('无法加载图片，请检查URL是否正确或图片是否存在');
        setLoading(false);
        setPreviewUrl(null);
      };
      img.src = imageUrl;
    } catch (error) {
      setError('加载图片时发生错误');
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleUrlSubmit();
    }
  };

  const handleSampleUrlSelect = (sampleUrl: SampleImageUrl) => {
    setImageUrl(sampleUrl.url);
    setShowSampleUrls(false);
    setError(null);
    setSuccess(false);
    setLoading(true);

    const img = new Image();
    img.onload = () => {
      setPreviewUrl(sampleUrl.url);
      setSuccess(true);
      setLoading(false);
      onImageSelect(null, sampleUrl.url);
    };
    img.onerror = () => {
      setError('示例图片加载失败');
      setLoading(false);
    };
    img.src = sampleUrl.url;
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
  };

  return (
    <Box>
      <Paper elevation={2} sx={{ borderRadius: 2 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab 
            icon={<CloudUploadIcon />} 
            label="上传文件" 
            iconPosition="start"
            sx={{ textTransform: 'none' }}
          />
          <Tab 
            icon={<LinkIcon />} 
            label="使用URL" 
            iconPosition="start"
            sx={{ textTransform: 'none' }}
          />
        </Tabs>

        {/* 文件上传标签页 */}
        <TabPanel value={tabValue} index={0}>
          <FileUploadTab onFileSelect={handleFileSelect} />
          
          {selectedFile && (
            <Fade in={true}>
              <Box sx={{ mt: 2, px: 3, pb: 3 }}>
                <Chip
                  icon={<ImageIcon />}
                  label={`${selectedFile.name} (${(selectedFile.size / 1024 / 1024).toFixed(2)} MB)`}
                  color="primary"
                  variant="outlined"
                  onDelete={clearAll}
                  deleteIcon={<CloseIcon />}
                />
              </Box>
            </Fade>
          )}
        </TabPanel>

        {/* URL输入标签页 */}
        <TabPanel value={tabValue} index={1}>
          <UrlInputTab
            imageUrl={imageUrl}
            loading={loading}
            onUrlChange={handleUrlChange}
            onUrlSubmit={handleUrlSubmit}
            onKeyPress={handleKeyPress}
            setImageUrl={setImageUrl}
            setError={setError}
          />

          <Box sx={{ px: 3, pb: 3 }}>
            <SampleImagesSection
              showSampleUrls={showSampleUrls}
              selectedCategory={selectedCategory}
              onToggleSampleUrls={() => setShowSampleUrls(!showSampleUrls)}
              onCategoryChange={handleCategoryChange}
              onSampleUrlSelect={handleSampleUrlSelect}
            />
          </Box>
        </TabPanel>
      </Paper>

      {/* 状态提示 */}
      <StatusAlerts
        error={error}
        success={success}
        onClearError={() => setError(null)}
      />

      {/* 图片预览 */}
      <ImagePreview
        previewUrl={previewUrl}
        onClear={clearAll}
      />
    </Box>
  );
};
