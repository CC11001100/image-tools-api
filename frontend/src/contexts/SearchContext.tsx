import React, { createContext, useContext, useState, useCallback, useMemo, useEffect } from 'react';
import Fuse from 'fuse.js';
import { buildSearchIndex, fuseOptions, SearchItem } from '../utils/searchData';

interface SearchContextType {
  isOpen: boolean;
  query: string;
  results: SearchItem[];
  isLoading: boolean;
  selectedIndex: number;
  openSearch: () => void;
  closeSearch: () => void;
  setQuery: (query: string) => void;
  selectNext: () => void;
  selectPrevious: () => void;
  selectResult: (index: number) => void;
  executeSelected: () => void;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

export const useSearch = () => {
  const context = useContext(SearchContext);
  if (!context) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
};

interface SearchProviderProps {
  children: React.ReactNode;
}

export const SearchProvider: React.FC<SearchProviderProps> = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQueryState] = useState('');
  const [results, setResults] = useState<SearchItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);

  // 创建Fuse搜索实例
  const fuse = useMemo(() => {
    const searchData = buildSearchIndex();
    return new Fuse(searchData, fuseOptions);
  }, []);

  // 防抖搜索函数
  const performSearch = useCallback(
    (searchQuery: string) => {
      setIsLoading(true);
      
      setTimeout(() => {
        if (searchQuery.trim() === '') {
          setResults([]);
        } else {
          const fuseResults = fuse.search(searchQuery);
          const searchResults = fuseResults.map(result => result.item);
          setResults(searchResults.slice(0, 10)); // 限制结果数量
        }
        setSelectedIndex(0);
        setIsLoading(false);
      }, 200); // 200ms 防抖延迟
    },
    [fuse]
  );

  // 更新搜索查询
  const setQuery = useCallback((newQuery: string) => {
    setQueryState(newQuery);
    performSearch(newQuery);
  }, [performSearch]);

  // 打开搜索
  const openSearch = useCallback(() => {
    setIsOpen(true);
  }, []);

  // 关闭搜索
  const closeSearch = useCallback(() => {
    setIsOpen(false);
    setQueryState('');
    setResults([]);
    setSelectedIndex(0);
  }, []);

  // 选择下一个结果
  const selectNext = useCallback(() => {
    setSelectedIndex(prev => (prev + 1) % Math.max(1, results.length));
  }, [results.length]);

  // 选择上一个结果
  const selectPrevious = useCallback(() => {
    setSelectedIndex(prev => (prev - 1 + results.length) % Math.max(1, results.length));
  }, [results.length]);

  // 选择特定结果
  const selectResult = useCallback((index: number) => {
    setSelectedIndex(index);
  }, []);

  // 执行选中的结果
  const executeSelected = useCallback(() => {
    if (results.length > 0 && selectedIndex < results.length) {
      const selectedResult = results[selectedIndex];
      if (selectedResult.path) {
        // 导航到选中的页面
        window.location.href = selectedResult.path;
        closeSearch();
      }
    }
  }, [results, selectedIndex, closeSearch]);

  // 键盘快捷键处理
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ctrl+K 或 Cmd+K 打开搜索
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        openSearch();
        return;
      }

      // 搜索框打开时的键盘导航
      if (isOpen) {
        switch (event.key) {
          case 'Escape':
            event.preventDefault();
            closeSearch();
            break;
          case 'ArrowDown':
            event.preventDefault();
            selectNext();
            break;
          case 'ArrowUp':
            event.preventDefault();
            selectPrevious();
            break;
          case 'Enter':
            event.preventDefault();
            executeSelected();
            break;
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, openSearch, closeSearch, selectNext, selectPrevious, executeSelected]);

  const value: SearchContextType = {
    isOpen,
    query,
    results,
    isLoading,
    selectedIndex,
    openSearch,
    closeSearch,
    setQuery,
    selectNext,
    selectPrevious,
    selectResult,
    executeSelected,
  };

  return (
    <SearchContext.Provider value={value}>
      {children}
    </SearchContext.Provider>
  );
}; 