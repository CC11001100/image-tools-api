import React, { useEffect, useRef } from 'react';
import {
  Dialog,
  DialogContent,
  TextField,
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
  InputAdornment,
  Fade,
} from '@mui/material';
import {
  Search as SearchIcon,
  KeyboardArrowDown as ArrowDownIcon,
  KeyboardArrowUp as ArrowUpIcon,
  KeyboardReturn as EnterIcon,
} from '@mui/icons-material';
import { useSearch } from '../contexts/SearchContext';

const GlobalSearch: React.FC = () => {
  const {
    isOpen,
    query,
    results,
    isLoading,
    selectedIndex,
    closeSearch,
    setQuery,
    selectResult,
    executeSelected,
  } = useSearch();

  const inputRef = useRef<HTMLInputElement>(null);

  // 当搜索框打开时自动聚焦
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // 获取类型标签颜色
  const getTypeColor = (type: string) => {
    switch (type) {
      case 'page':
        return 'primary';
      case 'api':
        return 'secondary';
      case 'feature':
        return 'success';
      default:
        return 'default';
    }
  };

  // 获取类型标签文本
  const getTypeText = (type: string) => {
    switch (type) {
      case 'page':
        return '页面';
      case 'api':
        return 'API';
      case 'feature':
        return '功能';
      default:
        return '其他';
    }
  };

  // 高亮搜索关键词
  const highlightText = (text: string, searchQuery: string) => {
    if (!searchQuery.trim()) return text;
    
    const regex = new RegExp(`(${searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    const parts = text.split(regex);
    
    return (
      <>
        {parts.map((part, index) => 
          regex.test(part) ? (
            <span key={index} style={{ backgroundColor: '#fff3cd', fontWeight: 'bold' }}>
              {part}
            </span>
          ) : (
            part
          )
        )}
      </>
    );
  };

  return (
    <Dialog
      open={isOpen}
      onClose={closeSearch}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 2,
          maxHeight: '80vh',
          position: 'relative',
          top: '-10vh', // 向上偏移一些
        },
      }}
    >
      <DialogContent sx={{ p: 0 }}>
        <Box sx={{ p: 3, pb: 2 }}>
          <TextField
            ref={inputRef}
            fullWidth
            placeholder="搜索功能、页面或API文档..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            variant="outlined"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ color: 'text.secondary' }} />
                </InputAdornment>
              ),
              endAdornment: isLoading ? (
                <InputAdornment position="end">
                  <CircularProgress size={20} />
                </InputAdornment>
              ) : null,
              sx: {
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                },
              },
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                fontSize: '1.1rem',
              },
            }}
          />
        </Box>

        {/* 搜索结果 */}
        <Box sx={{ maxHeight: '60vh', overflow: 'auto' }}>
          {query.trim() === '' ? (
            <Box sx={{ p: 3, textAlign: 'center', color: 'text.secondary' }}>
              <Typography variant="body2" sx={{ mb: 2 }}>
                开始输入以搜索功能、页面或API文档
              </Typography>
              <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, flexWrap: 'wrap' }}>
                <Chip size="small" label="Ctrl+K 快速打开" variant="outlined" />
                <Chip size="small" label="↑↓ 选择" variant="outlined" />
                <Chip size="small" label="回车 确认" variant="outlined" />
              </Box>
            </Box>
          ) : results.length === 0 && !isLoading ? (
            <Box sx={{ p: 3, textAlign: 'center', color: 'text.secondary' }}>
              <Typography variant="body2">
                未找到相关结果，请尝试其他关键词
              </Typography>
            </Box>
          ) : (
            <List sx={{ pt: 0 }}>
              {results.map((result, index) => (
                <Fade key={result.id} in timeout={200 + index * 50}>
                  <ListItem
                    button
                    selected={index === selectedIndex}
                    onClick={() => {
                      selectResult(index);
                      executeSelected();
                    }}
                    onMouseEnter={() => selectResult(index)}
                    sx={{
                      py: 2,
                      px: 3,
                      cursor: 'pointer',
                      '&.Mui-selected': {
                        backgroundColor: 'primary.light',
                        color: 'primary.contrastText',
                        '&:hover': {
                          backgroundColor: 'primary.main',
                        },
                      },
                      '&:hover': {
                        backgroundColor: 'action.hover',
                      },
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                          <Typography
                            variant="subtitle1"
                            sx={{
                              fontWeight: index === selectedIndex ? 600 : 500,
                              color: index === selectedIndex ? 'inherit' : 'text.primary',
                            }}
                          >
                            {highlightText(result.title, query)}
                          </Typography>
                          <Chip
                            size="small"
                            label={getTypeText(result.type)}
                            color={getTypeColor(result.type) as any}
                            sx={{ fontSize: '0.7rem', height: '20px' }}
                          />
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography
                            variant="body2"
                            sx={{
                              color: index === selectedIndex ? 'inherit' : 'text.secondary',
                              opacity: index === selectedIndex ? 0.9 : 0.7,
                              mb: 0.5,
                            }}
                          >
                            {highlightText(result.description, query)}
                          </Typography>
                          <Typography
                            variant="caption"
                            sx={{
                              color: index === selectedIndex ? 'inherit' : 'text.secondary',
                              opacity: index === selectedIndex ? 0.8 : 0.6,
                            }}
                          >
                            {result.category}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                </Fade>
              ))}
            </List>
          )}
        </Box>

        {/* 底部快捷键提示 */}
        {results.length > 0 && (
          <Box
            sx={{
              p: 2,
              borderTop: 1,
              borderColor: 'divider',
              backgroundColor: 'grey.50',
              display: 'flex',
              justifyContent: 'center',
              gap: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <ArrowUpIcon fontSize="small" sx={{ color: 'text.secondary' }} />
              <ArrowDownIcon fontSize="small" sx={{ color: 'text.secondary' }} />
              <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                选择
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <EnterIcon fontSize="small" sx={{ color: 'text.secondary' }} />
              <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                确认
              </Typography>
            </Box>
          </Box>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default GlobalSearch; 