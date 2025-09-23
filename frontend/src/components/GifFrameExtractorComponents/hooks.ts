/**
 * GIF帧提取器相关的自定义hooks
 */

import { useCallback } from 'react';
import { Frame } from './types';

export const useFrameExtraction = (showNotification: (message: string, type: 'success' | 'error' | 'warning') => void) => {
  // 提取帧预览信息
  const extractFramesPreviews = useCallback(async (file: File): Promise<Frame[]> => {
    try {
      // 估算帧数（基于文件大小的简单估算）
      const estimatedFrameCount = Math.min(50, Math.max(1, Math.floor(file.size / 30000)));
      const newFrames: Frame[] = [];
      
      // 创建占位符帧（显示帧编号）
      for (let i = 0; i < estimatedFrameCount; i++) {
        // 创建一个简单的占位符图片
        const canvas = document.createElement('canvas');
        canvas.width = 150;
        canvas.height = 150;
        const ctx = canvas.getContext('2d');
        
        if (ctx) {
          // 绘制背景
          ctx.fillStyle = '#f5f5f5';
          ctx.fillRect(0, 0, 150, 150);
          
          // 绘制边框
          ctx.strokeStyle = '#ddd';
          ctx.strokeRect(0, 0, 150, 150);
          
          // 绘制帧号
          ctx.fillStyle = '#666';
          ctx.font = '16px Arial';
          ctx.textAlign = 'center';
          ctx.fillText(`帧 ${i}`, 75, 75);
          ctx.font = '12px Arial';
          ctx.fillText('(预览)', 75, 95);
        }
        
        const dataUrl = canvas.toDataURL('image/png');
        newFrames.push({
          index: i,
          dataUrl,
          selected: false
        });
      }
      
      return newFrames;
    } catch (error) {
      console.error('生成帧预览失败:', error);
      showNotification('生成帧预览失败', 'error');
      return [];
    }
  }, [showNotification]);

  // 处理文件验证
  const validateFile = useCallback((file: File): boolean => {
    if (!file.type.includes('gif')) {
      showNotification('请上传GIF格式的文件', 'warning');
      return false;
    }

    if (file.size > 50 * 1024 * 1024) { // 50MB limit
      showNotification('文件过大，请上传小于50MB的GIF文件', 'warning');
      return false;
    }

    return true;
  }, [showNotification]);

  // 提取选中的帧
  const extractFrames = useCallback(async (
    gifFile: File,
    selectedFrames: Set<number>,
    framesLength: number
  ): Promise<boolean> => {
    try {
      const formData = new FormData();
      formData.append('file', gifFile);
      
      // 如果选择了所有帧，则不传frame_indices参数
      if (selectedFrames.size < framesLength) {
        const indices = Array.from(selectedFrames).sort((a, b) => a - b);
        formData.append('frame_indices', indices.join(','));
      }

      const response = await fetch('/api/gif/extract-frames', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // 处理下载
      const blob = await response.blob();
      const downloadUrl = URL.createObjectURL(blob);
      
      // 确定文件名和扩展名
      const contentType = response.headers.get('content-type');
      let filename = 'extracted_frames';
      let extension = '.zip';
      
      if (contentType?.includes('image/png')) {
        extension = '.png';
        filename = `frame_${Array.from(selectedFrames)[0]}`;
      }
      
      // 创建下载链接
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `${filename}${extension}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // 清理URL
      URL.revokeObjectURL(downloadUrl);
      
      const message = selectedFrames.size === 1 ? 
        '帧提取成功！' : 
        `成功提取${selectedFrames.size}帧，已打包为ZIP文件`;
      showNotification(message, 'success');
      
      return true;
    } catch (error) {
      console.error('提取帧失败:', error);
      showNotification(error instanceof Error ? error.message : '提取帧失败', 'error');
      return false;
    }
  }, [showNotification]);

  return {
    extractFramesPreviews,
    validateFile,
    extractFrames,
  };
};
