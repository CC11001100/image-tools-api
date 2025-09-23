/**
 * GIF帧提取器 - 重构版本
 * 将原来的483行大文件拆分为多个小组件，提高可维护性
 */

import React, { useState, useCallback, useRef } from 'react';
import {
  Box,
  Grid,
} from '@mui/material';

import { useNotification } from '../../hooks/useNotification';
import FileUpload from './FileUpload';
import GifPreview from './GifPreview';
import ExtractionControl from './ExtractionControl';
import FrameSelector from './FrameSelector';
import { useFrameExtraction } from './hooks';
import { Frame } from './types';

const GifFrameExtractor: React.FC = () => {
  const [gifFile, setGifFile] = useState<File | null>(null);
  const [gifPreviewUrl, setGifPreviewUrl] = useState<string | null>(null);
  const [frames, setFrames] = useState<Frame[]>([]);
  const [selectedFrames, setSelectedFrames] = useState<Set<number>>(new Set());
  const [isExtracting, setIsExtracting] = useState(false);
  const [isPlaying, setIsPlaying] = useState(true);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { showNotification } = useNotification();
  const { extractFramesPreviews, validateFile, extractFrames } = useFrameExtraction(showNotification);

  // 处理文件选择
  const handleFileSelect = useCallback(async (file: File) => {
    if (!validateFile(file)) {
      return;
    }

    setGifFile(file);
    const url = URL.createObjectURL(file);
    setGifPreviewUrl(url);
    
    // 提取帧预览
    const newFrames = await extractFramesPreviews(file);
    setFrames(newFrames);
    setSelectedFrames(new Set());
  }, [validateFile, extractFramesPreviews]);

  // 切换帧选择
  const toggleFrameSelection = useCallback((frameIndex: number) => {
    setSelectedFrames(prev => {
      const newSet = new Set(prev);
      if (newSet.has(frameIndex)) {
        newSet.delete(frameIndex);
      } else {
        newSet.add(frameIndex);
      }
      return newSet;
    });
  }, []);

  // 全选/取消全选
  const handleSelectAll = useCallback(() => {
    if (selectedFrames.size === frames.length) {
      setSelectedFrames(new Set());
    } else {
      setSelectedFrames(new Set(frames.map(f => f.index)));
    }
  }, [frames, selectedFrames.size]);

  // 清空选择
  const handleClearSelection = useCallback(() => {
    setSelectedFrames(new Set());
  }, []);

  // 提取选中的帧
  const handleExtractFrames = useCallback(async () => {
    if (!gifFile) {
      showNotification('请先上传GIF文件', 'warning');
      return;
    }

    if (selectedFrames.size === 0) {
      showNotification('请选择要提取的帧', 'warning');
      return;
    }

    setIsExtracting(true);
    try {
      await extractFrames(gifFile, selectedFrames, frames.length);
    } finally {
      setIsExtracting(false);
    }
  }, [gifFile, selectedFrames, frames.length, extractFrames, showNotification]);

  // 重置
  const handleReset = useCallback(() => {
    setGifFile(null);
    if (gifPreviewUrl) {
      URL.revokeObjectURL(gifPreviewUrl);
    }
    setGifPreviewUrl(null);
    setFrames([]);
    setSelectedFrames(new Set());
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [gifPreviewUrl]);

  return (
    <Box>
      {/* 文件上传区域 */}
      {!gifFile && (
        <FileUpload
          onFileSelect={handleFileSelect}
          fileInputRef={fileInputRef}
        />
      )}

      {/* GIF预览和控制 */}
      {gifFile && gifPreviewUrl && (
        <Grid container spacing={3}>
          {/* 左侧：GIF预览 */}
          <Grid item xs={12} md={6}>
            <GifPreview
              gifFile={gifFile}
              gifPreviewUrl={gifPreviewUrl}
              frames={frames}
              isPlaying={isPlaying}
              setIsPlaying={setIsPlaying}
              onReset={handleReset}
            />
          </Grid>

          {/* 右侧：操作控制 */}
          <Grid item xs={12} md={6}>
            <ExtractionControl
              selectedFrames={selectedFrames}
              frames={frames}
              isExtracting={isExtracting}
              onSelectAll={handleSelectAll}
              onClearSelection={handleClearSelection}
              onExtractFrames={handleExtractFrames}
            />
          </Grid>
        </Grid>
      )}

      {/* 帧选择器 */}
      <FrameSelector
        frames={frames}
        selectedFrames={selectedFrames}
        onToggleFrameSelection={toggleFrameSelection}
      />
    </Box>
  );
};

export default GifFrameExtractor;
