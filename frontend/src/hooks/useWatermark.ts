import { useState } from 'react';
import axios from 'axios';

type Position = 'center' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';

export const useWatermark = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [watermarkText, setWatermarkText] = useState<string>('水印文本');
  const [position, setPosition] = useState<Position>('bottom-right');
  const [opacity, setOpacity] = useState<number>(0.5);
  const [color, setColor] = useState<string>('#ffffff');
  const [fontSize, setFontSize] = useState<number>(40);
  const [angle, setAngle] = useState<number>(0);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setResultImage(null);
  };

  const handleApplyWatermark = async () => {
    if (!selectedFile || !watermarkText) return;

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('text', watermarkText);
      formData.append('position', position);
      formData.append('opacity', opacity.toString());
      formData.append('color', color);
      formData.append('font_size', fontSize.toString());
      formData.append('angle', angle.toString());

      const response = await axios.post('/watermark', formData, {
        responseType: 'blob',
      });

      const imageUrl = URL.createObjectURL(response.data);
      setResultImage(imageUrl);
    } catch (error) {
      console.error('Error applying watermark:', error);
      alert('添加水印失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    selectedFile,
    watermarkText,
    setWatermarkText,
    position,
    setPosition,
    opacity,
    setOpacity,
    color,
    setColor,
    fontSize,
    setFontSize,
    angle,
    setAngle,
    resultImage,
    isLoading,
    handleImageSelected,
    handleApplyWatermark,
  };
}; 