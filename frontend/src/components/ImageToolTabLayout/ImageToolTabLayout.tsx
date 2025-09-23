import React from 'react';
import { Box } from '@mui/material';
import { ApiIntegrationTabs } from '../ApiIntegrationTabs';
import { EffectShowcase } from '../EffectShowcase';
import { OnlineTestSection } from '../OnlineTestSection';
import { ApiEndpoint, EffectExample, MultiImageEffectExample } from '../../types/api';
import { useImageProcessing } from '../../hooks/useImageProcessing';
import { useNotification } from '../../hooks/useNotification';
import { useApiRequest } from '../../hooks/useApiRequest';
import { NotificationProvider } from '../NotificationProvider';
import { DEFAULT_SAMPLE_IMAGE } from '../../config/constants';

interface ImageProcessingOptions {
  showOriginal: boolean;
  originalImage: string | null;
  showOriginalSize: boolean;
  enableSizeComparison: boolean;
}

export interface ImageToolTabLayoutProps {
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
  effectExamples?: EffectExample[] | MultiImageEffectExample[];
  downloadFileName?: string;
  enableLargeDisplay?: boolean;
  customFormDataBuilder?: (formData: FormData, settings: Record<string, any>) => void;
  customJsonDataBuilder?: (imageUrl: string, settings: Record<string, any>) => any;
}

export const ImageToolTabLayout: React.FC<ImageToolTabLayoutProps> = ({
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

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const handleSettingsChange = (newSettings: any) => {
    setCurrentSettings(newSettings);
    if (onSettingsChange) {
      onSettingsChange(newSettings);
    }
  };

  const handleApplyParams = (params: any) => {
    setCurrentSettings(params);
    setAppliedParams(params);
  };

  // 构建额外内容（效果展示和在线测试）
  const additionalContent = (
    <Box>
      {/* 效果展示 */}
      {effectExamples && effectExamples.length > 0 && (
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
      )}

      {/* 在线测试 */}
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
    </Box>
  );

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
        <h4>{title}</h4>
        <ApiIntegrationTabs
          endpoint={endpoint}
          settings={currentSettings}
          additionalHttpContent={additionalContent}
        />
      </Box>
    </NotificationProvider>
  );
};
