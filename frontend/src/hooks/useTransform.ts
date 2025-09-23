import { useState } from 'react';
import axios from 'axios';

export type TransformType = 'rotate' | 'flip-horizontal' | 'flip-vertical' | 'rotate-90-cw' | 'rotate-90-ccw' | 'rotate-180';

export interface RotateSettings {
  angle: number;
  expand: boolean;
  fillColor: string;
}

export const useTransform = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [transformType, setTransformType] = useState<TransformType>('rotate');
  const [quality, setQuality] = useState<number>(90);
  
  // 旋转设置
  const [rotateSettings, setRotateSettings] = useState<RotateSettings>({
    angle: 0,
    expand: true,
    fillColor: '#ffffff'
  });
  
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setResultImage(null);
  };

  const handleApplyTransform = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('quality', quality.toString());

      let endpoint = '';
      
      switch (transformType) {
        case 'rotate':
          endpoint = '/transform/rotate';
          formData.append('angle', rotateSettings.angle.toString());
          formData.append('expand', rotateSettings.expand.toString());
          formData.append('fill_color', rotateSettings.fillColor);
          break;
          
        case 'flip-horizontal':
          endpoint = '/transform/flip-horizontal';
          break;
          
        case 'flip-vertical':
          endpoint = '/transform/flip-vertical';
          break;
          
        case 'rotate-90-cw':
          endpoint = '/transform/rotate-90-cw';
          break;
          
        case 'rotate-90-ccw':
          endpoint = '/transform/rotate-90-ccw';
          break;
          
        case 'rotate-180':
          endpoint = '/transform/rotate-180';
          break;
          
        default:
          throw new Error('未知的变换类型');
      }

      const response = await axios.post(endpoint, formData, {
        responseType: 'blob',
      });

      const imageUrl = URL.createObjectURL(response.data);
      setResultImage(imageUrl);
    } catch (error) {
      console.error('Error transforming image:', error);
      alert('变换图片失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  const getTransformTypeName = (type: TransformType): string => {
    const names = {
      'rotate': '自定义旋转',
      'flip-horizontal': '水平翻转',
      'flip-vertical': '垂直翻转',
      'rotate-90-cw': '顺时针90°',
      'rotate-90-ccw': '逆时针90°',
      'rotate-180': '旋转180°'
    };
    return names[type];
  };

  return {
    selectedFile,
    transformType,
    setTransformType,
    quality,
    setQuality,
    rotateSettings,
    setRotateSettings,
    resultImage,
    isLoading,
    handleImageSelected,
    handleApplyTransform,
    getTransformTypeName,
  };
};