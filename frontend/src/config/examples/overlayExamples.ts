import { EffectExample } from '../../types/api';

export const overlayExamples: EffectExample[] = [
  {
    title: "线性渐变叠加",
    description: "添加线性渐变叠加效果，营造层次感",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-linear_gradient.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-linear_gradient.jpg",
    parameters: [
      { label: '叠加类型', value: '渐变' },
      { label: '渐变类型', value: 'linear' },
      { label: '透明度', value: '60%' }
    ],
    apiParams: {
      endpoint: "/api/v1/overlay",
      overlay_type: "gradient",
      gradient_type: "linear",
      gradient_direction: "to_bottom",
      start_color: "#FF0000",
      end_color: "#0000FF",
      start_opacity: 0.0,
      end_opacity: 0.6,
      quality: 90
    }
  },
  {
    title: "径向渐变叠加",
    description: "添加径向渐变叠加效果，突出中心区域",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-radial_gradient.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-radial_gradient.jpg",
    parameters: [
      { label: '叠加类型', value: '渐变' },
      { label: '渐变类型', value: 'radial' },
      { label: '透明度', value: '70%' }
    ],
    apiParams: {
      endpoint: "/api/v1/overlay",
      overlay_type: "gradient",
      gradient_type: "radial",
      start_color: "#FFFF00",
      end_color: "#FF00FF",
      start_opacity: 0.0,
      end_opacity: 0.7,
      quality: 90
    }
  },
  {
    title: "暗角效果叠加",
    description: "添加暗角效果，突出中心区域",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-vignette.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-vignette.jpg",
    parameters: [
      { label: '叠加类型', value: '暗角' },
      { label: '强度', value: '80%' },
      { label: '半径', value: '1.2' }
    ],
    apiParams: {
      endpoint: "/api/v1/overlay",
      overlay_type: "vignette",
      vignette_intensity: 0.8,
      vignette_radius: 1.2,
      quality: 90
    }
  },
  {
    title: "边框叠加",
    description: "添加边框叠加效果，增强图片边界",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-border.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-border.jpg",
    parameters: [
      { label: '叠加类型', value: '边框' },
      { label: '宽度', value: '20px' },
      { label: '样式', value: 'solid' }
    ],
    apiParams: {
      endpoint: "/api/v1/overlay",
      overlay_type: "border",
      border_width: 20,
      border_color: "#000000",
      border_style: "solid",
      quality: 90
    }
  },
  {
    title: "透明叠加",
    description: "添加半透明叠加效果，柔和过渡",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-transparent.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-transparent.jpg",
    parameters: [
      { label: '叠加类型', value: '渐变' },
      { label: '渐变类型', value: 'linear' },
      { label: '透明度', value: '30%' }
    ],
    apiParams: {
      endpoint: "/api/v1/overlay",
      overlay_type: "gradient",
      gradient_type: "linear",
      gradient_direction: "to_right",
      start_color: "#FFFFFF",
      end_color: "#000000",
      start_opacity: 0.3,
      end_opacity: 0.3,
      quality: 90
    }
  },
  {
    title: "混合叠加",
    description: "混合多种叠加效果，创造独特视觉",
    originalImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/original-mixed.jpg",
    processedImage: "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/overlay/overlay-mixed.jpg",
    parameters: [
      { label: '叠加类型', value: '渐变' },
      { label: '渐变类型', value: 'radial' },
      { label: '透明度', value: '80%' }
    ],
    apiParams: {
      endpoint: "/api/v1/overlay",
      overlay_type: "gradient",
      gradient_type: "radial",
      start_color: "#00FF00",
      end_color: "#FF0000",
      start_opacity: 0.2,
      end_opacity: 0.8,
      quality: 90
    }
  }
];
