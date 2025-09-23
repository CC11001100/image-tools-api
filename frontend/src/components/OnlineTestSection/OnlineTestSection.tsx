import React from 'react';
import { Box, Button, Paper, Typography, Alert } from '@mui/material';
import { ImageInput } from '../ImageInput';
import { ClickableImage } from '../ClickableImage';

interface OnlineTestSectionProps {
  onImageSelect: (file: File | null, imageUrl: string | null) => void;
  onUseDefaultImage: () => void;
  previewUrl: string | null;
  showImagePreview: boolean;
  settingsComponent?: React.ComponentType<{
    onSettingsChange: (settings: any) => void;
    isLoading: boolean;
    appliedParams?: Record<string, any> | null;
    settings?: Record<string, any>;
    [key: string]: any;
  }>;
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
  onProcess: () => void;
  appliedParams?: Record<string, any> | null;
  processButtonRef?: React.RefObject<HTMLButtonElement>;
  forceTabValue?: number;
  forceImageUrl?: string;
  onTabChange?: (tabValue: number) => void;
  currentSettings?: Record<string, any>;
  // 结果显示相关
  resultImage: string | null;
  downloadFileName: string;
  error: string | null;
}

export const OnlineTestSection: React.FC<OnlineTestSectionProps> = ({
  onImageSelect,
  onUseDefaultImage,
  previewUrl,
  showImagePreview,
  settingsComponent: SettingsComponent,
  onSettingsChange,
  isLoading,
  onProcess,
  appliedParams,
  processButtonRef,
  forceTabValue,
  forceImageUrl,
  onTabChange,
  currentSettings,
  resultImage,
  downloadFileName,
  error,
}) => {
  return (
    <Box sx={{ mb: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
        🧪 在线测试
      </Typography>
      
      {/* 图片选择和参数设置 */}
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3, mb: 3 }}>
        {/* 左侧：图片选择 */}
        <Box sx={{ flex: 1 }}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
              <Button 
                variant="outlined" 
                size="small"
                onClick={onUseDefaultImage}
              >
                使用示例图片
              </Button>
            </Box>
            
            <ImageInput 
              onImageSelect={onImageSelect} 
              forceTabValue={forceTabValue}
              forceImageUrl={forceImageUrl}
              onTabChange={onTabChange}
            />
            
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
                    maxWidth: 'min(100%, 450px)', 
                    minWidth: '250px',
                    height: 'auto', 
                    border: '2px solid #e0e0e0',
                    borderRadius: '8px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                  }}
                  downloadFileName="current-image.jpg"
                />
              </Box>
            )}
          </Paper>
        </Box>

        {/* 右侧：参数设置 */}
        <Box sx={{ flex: 1 }}>
          {SettingsComponent && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                参数设置
              </Typography>
              <SettingsComponent
                onSettingsChange={onSettingsChange}
                isLoading={isLoading}
                appliedParams={appliedParams}
                settings={currentSettings}
              />
            </Paper>
          )}
        </Box>
      </Box>

      {/* 开始处理按钮 */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Button
          ref={processButtonRef}
          fullWidth
          variant="contained"
          color="primary"
          onClick={onProcess}
          disabled={isLoading}
          size="large"
        >
          {isLoading ? '处理中...' : '开始处理'}
        </Button>
      </Paper>

      {/* 错误信息 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* 处理结果 */}
      {resultImage && (
        <Paper sx={{ p: 3 }}>
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
              border: '1px solid #ddd',
              borderRadius: '8px'
            }}
            downloadFileName={downloadFileName}
          />
          <Button 
            fullWidth
            variant="outlined" 
            color="primary" 
            sx={{ mt: 2 }}
            href={resultImage}
            download={downloadFileName}
          >
            下载图片
          </Button>
        </Paper>
      )}
    </Box>
  );
};
