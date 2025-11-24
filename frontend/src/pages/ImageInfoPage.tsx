import React from 'react';
import { ImageInfoLayout } from '../components/ImageInfoLayout';
import { imageInfoEndpoint } from '../config/endpoints';

const ImageInfoPage: React.FC = () => {
  return (
    <ImageInfoLayout
      title="图片信息查询"
      description="快速获取图片的详细信息，包括格式、尺寸、大小、颜色模式、DPI、透明通道、GIF动画信息等。支持多种图片格式，一键查看完整参数。"
      endpoint={imageInfoEndpoint}
    />
  );
};

export default ImageInfoPage;
