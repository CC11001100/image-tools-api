#!/usr/bin/env python3
"""
更新前端配置文件，指向新生成的1080x1920尺寸图片
任务2859：更新配置文件以使用正确尺寸的图片
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def update_noise_examples():
    """更新noise页面配置"""
    print("🔧 更新noise页面配置...")
    
    config_path = project_root / "frontend/src/config/examples/noiseExamples.ts"
    
    new_content = '''import { EffectExample } from '../../types/api';

export const noiseExamples: EffectExample[] = [
  {
    title: '高斯噪点',
    description: '添加高斯噪点，模拟传感器噪点效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/noise/original-gaussian.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/noise/noise-gaussian.jpg',
    parameters: [
      { label: '噪点类型', value: '高斯' },
      { label: '强度', value: '10%' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/noise',
      noise_type: 'gaussian',
      intensity: 10,
      quality: 90
    }
  }
];
'''
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("   ✅ noise配置已更新")

def update_pixelate_examples():
    """更新pixelate页面配置"""
    print("🔧 更新pixelate页面配置...")
    
    config_path = project_root / "frontend/src/config/examples/pixelateExamples.ts"
    
    new_content = '''import { EffectExample } from '../../types/api';

export const pixelateExamples: EffectExample[] = [
  {
    title: '像素化效果',
    description: '对整张图片应用10像素马赛克，像素化效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/original-pixelate.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/pixelate-pixelate.jpg',
    parameters: [
      { label: '像素大小', value: '10px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/pixelate',
      pixel_size: 10,
      quality: 90
    }
  },
  {
    title: '马赛克效果',
    description: '对整张图片应用20像素马赛克，马赛克效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/original-mosaic.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/pixelate-mosaic.jpg',
    parameters: [
      { label: '像素大小', value: '20px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/pixelate',
      pixel_size: 20,
      quality: 90
    }
  },
  {
    title: '复古像素',
    description: '对整张图片应用8像素马赛克，复古像素效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/original-retro.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/pixelate/pixelate-retro.jpg',
    parameters: [
      { label: '像素大小', value: '8px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/pixelate',
      pixel_size: 8,
      quality: 90
    }
  }
];
'''
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("   ✅ pixelate配置已更新")

def update_overlay_examples():
    """更新overlay页面配置"""
    print("🔧 更新overlay页面配置...")
    
    config_path = project_root / "frontend/src/config/examples/overlayExamples.ts"
    
    new_content = '''import { EffectExample } from '../../types/api';

export const overlayExamples: EffectExample[] = [
  {
    title: '线性渐变',
    description: '添加线性渐变叠加效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-linear_gradient.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-linear_gradient.jpg',
    parameters: [
      { label: '叠加类型', value: '渐变' },
      { label: '渐变类型', value: '线性' },
      { label: '透明度', value: '50%' }
    ],
    apiParams: {
      endpoint: '/api/v1/overlay',
      overlay_type: 'gradient',
      gradient_type: 'linear',
      colors: ['#FF0000', '#0000FF'],
      opacity: 0.5
    }
  },
  {
    title: '径向渐变',
    description: '添加径向渐变叠加效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-radial_gradient.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-radial_gradient.jpg',
    parameters: [
      { label: '叠加类型', value: '渐变' },
      { label: '渐变类型', value: '径向' },
      { label: '透明度', value: '60%' }
    ],
    apiParams: {
      endpoint: '/api/v1/overlay',
      overlay_type: 'gradient',
      gradient_type: 'radial',
      colors: ['#FFFF00', '#FF00FF'],
      opacity: 0.6
    }
  },
  {
    title: '暗角效果',
    description: '添加暗角效果，突出中心区域',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-vignette.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-vignette.jpg',
    parameters: [
      { label: '叠加类型', value: '暗角' },
      { label: '强度', value: '70%' },
      { label: '透明度', value: '80%' }
    ],
    apiParams: {
      endpoint: '/api/v1/overlay',
      overlay_type: 'vignette',
      intensity: 0.7,
      opacity: 0.8
    }
  }
];
'''
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("   ✅ overlay配置已更新")

def update_mask_examples():
    """更新mask页面配置"""
    print("🔧 更新mask页面配置...")
    
    config_path = project_root / "frontend/src/config/examples/maskExamples.ts"
    
    new_content = '''import { EffectExample } from '../../types/api';

// 遮罩效果示例
export const maskExamples: EffectExample[] = [
  {
    title: '圆形遮罩',
    description: '使用圆形遮罩裁剪图片，创建圆形效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-circle.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-circle.jpg',
    parameters: [
      { label: '遮罩类型', value: '圆形' },
      { label: '羽化', value: '10px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/mask',
      mask_type: 'circle',
      feather: 10,
      quality: 90
    }
  },
  {
    title: '矩形遮罩',
    description: '使用矩形遮罩裁剪图片，创建矩形效果',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/original-rectangle.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/mask/mask-rectangle.jpg',
    parameters: [
      { label: '遮罩类型', value: '矩形' },
      { label: '羽化', value: '5px' },
      { label: '质量', value: '90' }
    ],
    apiParams: {
      endpoint: '/api/v1/mask',
      mask_type: 'rectangle',
      feather: 5,
      quality: 90
    }
  }
];
'''
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("   ✅ mask配置已更新")

def update_format_examples():
    """更新format页面配置"""
    print("🔧 更新format页面配置...")
    
    config_path = project_root / "frontend/src/config/examples/formatExamples.ts"
    
    new_content = '''import { EffectExample } from '../../types/api';

export const formatExamples: EffectExample[] = [
  {
    title: 'JPEG格式转换',
    description: '将图片转换为JPEG格式，适合照片存储',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-jpeg.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-jpeg.jpg',
    parameters: [
      { label: '目标格式', value: 'JPEG' },
      { label: '质量', value: '90%' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      format: 'jpeg',
      quality: 90,
      optimize: true
    }
  },
  {
    title: 'PNG格式转换',
    description: '将图片转换为PNG格式，支持透明度',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-png.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-png.png',
    parameters: [
      { label: '目标格式', value: 'PNG' },
      { label: '质量', value: '100%' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      format: 'png',
      quality: 100,
      optimize: true
    }
  },
  {
    title: 'WebP格式转换',
    description: '将图片转换为WebP格式，现代高效格式',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/original-webp.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/format/format-webp.webp',
    parameters: [
      { label: '目标格式', value: 'WebP' },
      { label: '质量', value: '85%' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/format',
      format: 'webp',
      quality: 85,
      optimize: true
    }
  }
];
'''
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("   ✅ format配置已更新")

def update_gif_examples():
    """更新gif页面配置"""
    print("🔧 更新gif页面配置...")
    
    config_path = project_root / "frontend/src/config/examples/gifExamples.ts"
    
    new_content = '''import { EffectExample } from '../../types/api';

export const gifExamples: EffectExample[] = [
  {
    title: '创建GIF',
    description: '将多张图片合成为GIF动画',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-create.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/gif-create.gif',
    parameters: [
      { label: '帧间隔', value: '500ms' },
      { label: '循环', value: '无限' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/gif/create',
      duration: 500,
      loop: true,
      optimize: true
    }
  },
  {
    title: '快速GIF',
    description: '创建快速播放的GIF动画',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/original-fast.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/gif/gif-fast.gif',
    parameters: [
      { label: '帧间隔', value: '200ms' },
      { label: '循环', value: '无限' },
      { label: '优化', value: '启用' }
    ],
    apiParams: {
      endpoint: '/api/v1/gif/create',
      duration: 200,
      loop: true,
      optimize: true
    }
  }
];
'''
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("   ✅ gif配置已更新")

def update_stitch_examples():
    """更新stitch页面配置"""
    print("🔧 更新stitch页面配置...")

    config_path = project_root / "frontend/src/config/examples/stitchExamples.ts"

    new_content = '''import { EffectExample } from '../../types/api';

export const stitchExamples: EffectExample[] = [
  {
    title: '水平拼接',
    description: '将多张图片水平排列拼接成一张长图',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-horizontal.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-horizontal.jpg',
    parameters: [
      { label: '方向', value: 'horizontal' },
      { label: '图片1', value: '1080x1920' },
      { label: '图片2', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'horizontal',
      spacing: 10,
      quality: 90
    }
  },
  {
    title: '垂直拼接',
    description: '将多张图片垂直排列拼接成一张高图',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-vertical.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-vertical.jpg',
    parameters: [
      { label: '方向', value: 'vertical' },
      { label: '图片1', value: '1080x1920' },
      { label: '图片2', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'vertical',
      spacing: 5,
      quality: 90
    }
  },
  {
    title: '网格拼接',
    description: '将四张图片排列成2x2网格布局',
    originalImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/original1-grid.jpg',
    processedImage: 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/stitch/stitch-grid.jpg',
    parameters: [
      { label: '方向', value: 'grid' },
      { label: '图片1', value: '1080x1920' },
      { label: '图片2', value: '1080x1920' }
    ],
    apiParams: {
      endpoint: '/api/v1/stitch',
      direction: 'grid',
      spacing: 8,
      quality: 90
    }
  }
];
'''

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("   ✅ stitch配置已更新")

def main():
    """主函数"""
    print("🚀 开始更新前端配置文件...")
    print("=" * 60)

    # 更新各个页面的配置
    update_noise_examples()
    update_pixelate_examples()
    update_overlay_examples()
    update_mask_examples()
    update_format_examples()
    update_gif_examples()
    update_stitch_examples()

    print("\n" + "=" * 60)
    print("🎉 所有配置文件更新完成！")
    print("现在所有页面都指向1080x1920尺寸的图片")

if __name__ == "__main__":
    main()
