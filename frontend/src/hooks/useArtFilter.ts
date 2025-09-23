import { useState, useEffect } from 'react';
import { FilterOption } from '../types/api';
import { FILTER_PARAMETERS } from '../config/filterConfig';
import axios from 'axios';

export const useArtFilter = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filterOptions, setFilterOptions] = useState<FilterOption[]>([]);
  const [selectedFilter, setSelectedFilter] = useState<string>('');
  const [currentTabIndex, setCurrentTabIndex] = useState<number>(0);
  const [intensity, setIntensity] = useState<number>(1.0);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [paramValues, setParamValues] = useState<{ [key: string]: any }>({});
  const [isLoadingFilters, setIsLoadingFilters] = useState<boolean>(true);

  // 加载可用的滤镜列表
  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const response = await axios.get('/art-filter/list');
        const filters = response.data.filters;
        const options: FilterOption[] = Object.entries(filters).map(([key, desc]) => ({
          value: key,
          label: key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
          description: desc as string,
        }));
        setFilterOptions(options);
        if (options.length > 0) {
          setSelectedFilter(options[0].value);
        }
      } catch (error) {
        console.error('Error fetching filters:', error);
      } finally {
        setIsLoadingFilters(false);
      }
    };

    fetchFilters();
  }, []);

  // 当选择新滤镜时重置参数值
  useEffect(() => {
    if (selectedFilter && FILTER_PARAMETERS[selectedFilter]) {
      const defaultParams: { [key: string]: any } = {};
      FILTER_PARAMETERS[selectedFilter].forEach(param => {
        defaultParams[param.name] = param.defaultValue;
      });
      setParamValues(defaultParams);
    }
  }, [selectedFilter]);

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setResultImage(null);
  };

  const handleFilterChange = (filterType: string) => {
    setSelectedFilter(filterType);
    setResultImage(null);
  };

  const handleParameterChange = (paramName: string, value: any) => {
    setParamValues(prev => ({
      ...prev,
      [paramName]: value,
    }));
  };

  const handleApplyFilter = async () => {
    if (!selectedFile || !selectedFilter) return;

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('intensity', intensity.toString());

      if (Object.keys(paramValues).length > 0) {
        const paramsJson = JSON.stringify(paramValues);
        formData.append('params', paramsJson);
      }

      const response = await axios.post(`/art-filter/${selectedFilter}`, formData, {
        responseType: 'blob',
      });

      const imageUrl = URL.createObjectURL(response.data);
      setResultImage(imageUrl);
    } catch (error) {
      console.error('Error applying filter:', error);
      alert('应用滤镜失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    selectedFile,
    filterOptions,
    selectedFilter,
    currentTabIndex,
    setCurrentTabIndex,
    intensity,
    setIntensity,
    resultImage,
    isLoading,
    paramValues,
    isLoadingFilters,
    handleImageSelected,
    handleFilterChange,
    handleParameterChange,
    handleApplyFilter,
  };
}; 