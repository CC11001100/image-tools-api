import { useState } from 'react';
import { DEFAULT_SAMPLE_IMAGE } from '../config/constants';

export interface UseImageProcessingReturn {
  // 状态
  selectedFile: File | null;
  selectedImageUrl: string | null;
  previewUrl: string | null;
  resultImage: string | null;
  isLoading: boolean;
  error: string | null;
  
  // 操作方法
  handleImageSelect: (file: File | null, imageUrl: string | null) => void;
  handleUseDefaultImage: () => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setResultImage: (image: string | null) => void;
  resetState: () => void;
}

export const useImageProcessing = (): UseImageProcessingReturn => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedImageUrl, setSelectedImageUrl] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = (file: File | null, imageUrl: string | null) => {
    setSelectedFile(file);
    setSelectedImageUrl(imageUrl);
    
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewUrl(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    } else if (imageUrl) {
      setPreviewUrl(imageUrl);
    }
    
    setError(null);
    setResultImage(null);
  };

  const handleUseDefaultImage = () => {
    setSelectedFile(null);
    setSelectedImageUrl(DEFAULT_SAMPLE_IMAGE);
    setPreviewUrl(DEFAULT_SAMPLE_IMAGE);
    setError(null);
    setResultImage(null);
  };

  const resetState = () => {
    setSelectedFile(null);
    setSelectedImageUrl(null);
    setPreviewUrl(null);
    setResultImage(null);
    setIsLoading(false);
    setError(null);
  };

  return {
    selectedFile,
    selectedImageUrl,
    previewUrl,
    resultImage,
    isLoading,
    error,
    handleImageSelect,
    handleUseDefaultImage,
    setIsLoading,
    setError,
    setResultImage,
    resetState,
  };
}; 