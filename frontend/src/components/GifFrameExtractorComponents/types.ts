/**
 * GIF帧提取器相关的类型定义
 */

export interface Frame {
  index: number;
  dataUrl: string;
  selected: boolean;
}

export interface FileUploadProps {
  onFileSelect: (file: File) => void;
  fileInputRef: React.RefObject<HTMLInputElement>;
}

export interface GifPreviewProps {
  gifFile: File;
  gifPreviewUrl: string;
  frames: Frame[];
  isPlaying: boolean;
  setIsPlaying: (playing: boolean) => void;
  onReset: () => void;
}

export interface ExtractionControlProps {
  selectedFrames: Set<number>;
  frames: Frame[];
  isExtracting: boolean;
  onSelectAll: () => void;
  onClearSelection: () => void;
  onExtractFrames: () => void;
}

export interface FrameSelectorProps {
  frames: Frame[];
  selectedFrames: Set<number>;
  onToggleFrameSelection: (frameIndex: number) => void;
}
