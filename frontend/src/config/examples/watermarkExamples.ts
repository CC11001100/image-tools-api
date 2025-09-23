import { EffectExample } from '../../types/api';

// Watermark 效果示例
export const watermarkExamples: EffectExample[] = [
  {
    title: '中心文字水印',
    description: '在图像中心添加文字水印，适合版权保护',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/original-center-text.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/watermark-center-text.jpg",
    parameters: [
      { label: '文字内容', value: 'SAMPLE' },
      { label: '位置', value: '中心' },
      { label: '透明度', value: '80%' },
      { label: '字体大小', value: '48px' },
      { label: '颜色', value: '白色' }
    ],
    apiParams: {
      endpoint: '/api/v1/watermark',
      watermark_text: 'SAMPLE',
      position: 'center',
      font_size: 48,
      font_color: '#FFFFFF',
      opacity: 0.8
    }
  },
  {
    title: '右下角版权水印',
    description: '在图像右下角添加版权信息水印，不影响主体内容',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/original-bottom-right.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/watermark-bottom-right.jpg",
    parameters: [
      { label: '文字内容', value: '© 2024' },
      { label: '位置', value: '右下角' },
      { label: '透明度', value: '70%' },
      { label: '字体大小', value: '32px' },
      { label: '颜色', value: '白色' }
    ],
    apiParams: {
      endpoint: '/api/v1/watermark',
      watermark_text: '© 2024',
      position: 'bottom-right',
      font_size: 32,
      font_color: '#FFFFFF',
      opacity: 0.7
    }
  },
  {
    title: '对角线水印',
    description: '添加倾斜的对角线水印，增强视觉效果',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/original-diagonal.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/watermark-diagonal.jpg",
    parameters: [
      { label: '文字内容', value: 'WATERMARK' },
      { label: '位置', value: '中心' },
      { label: '透明度', value: '50%' },
      { label: '字体大小', value: '60px' },
      { label: '角度', value: '-30°' },
      { label: '颜色', value: '白色' }
    ],
    apiParams: {
      endpoint: '/api/v1/watermark',
      watermark_text: 'WATERMARK',
      position: 'center',
      font_size: 60,
      font_color: '#FFFFFF',
      opacity: 0.5,
      angle: -30
    }
  },
  {
    title: '左上角标识',
    description: '在左上角添加品牌标识水印',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/original-top-left.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/watermark-top-left.jpg",
    parameters: [
      { label: '文字内容', value: 'BRAND' },
      { label: '位置', value: '左上角' },
      { label: '透明度', value: '90%' },
      { label: '字体大小', value: '36px' },
      { label: '颜色', value: '黑色' }
    ],
    apiParams: {
      endpoint: '/api/v1/watermark',
      watermark_text: 'BRAND',
      position: 'top-left',
      font_size: 36,
      font_color: '#000000',
      opacity: 0.9
    }
  },
  {
    title: '透明水印',
    description: '添加高透明度的机密标识水印',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/original-transparent.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/watermark-transparent.jpg",
    parameters: [
      { label: '文字内容', value: 'CONFIDENTIAL' },
      { label: '位置', value: '中心' },
      { label: '透明度', value: '30%' },
      { label: '字体大小', value: '80px' },
      { label: '角度', value: '45°' },
      { label: '颜色', value: '红色' }
    ],
    apiParams: {
      endpoint: '/api/v1/watermark',
      watermark_text: 'CONFIDENTIAL',
      position: 'center',
      font_size: 80,
      font_color: '#FF0000',
      opacity: 0.3,
      angle: 45
    }
  },
  {
    title: '网站水印',
    description: '在左下角添加网站地址水印',
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/original-website.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/watermark/watermark-website.jpg",
    parameters: [
      { label: '文字内容', value: 'www.example.com' },
      { label: '位置', value: '左下角' },
      { label: '透明度', value: '80%' },
      { label: '字体大小', value: '28px' },
      { label: '颜色', value: '白色' }
    ],
    apiParams: {
      endpoint: '/api/v1/watermark',
      watermark_text: 'www.example.com',
      position: 'bottom-left',
      font_size: 28,
      font_color: '#FFFFFF',
      opacity: 0.8
    }
  }
];
