import { apiEndpoints } from '../config/apiEndpoints';
import { featureGroups } from '../config/homeFeatures';

export interface SearchItem {
  id: string;
  title: string;
  description: string;
  category: string;
  path?: string;
  type: 'page' | 'api' | 'feature';
  keywords: string[];
}

// 菜单数据结构（从Layout.tsx复制）
const menuItems = [
  { text: '首页', path: '/', category: '导航' },
  { text: '调整大小', path: '/resize', category: '基础编辑' },
  { text: '裁剪', path: '/crop', category: '基础编辑' },
  { text: '旋转翻转', path: '/transform', category: '基础编辑' },
  { text: '画布调整', path: '/canvas', category: '基础编辑' },
  { text: '透视变换', path: '/perspective', category: '基础编辑' },
  { text: '基础滤镜', path: '/filter', category: '滤镜效果' },
  { text: '艺术滤镜', path: '/art-filter', category: '滤镜效果' },
  { text: '色彩调整', path: '/color', category: '滤镜效果' },
  { text: '图片增强', path: '/enhance', category: '滤镜效果' },
  { text: '图片噪点', path: '/noise', category: '滤镜效果' },
  { text: '马赛克', path: '/pixelate', category: '滤镜效果' },
  { text: '水印', path: '/watermark', category: '文字与标注' },
  { text: '文字添加', path: '/text', category: '文字与标注' },
  { text: '图片标注', path: '/annotation', category: '文字与标注' },
  { text: '图层混合', path: '/blend', category: '图像合成' },
  { text: '图片拼接', path: '/stitch', category: '图像合成' },
  { text: '图片叠加', path: '/overlay', category: '图像合成' },
  { text: '遮罩效果', path: '/mask', category: '图像合成' },
  { text: '格式转换', path: '/format', category: '格式转换' },
  { text: 'GIF 处理', path: '/gif', category: 'GIF处理' },
  { text: '图片合成GIF', path: '/create-gif', category: 'GIF处理' },
  { text: 'GIF拆图', path: '/extract-gif', category: 'GIF处理' },

  { text: 'API 文档', path: '/api-docs', category: '文档' },
];

// 构建搜索数据索引
export function buildSearchIndex(): SearchItem[] {
  const searchItems: SearchItem[] = [];

  // 添加导航菜单项
  menuItems.forEach(item => {
    searchItems.push({
      id: `page-${item.path}`,
      title: item.text,
      description: `${item.category} - ${item.text}功能页面`,
      category: item.category,
      path: item.path,
      type: 'page',
      keywords: [item.text, item.category, '功能', '图像处理']
    });
  });

  // 添加API端点
  apiEndpoints.forEach(endpoint => {
    searchItems.push({
      id: `api-${endpoint.path}`,
      title: endpoint.description,
      description: `${endpoint.method} ${endpoint.path} - ${endpoint.description}`,
      category: `API - ${endpoint.category}`,
      path: '/api-docs',
      type: 'api',
      keywords: [endpoint.description, endpoint.category, 'API', endpoint.method, endpoint.path]
    });
  });

  // 添加功能特性
  featureGroups.forEach(group => {
    group.features.forEach(feature => {
      searchItems.push({
        id: `feature-${feature.link}`,
        title: feature.title,
        description: feature.description,
        category: group.title,
        path: feature.link,
        type: 'feature',
        keywords: [feature.title, group.title, '功能', '图像处理', feature.description]
      });
    });
  });

  return searchItems;
}

// Fuse.js 搜索配置
export const fuseOptions = {
  // 设置搜索的字段
  keys: [
    {
      name: 'title',
      weight: 0.6  // 标题权重最高
    },
    {
      name: 'description',
      weight: 0.3
    },
    {
      name: 'category',
      weight: 0.05
    },
    {
      name: 'keywords',
      weight: 0.05
    }
  ],
  // 搜索配置
  threshold: 0.3,  // 匹配阈值，0表示精确匹配，1表示匹配任何内容
  distance: 100,   // 匹配距离
  includeScore: true,
  includeMatches: true,
  minMatchCharLength: 2,
  shouldSort: true,
  findAllMatches: false,
  useExtendedSearch: false
}; 