import React from 'react';
import { Typography, Box } from '@mui/material';
import { EffectShowcase } from '../EffectShowcase';
import { OnlineTestSection } from '../OnlineTestSection';
import { ApiDocumentationTabs } from '../ApiDocumentationTabs';
import { useImageProcessing } from '../../hooks/useImageProcessing';
import { useNotification } from '../../hooks/useNotification';
import { useApiRequest } from '../../hooks/useApiRequest';
import { NotificationProvider } from '../NotificationProvider';
import { EffectExample } from '../../types/api';
import { ApiEndpoint } from '../../types/api';
import { DEFAULT_SAMPLE_IMAGE } from '../../config/constants';

interface ImageProcessingOptions {
  showOriginal: boolean;
  originalImage: string | null;
  showOriginalSize: boolean;
  enableSizeComparison: boolean;
}

export interface StandardImageProcessingPageProps {
  title: string;
  description: string;
  endpoint: ApiEndpoint;
  settings?: Record<string, any>;
  onSettingsChange?: (settings: any) => void;
  settingsComponent?: React.ComponentType<{
    onSettingsChange: (settings: any) => void;
    isLoading: boolean;
    appliedParams?: Record<string, any> | null;
    [key: string]: any;
  }>;
  effectExamples?: EffectExample[];
  downloadFileName?: string;
  enableLargeDisplay?: boolean;
  customFormDataBuilder?: (formData: FormData, settings: Record<string, any>) => void;
  customJsonDataBuilder?: (imageUrl: string, settings: Record<string, any>) => any;
}

export const StandardImageProcessingPage: React.FC<StandardImageProcessingPageProps> = ({
  title,
  description,
  endpoint,
  settings,
  onSettingsChange,
  settingsComponent: SettingsComponent,
  effectExamples,
  downloadFileName = 'processed-image.jpg',
  enableLargeDisplay = false,
  customFormDataBuilder,
  customJsonDataBuilder
}) => {
  const [currentSettings, setCurrentSettings] = React.useState(settings || {});
  const [isLoading, setIsLoading] = React.useState(false);
  const [showImagePreview, setShowImagePreview] = React.useState(false);
  const [previewUrl, setPreviewUrl] = React.useState<string | null>(null);
  const [resultImage, setResultImage] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [appliedParams, setAppliedParams] = React.useState<Record<string, any> | null>(null);
  const [forceTabValue, setForceTabValue] = React.useState<number>();
  const [forceImageUrl, setForceImageUrl] = React.useState<string>();
  const processButtonRef = React.useRef<HTMLButtonElement>(null);

  const notification = useNotification();
  const imageProcessing = useImageProcessing();
  const { processImage } = useApiRequest();

  // 图片处理选项
  const imageProcessingOptions: ImageProcessingOptions = {
    showOriginal: true,
    originalImage: previewUrl,
    showOriginalSize: false,
    enableSizeComparison: false
  };

  const handleImageSelect = (file: File | null, imageUrl: string | null) => {
    // 调用imageProcessing的handleImageSelect来正确保存文件状态
    imageProcessing.handleImageSelect(file, imageUrl);

    if (file) {
      setPreviewUrl(URL.createObjectURL(file));
      setShowImagePreview(true);
    } else if (imageUrl) {
      setPreviewUrl(imageUrl);
      setShowImagePreview(true);
    }
  };

  const handleUseDefaultImage = () => {
    imageProcessing.handleUseDefaultImage();
    setPreviewUrl(DEFAULT_SAMPLE_IMAGE);
    setShowImagePreview(true);
  };

  const handleProcess = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // 处理逻辑
      await processImage({
        selectedFile: imageProcessing.selectedFile,
        selectedImageUrl: imageProcessing.selectedImageUrl,
        previewUrl,
        settings: currentSettings,
        getApiPath: () => endpoint.path,
        getUrlApiPath: () => endpoint.urlPath,
        requestType: endpoint.requestType,
        getFormData: customFormDataBuilder || ((formData: FormData, settings: Record<string, any>) => {
          for (const [key, value] of Object.entries(settings)) {
            formData.append(key, String(value));
          }
        }),
        getJsonData: customJsonDataBuilder,
        onSuccess: setResultImage,
        onError: setError,
        onLoadingChange: setIsLoading,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : '处理失败');
    } finally {
      setIsLoading(false);
    }
  };

  const handleApplyParams = (params: any) => {
    setCurrentSettings(params);
    setAppliedParams(params);
  };

  return (
    <NotificationProvider
      notification={{
        isOpen: notification.isOpen,
        message: notification.message,
        type: notification.type,
        onClose: notification.hideNotification,
      }}
    >
      <Box>
        {/* 第一部分：页面标题和描述 */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            {title}
          </Typography>
          <Typography variant="body1" paragraph>
            {description}
          </Typography>
        </Box>

        {/* 第二部分：效果展示 */}
        {effectExamples && effectExamples.length > 0 && (
          <Box sx={{ mb: 4 }}>
            <EffectShowcase
              title="🎨 效果展示"
              description="以下是功能效果的实际示例，点击图片可查看大图"
              examples={effectExamples}
              showOriginal={imageProcessingOptions.showOriginal}
              originalImage={imageProcessingOptions.originalImage || undefined}
              onApplyParams={handleApplyParams}
              enableSizeComparison={imageProcessingOptions.enableSizeComparison}
              showOriginalSize={imageProcessingOptions.showOriginalSize}
              enableLargeDisplay={enableLargeDisplay}
            />
          </Box>
        )}

        {/* 第三部分：在线测试 */}
        <OnlineTestSection
          onImageSelect={handleImageSelect}
          onUseDefaultImage={handleUseDefaultImage}
          previewUrl={previewUrl}
          showImagePreview={showImagePreview}
          settingsComponent={SettingsComponent}
          onSettingsChange={setCurrentSettings}
          isLoading={isLoading}
          onProcess={handleProcess}
          appliedParams={appliedParams}
          processButtonRef={processButtonRef}
          forceTabValue={forceTabValue}
          forceImageUrl={forceImageUrl}
          onTabChange={(tabValue) => {
            console.log('📋 ImageInput tab changed to:', tabValue);
            // 清除强制状态，避免重复触发
            setForceTabValue(undefined);
            setForceImageUrl(undefined);
          }}
          currentSettings={currentSettings}
          resultImage={resultImage}
          downloadFileName={downloadFileName}
          error={error}
        />

        {/* 第四部分：API文档 */}
        <ApiDocumentationTabs endpoint={endpoint} />
      </Box>
    </NotificationProvider>
  );
}; 