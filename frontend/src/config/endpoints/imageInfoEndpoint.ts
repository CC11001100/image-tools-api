import { ApiEndpoint } from '../../types/api';

export const imageInfoEndpoint: ApiEndpoint = {
  method: 'POST',
  path: '/api/v1/image-info',
  urlPath: '/api/v1/image-info-by-url',
  description: '图片信息查询',
  category: 'analysis',
  requestType: {
    file: 'multipart/form-data',
    url: 'application/json'
  },
  responseType: 'application/json',
  parameters: []
};
