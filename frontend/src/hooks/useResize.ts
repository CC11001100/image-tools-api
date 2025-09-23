import { useState } from 'react';
import axios from 'axios';

export const useResize = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [width, setWidth] = useState<string>('');
  const [height, setHeight] = useState<string>('');
  const [maintainRatio, setMaintainRatio] = useState<boolean>(true);
  const [quality, setQuality] = useState<number>(90);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setResultImage(null);
  };

  const handleApplyResize = async () => {
    if (!selectedFile || (!width && !height)) return;

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      if (width) formData.append('width', width);
      if (height) formData.append('height', height);
      
      formData.append('maintain_ratio', maintainRatio.toString());
      formData.append('quality', quality.toString());

      const response = await axios.post('/resize', formData, {
        responseType: 'blob',
      });

      const imageUrl = URL.createObjectURL(response.data);
      setResultImage(imageUrl);
    } catch (error) {
      console.error('Error resizing image:', error);
      alert('调整大小失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    selectedFile,
    width,
    setWidth,
    height,
    setHeight,
    maintainRatio,
    setMaintainRatio,
    quality,
    setQuality,
    resultImage,
    isLoading,
    handleImageSelected,
    handleApplyResize,
  };
}; 