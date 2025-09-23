import { FilterOption } from '../types/api';

export interface FilterParameter {
  name: string;
  label: string;
  type: 'slider' | 'color' | 'select' | 'number';
  min?: number;
  max?: number;
  step?: number;
  options?: { value: string | number; label: string }[];
  defaultValue: any;
}

export interface FilterGroup {
  name: string;
  label: string;
  filters: string[];
} 