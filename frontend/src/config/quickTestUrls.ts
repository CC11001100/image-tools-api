export interface QuickTestUrl {
  name: string;
  url: string;
  description: string;
  resolution: string;
}

export const quickTestUrls: QuickTestUrl[] = [
  {
    name: '手机竖屏',
    url: 'https://picsum.photos/1080/1920?random=1',
    description: '适合手机竖屏显示的高清图片',
    resolution: '1080×1920'
  },
  {
    name: '平板横屏', 
    url: 'https://picsum.photos/1024/768?random=1',
    description: '适合平板横屏显示的标准图片',
    resolution: '1024×768'
  },
  {
    name: '低分辨率',
    url: 'https://picsum.photos/480/800?random=1', 
    description: '低分辨率图片，适合快速测试',
    resolution: '480×800'
  }
];

// 生成带时间戳的随机URL，避免缓存
export const generateRandomTestUrl = (baseUrl: string): string => {
  const timestamp = Date.now();
  return baseUrl.replace('random=1', `random=${timestamp}`);
}; 