// 默认示例图片URL（本地示例图片）
export const DEFAULT_SAMPLE_IMAGE = "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg";

// API基础URL - 根据环境自动配置
export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ||
  (window.location.hostname === 'localhost' ? 'http://localhost:58888' :
   `${window.location.protocol}//${window.location.hostname}`);

// 支持的图片格式
export const SUPPORTED_IMAGE_FORMATS = [
  'image/jpeg',
  'image/jpg', 
  'image/png',
  'image/gif',
  'image/bmp',
  'image/webp'
];

// 支持的图片扩展名
export const SUPPORTED_IMAGE_EXTENSIONS = [
  '.jpg',
  '.jpeg',
  '.png', 
  '.gif',
  '.bmp',
  '.webp'
]; 