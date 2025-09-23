import axios from 'axios';
import { API_BASE_URL } from '../config/constants';
import { FilterOption } from '../types/api';

export const fetchArtFilters = async (): Promise<FilterOption[]> => {
  const response = await axios.get(`${API_BASE_URL}/art-filter/list`);
  const filters = response.data.filters;
  return Object.entries(filters).map(([key, desc]) => ({
    value: key,
    label: key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
    description: desc as string,
    useCase: response.data.useCases?.[key],
  }));
};

export const buildArtFilterFormData = (formData: FormData, settings: any) => {
  formData.append('intensity', settings.intensity.toString());
  if (settings.params && settings.params !== '{}') {
    formData.append('params', settings.params);
  }
}; 