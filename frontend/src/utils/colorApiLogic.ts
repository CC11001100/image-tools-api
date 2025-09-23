import { ColorSettings } from '../types/settings';

export const getColorApiPath = () => {
  return '/api/v1/color-by-url';
};

export const buildColorFormData = (formData: FormData, settings: ColorSettings) => {
  formData.append('quality', settings.quality.toString());
  formData.append('adjustment_type', settings.adjustment_type);

  // 根据不同的调整类型添加相应参数
  switch (settings.adjustment_type) {
    case 'hsl':
      formData.append('hue_shift', settings.hue_shift?.toString() || '0');
      formData.append('saturation_scale', settings.saturation_scale?.toString() || '1');
      formData.append('lightness_scale', settings.lightness_scale?.toString() || '1');
      break;
    case 'balance':
      formData.append('shadows_cyan_red', settings.shadows_cyan_red?.toString() || '0');
      formData.append('shadows_magenta_green', settings.shadows_magenta_green?.toString() || '0');
      formData.append('shadows_yellow_blue', settings.shadows_yellow_blue?.toString() || '0');
      break;
    case 'levels':
      formData.append('black_point', settings.black_point?.toString() || '0');
      formData.append('white_point', settings.white_point?.toString() || '255');
      formData.append('gamma', settings.gamma?.toString() || '1');
      break;
    case 'temperature':
      formData.append('temperature', settings.temperature?.toString() || '0');
      formData.append('tint', settings.tint?.toString() || '0');
      break;
    case 'duotone':
      formData.append('highlight_color', settings.highlight_color || '#ffffff');
      formData.append('shadow_color', settings.shadow_color || '#000000');
      break;
  }
};

export const buildColorJsonData = (imageUrl: string, settings: ColorSettings) => {
  const data: any = {
    image_url: imageUrl,
    quality: settings.quality,
    adjustment_type: settings.adjustment_type,
  };

  // 根据不同的调整类型添加相应参数
  switch (settings.adjustment_type) {
    case 'hsl':
      data.hue_shift = settings.hue_shift || 0;
      data.saturation_scale = settings.saturation_scale || 1;
      data.lightness_scale = settings.lightness_scale || 1;
      break;
    case 'balance':
      data.red_bias = settings.shadows_cyan_red || 0;
      data.green_bias = settings.shadows_magenta_green || 0;
      data.blue_bias = settings.shadows_yellow_blue || 0;
      break;
    case 'levels':
      data.black_point = settings.black_point || 0;
      data.white_point = settings.white_point || 255;
      data.gamma = settings.gamma || 1;
      break;
    case 'temperature':
      data.temperature = settings.temperature || 0;
      data.tint = settings.tint || 0;
      break;
    case 'duotone':
      data.highlight_color = settings.highlight_color || '#ffffff';
      data.shadow_color = settings.shadow_color || '#000000';
      break;
  }

  return data;
};

export const getColorCurlParams = (settings: ColorSettings) => {
  const customParams = [`quality=${settings.quality}`];
  customParams.push(`adjustment_type=${settings.adjustment_type}`);
  
  // 添加特定参数
  switch (settings.adjustment_type) {
    case 'hsl':
      customParams.push(`hue_shift=${settings.hue_shift || 0}`);
      customParams.push(`saturation_scale=${settings.saturation_scale || 1}`);
      customParams.push(`lightness_scale=${settings.lightness_scale || 1}`);
      break;
    case 'balance':
      customParams.push(`shadows_cyan_red=${settings.shadows_cyan_red || 0}`);
      customParams.push(`shadows_magenta_green=${settings.shadows_magenta_green || 0}`);
      customParams.push(`shadows_yellow_blue=${settings.shadows_yellow_blue || 0}`);
      break;
    case 'levels':
      customParams.push(`black_point=${settings.black_point || 0}`);
      customParams.push(`white_point=${settings.white_point || 255}`);
      customParams.push(`gamma=${settings.gamma || 1}`);
      break;
    case 'temperature':
      customParams.push(`temperature=${settings.temperature || 0}`);
      customParams.push(`tint=${settings.tint || 0}`);
      break;
    case 'duotone':
      customParams.push(`highlight_color=${settings.highlight_color || '#ffffff'}`);
      customParams.push(`shadow_color=${settings.shadow_color || '#000000'}`);
      break;
  }
  
  return customParams;
}; 