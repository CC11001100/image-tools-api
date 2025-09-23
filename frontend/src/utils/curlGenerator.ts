import { API_BASE_URL } from '../config/constants';

interface CurlGeneratorOptions {
  endpoint: string;
  isUrlMode?: boolean;
  parameters?: Record<string, any>;
  fileFieldName?: string;
  urlFieldName?: string;
}

export const generateCurlCommand = ({
  endpoint,
  isUrlMode = false,
  parameters = {},
  fileFieldName = 'file',
  urlFieldName = 'image_url',
}: CurlGeneratorOptions): string => {
  let curl = `curl -X POST "${API_BASE_URL}${endpoint}"`;
  
  if (isUrlMode) {
    curl += ` \\\n  -F "${urlFieldName}=https://example.com/image.jpg"`;
  } else {
    curl += ` \\\n  -F "${fileFieldName}=@your_image.jpg"`;
  }
  
  // 添加其他参数
  Object.entries(parameters).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      curl += ` \\\n  -F "${key}=${value}"`;
    }
  });
  
  return curl;
};

export const generateTransformCurlCommand = (
  transformType: string,
  settings: any,
  isUrlMode: boolean = false
): string => {
  const endpoint = transformType === 'rotate' 
    ? `/transform/rotate${isUrlMode ? '-url' : ''}`
    : `/transform/${transformType}${isUrlMode ? '-url' : ''}`;
  
  const parameters: Record<string, any> = {
    quality: settings.quality,
  };
  
  if (transformType === 'rotate') {
    parameters.angle = settings.angle;
    parameters.expand = settings.expand;
    parameters.fill_color = settings.fill_color;
  }
  
  return generateCurlCommand({
    endpoint,
    isUrlMode,
    parameters,
  });
}; 