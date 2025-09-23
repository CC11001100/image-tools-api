import { FilterGroup } from './filterTypes';

// 滤镜分组配置
export const FILTER_GROUPS: FilterGroup[] = [
  {
    name: 'painting',
    label: '绘画风格',
    filters: ['oil_painting', 'watercolor', 'dry_brush', 'fresco'],
  },
  {
    name: 'sketch',
    label: '素描风格',
    filters: ['pencil_sketch', 'colored_pencil', 'cutout', 'poster_edges'],
  },
  {
    name: 'texture',
    label: '纹理风格',
    filters: ['rough_pastels'],
  },
]; 