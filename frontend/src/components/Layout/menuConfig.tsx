/**
 * 菜单配置
 */

import React from 'react';
import {
  Home as HomeIcon,
  TextFields as TextFieldsIcon,
  ZoomIn as ZoomInIcon,
  FilterVintage as FilterVintageIcon,
  Palette as PaletteIcon,
  CropFree as CropFreeIcon,
  RotateRight as RotateRightIcon,
  CameraAlt as CameraAltIcon,
  Layers as LayersIcon,
  ViewModule as ViewModuleIcon,
  Grain as GrainIcon,
  ColorLens as ColorLensIcon,
  AutoFixHigh as AutoFixHighIcon,
  GridOn as GridOnIcon,
  AspectRatio as AspectRatioIcon,
  AddPhotoAlternate as AddPhotoAlternateIcon,
  BlurOn as BlurOnIcon,
  Gif as GifIcon,
  TextFormat as TextFormatIcon,
  Create as CreateIcon,
  Image as ImageIcon,
  PhotoFilter as PhotoFilterIcon,
  Collections as CollectionsIcon,
  Folder as FolderIcon,
  InsertDriveFile as InsertDriveFileIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

import { MenuItem } from './types';

export const drawerWidth = 260;

export const menuItems: MenuItem[] = [
  { text: '首页', path: '/', icon: <HomeIcon /> },
  {
    text: '基础编辑',
    icon: <ImageIcon />,
    children: [
      { text: '调整大小', path: '/resize', icon: <ZoomInIcon /> },
      { text: '裁剪', path: '/crop', icon: <CropFreeIcon /> },
      { text: '旋转翻转', path: '/transform', icon: <RotateRightIcon /> },
      { text: '画布调整', path: '/canvas', icon: <AspectRatioIcon /> },
      { text: '透视变换', path: '/perspective', icon: <CameraAltIcon /> },
    ],
  },
  {
    text: '滤镜效果',
    icon: <PhotoFilterIcon />,
    children: [
      { text: '基础滤镜', path: '/filter', icon: <FilterVintageIcon /> },
      { text: '艺术滤镜', path: '/art-filter', icon: <PaletteIcon /> },
      { text: '色彩调整', path: '/color', icon: <ColorLensIcon /> },
      { text: '图片增强', path: '/enhance', icon: <AutoFixHighIcon /> },
      { text: '图片噪点', path: '/noise', icon: <GrainIcon /> },
      { text: '马赛克', path: '/pixelate', icon: <GridOnIcon /> },
    ],
  },
  {
    text: '文字与标注',
    icon: <TextFieldsIcon />,
    children: [
      { text: '图片水印', path: '/watermark', icon: <TextFieldsIcon /> },
      { text: '文字添加', path: '/text', icon: <TextFormatIcon /> },
      { text: '图片标注', path: '/annotation', icon: <CreateIcon /> },
    ],
  },
  {
    text: '图像合成',
    icon: <CollectionsIcon />,
    children: [
      { text: '图层混合', path: '/blend', icon: <LayersIcon /> },
      { text: '图片拼接', path: '/stitch', icon: <ViewModuleIcon /> },
      { text: '图片叠加', path: '/overlay', icon: <AddPhotoAlternateIcon /> },
      { text: '遮罩效果', path: '/mask', icon: <BlurOnIcon /> },
    ],
  },
  {
    text: '格式转换',
    icon: <FolderIcon />,
    children: [
      { text: '格式转换', path: '/format', icon: <InsertDriveFileIcon /> },
      { text: '图片信息', path: '/image-info', icon: <InfoIcon /> },
    ],
  },
  {
    text: 'GIF处理',
    icon: <GifIcon />,
    children: [
      { text: 'GIF帧提取', path: '/gif-extract', icon: <PhotoFilterIcon /> },
      { text: 'GIF动画创建', path: '/gif-create', icon: <AddPhotoAlternateIcon /> },
      { text: 'GIF优化压缩', path: '/gif-optimize', icon: <GifIcon /> },
    ],
  },
];
