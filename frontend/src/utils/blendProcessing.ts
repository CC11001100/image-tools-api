export const buildBlendFormData = (
  formData: FormData,
  baseFile: File | null,
  baseImageUrl: string | null,
  overlayFile: File | null,
  overlayImageUrl: string | null,
  overlayPreviewUrl: string | null,
  settings: any
) => {
  // 添加基础图片
  if (baseFile) {
    formData.append('base', baseFile);
  } else {
    formData.append('base_url', baseImageUrl || 'https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original-800px.jpg');
  }
  
  // 添加叠加图片
  if (overlayFile) {
    formData.append('overlay', overlayFile);
  } else {
    formData.append('overlay_url', overlayImageUrl || overlayPreviewUrl || '');
  }
  
  // 添加参数
  formData.append('blend_mode', settings.blend_mode);
  formData.append('opacity', settings.opacity.toString());
  formData.append('position', settings.position);
  formData.append('scale', settings.scale.toString());
  formData.append('quality', settings.quality.toString());
  
  if (settings.position === 'custom') {
    formData.append('x_offset', settings.x_offset.toString());
    formData.append('y_offset', settings.y_offset.toString());
  }
}; 