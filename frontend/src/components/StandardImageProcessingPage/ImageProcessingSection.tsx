import React from 'react';
import { Box, Button, Paper, Typography } from '@mui/material';
import { ImageInput } from '../ImageInput';
import { ClickableImage } from '../ClickableImage';

interface ImageProcessingSectionProps {
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
  // 新增：用于控制ImageInput的props
  forceTabValue?: number;
  forceImageUrl?: string;
  onTabChange?: (tabValue: number) => void;
  // 新增：当前设置
  currentSettings?: Record<string, any>;
}

export const ImageProcessingSection: React.FC<ImageProcessingSectionProps> = ({
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
}) => {
  return (
    <>
      <Paper sx={{ p: 3, mb: 3 }}>
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

      {SettingsComponent && (
        <Paper sx={{ p: 3, mb: 3 }}>
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

      <Paper sx={{ p: 3 }}>
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
    </>
  );
}; 