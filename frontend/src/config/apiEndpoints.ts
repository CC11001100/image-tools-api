import {
  basicEndpoints,
  imageProcessingEndpoints,
  geometryEndpoints,
  advancedEndpoints
} from './endpoints';

export interface ApiEndpoint {
  method: string;
  path: string;
  urlPath: string;
  description: string;
  category: string;
  requestType: {
    file: string;
    url: string;
  };
  responseType: string;
  parameters?: Array<{
    name: string;
    type: 'string' | 'number' | 'boolean' | 'select' | 'file' | 'color';
    required: boolean;
    description: string;
    defaultValue?: any;
    options?: string[];
    min?: number;
    max?: number;
  }>;
}

// API端点配置 - 20个端点（模块化）
export const apiEndpoints: ApiEndpoint[] = [
  ...basicEndpoints,
  ...imageProcessingEndpoints,
  ...geometryEndpoints,
  ...advancedEndpoints
];


// 按类别分组的端点
export const getGroupedEndpoints = () => {
  return apiEndpoints.reduce((acc, endpoint) => {
    if (!acc[endpoint.category]) {
      acc[endpoint.category] = [];
    }
    acc[endpoint.category].push(endpoint);
    return acc;
  }, {} as Record<string, ApiEndpoint[]>);
}; 