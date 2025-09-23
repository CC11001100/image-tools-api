import { useState } from 'react';
import axios from 'axios';

export type CropType = 'rectangle' | 'circle' | 'smart-center';

export interface CropRectangle {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface CropCircle {
  centerX: number;
  centerY: number;
  radius: number;
}

export interface CropSmartCenter {
  targetWidth: number;
  targetHeight: number;
}

export const useCrop = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [cropType, setCropType] = useState<CropType>('rectangle');
  const [quality, setQuality] = useState<number>(90);
  
  // 矩形裁剪参数
  const [rectangle, setRectangle] = useState<CropRectangle>({
    x: 0,
    y: 0,
    width: 200,
    height: 200
  });
  
  // 圆形裁剪参数
  const [circle, setCircle] = useState<CropCircle>({
    centerX: 100,
    centerY: 100,
    radius: 50
  });
  
  // 智能居中裁剪参数
  const [smartCenter, setSmartCenter] = useState<CropSmartCenter>({
    targetWidth: 400,
    targetHeight: 400
  });
  
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [originalImageSize, setOriginalImageSize] = useState<{width: number, height: number} | null>(null);

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setResultImage(null);
    
    // 获取图片尺寸
    const img = new Image();
    img.onload = () => {
      setOriginalImageSize({ width: img.width, height: img.height });
      
      // 根据图片尺寸调整默认裁剪参数
      const centerX = Math.floor(img.width / 2);
      const centerY = Math.floor(img.height / 2);
      const defaultSize = Math.min(img.width, img.height) / 4;
      
      setRectangle({
        x: centerX - defaultSize / 2,
        y: centerY - defaultSize / 2,
        width: defaultSize,
        height: defaultSize
      });
      
      setCircle({
        centerX,
        centerY,
        radius: defaultSize / 2
      });
      
      setSmartCenter({
        targetWidth: Math.min(400, img.width),
        targetHeight: Math.min(400, img.height)
      });
    };
    img.src = URL.createObjectURL(file);
  };

  const handleApplyCrop = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('quality', quality.toString());

      let endpoint = '';
      
      switch (cropType) {
        case 'rectangle':
          endpoint = '/crop/rectangle';
          formData.append('x', Math.round(rectangle.x).toString());
          formData.append('y', Math.round(rectangle.y).toString());
          formData.append('width', Math.round(rectangle.width).toString());
          formData.append('height', Math.round(rectangle.height).toString());
          break;
          
        case 'circle':
          endpoint = '/crop/circle';
          formData.append('center_x', Math.round(circle.centerX).toString());
          formData.append('center_y', Math.round(circle.centerY).toString());
          formData.append('radius', Math.round(circle.radius).toString());
          break;
          
        case 'smart-center':
          endpoint = '/crop/smart-center';
          formData.append('target_width', smartCenter.targetWidth.toString());
          formData.append('target_height', smartCenter.targetHeight.toString());
          break;
          
        default:
          throw new Error('未知的裁剪类型');
      }

      const response = await axios.post(endpoint, formData, {
        responseType: 'blob',
      });

      const imageUrl = URL.createObjectURL(response.data);
      setResultImage(imageUrl);
    } catch (error) {
      console.error('Error cropping image:', error);
      alert('裁剪图片失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    selectedFile,
    cropType,
    setCropType,
    quality,
    setQuality,
    rectangle,
    setRectangle,
    circle,
    setCircle,
    smartCenter,
    setSmartCenter,
    resultImage,
    isLoading,
    originalImageSize,
    handleImageSelected,
    handleApplyCrop,
  };
}; 