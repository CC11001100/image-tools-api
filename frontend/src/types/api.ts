export interface ApiParameter {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'select' | 'file' | 'color';
  description: string;
  required?: boolean;
  defaultValue?: any;
  options?: string[];
  min?: number;
  max?: number;
  step?: number;
}

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
  parameters?: ApiParameter[];
}

export interface EffectExample {
  title: string;
  description: string;
  originalImage: string;
  processedImage: string;
  parameters: Array<{
    label: string;
    value: string;
  }>;
  apiParams: {
    endpoint: string;
    [key: string]: any;
  };
  imageDimensions?: {
    original?: {
      width: number;
      height: number;
    };
    processed?: {
      width: number;
      height: number;
    };
  };
}

// 扩展类型，支持多张原图（用于拼接等功能）
export interface MultiImageEffectExample extends Omit<EffectExample, 'originalImage'> {
  originalImages: string[];  // 多张原图URL数组
  originalImageLabels?: string[];  // 原图标签数组（可选）
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface ApiDocumentationProps {
  endpoint: ApiEndpoint;
  settings?: Record<string, any>;
}

export interface ApiTabEndpoint {
  label: string;
  component: React.ComponentType<ApiDocumentationProps>;
  componentProps: {
    endpoint: ApiEndpoint;
    settings?: Record<string, any>;
  };
}

export interface FilterOption {
  value: string;
  label: string;
  description: string;
  category?: string;
  parameters?: {
    [key: string]: {
      type: string;
      default?: any;
      min?: number;
      max?: number;
      step?: number;
    };
  };
} 