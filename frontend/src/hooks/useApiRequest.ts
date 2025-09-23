import { API_BASE_URL, DEFAULT_SAMPLE_IMAGE } from '../config/constants';

export interface ApiRequestOptions {
  selectedFile: File | null;
  selectedImageUrl: string | null;
  previewUrl: string | null;
  settings: Record<string, any>;
  getApiPath: () => string;
  getUrlApiPath?: () => string;
  getFormData?: (formData: FormData, settings: Record<string, any>) => void;
  getJsonData?: (imageUrl: string, settings: Record<string, any>) => any;
  requestType?: {
    file: string;
    url: string;
  };
  onSuccess: (imageUrl: string) => void;
  onError: (error: string) => void;
  onLoadingChange: (loading: boolean) => void;
}

export const useApiRequest = () => {
  const processImage = async (options: ApiRequestOptions) => {
    console.log('🚀 useApiRequest.processImage 被调用');
    const {
      selectedFile,
      selectedImageUrl,
      previewUrl,
      settings,
      getApiPath,
      getUrlApiPath,
      getFormData,
      getJsonData,
      requestType,
      onSuccess,
      onError,
      onLoadingChange,
    } = options;

    console.log('📊 processImage 参数:', {
      hasFile: !!selectedFile,
      hasUrl: !!selectedImageUrl,
      hasPreview: !!previewUrl,
      settings
    });

    if (!selectedFile && !selectedImageUrl && !previewUrl) {
      console.log('❌ processImage: 没有图片源');
      onError('请先选择图片或使用示例图片');
      return;
    }

    console.log('🔄 设置loading状态为true');
    onLoadingChange(true);
    onError('');

    try {
      let apiPath: string;
      let requestBody: FormData | string;
      let headers: Record<string, string> = {};

      if (selectedFile) {
        console.log('📁 使用文件模式:', selectedFile.name);
        apiPath = getApiPath();

        // 文件模式总是使用FormData
        const formData = new FormData();
        formData.append('file', selectedFile);

        // 允许自定义FormData的构建
        if (getFormData) {
          console.log('⚙️ 执行自定义FormData构建');
          getFormData(formData, settings);
        }

        requestBody = formData;

        // 显示FormData内容（用于调试）
        console.log('📦 FormData内容:');
        Array.from(formData.entries()).forEach(([key, value]) => {
          console.log(`  ${key}:`, value);
        });
      } else {
        const urlToUse = selectedImageUrl || previewUrl || DEFAULT_SAMPLE_IMAGE;
        console.log('🔗 使用URL模式:', urlToUse);

        // 优先使用getUrlApiPath，如果没有则在原路径后添加-url后缀
        if (getUrlApiPath) {
          apiPath = getUrlApiPath();
        } else {
          apiPath = getApiPath();
          if (!apiPath.endsWith('-url') && !apiPath.endsWith('-by-url')) {
            apiPath = apiPath + '-url';
          }
        }

        // 检查URL模式的请求类型
        const urlRequestType = requestType?.url || 'multipart/form-data';
        console.log('🔍 URL请求类型:', urlRequestType);

        if (urlRequestType === 'application/json') {
          // JSON格式请求
          let jsonData;
          if (getJsonData) {
            console.log('⚙️ 使用自定义JSON构建函数');
            jsonData = getJsonData(urlToUse, settings);
          } else {
            jsonData = {
              image_url: urlToUse,
              ...settings
            };
          }
          requestBody = JSON.stringify(jsonData);
          headers['Content-Type'] = 'application/json';

          console.log('📦 JSON请求内容:', jsonData);
        } else {
          // FormData格式请求
          const formData = new FormData();
          formData.append('image_url', urlToUse);

          // 允许自定义FormData的构建
          if (getFormData) {
            console.log('⚙️ 执行自定义FormData构建');
            getFormData(formData, settings);
          }

          requestBody = formData;

          // 显示FormData内容（用于调试）
          console.log('📦 FormData内容:');
          Array.from(formData.entries()).forEach(([key, value]) => {
            console.log(`  ${key}:`, value);
          });
        }
      }

      console.log('🎯 最终API路径:', apiPath);

      const fullUrl = `${API_BASE_URL}${apiPath}`;
      console.log('🌐 发送请求到:', fullUrl);

      const response = await fetch(fullUrl, {
        method: 'POST',
        headers,
        body: requestBody,
      });

      console.log('📡 收到响应:', response.status, response.statusText);

      if (response.ok) {
        console.log('✅ 响应成功');
        const contentType = response.headers.get('content-type');
        console.log('📄 内容类型:', contentType);
        if (contentType?.includes('image')) {
          console.log('🖼️ 处理图片响应...');
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          console.log('🎉 图片处理成功，URL:', url);
          onSuccess(url);
        } else {
          console.log('❌ 不是图片格式');
          onError('服务器返回了非图片格式的数据');
        }
      } else {
        console.log('❌ 响应失败:', response.status);
        const errorText = await response.text();
        console.log('💬 错误信息:', errorText);
        onError(`处理失败: ${errorText}`);
      }
    } catch (error) {
      console.error('💥 发生异常:', error);
      onError('网络错误或服务器异常');
    } finally {
      console.log('🏁 设置loading状态为false');
      onLoadingChange(false);
    }
  };

  const generateCurlCommand = (
    apiPath: string,
    settings: any,
    isUrlMode: boolean = false,
    customParams: string[] = []
  ): string => {
    let curl = `curl -X POST "${API_BASE_URL}${apiPath}"`;
    
    if (isUrlMode) {
      curl += ` \\\n  -F "image_url=https://example.com/image.jpg"`;
    } else {
      curl += ` \\\n  -F "file=@your_image.jpg"`;
    }

    // 添加自定义参数
    customParams.forEach(param => {
      curl += ` \\\n  -F "${param}"`;
    });

    return curl;
  };

  return {
    processImage,
    generateCurlCommand,
  };
}; 