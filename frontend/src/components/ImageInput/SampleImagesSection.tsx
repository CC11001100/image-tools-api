import React from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Chip,
} from '@mui/material';
import { sampleImageCategories, getSampleImagesByCategory, type SampleImageUrl } from '../../config/sampleImageUrls';

interface SampleImagesSectionProps {
  showSampleUrls: boolean;
  selectedCategory: string;
  onToggleSampleUrls: () => void;
  onCategoryChange: (category: string) => void;
  onSampleUrlSelect: (sampleUrl: SampleImageUrl) => void;
}

export const SampleImagesSection: React.FC<SampleImagesSectionProps> = ({
  showSampleUrls,
  selectedCategory,
  onToggleSampleUrls,
  onCategoryChange,
  onSampleUrlSelect,
}) => {
  return (
    <Box sx={{ mt: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="subtitle2" color="text.secondary">
          或选择示例图片快速测试：
        </Typography>
        <Button
          size="small"
          variant="outlined"
          onClick={onToggleSampleUrls}
        >
          {showSampleUrls ? '收起' : '选择示例'}
        </Button>
      </Box>

      {showSampleUrls && (
        <Paper elevation={1} sx={{ p: 2, bgcolor: 'grey.50' }}>
          {/* 分类选择 */}
          <Box sx={{ mb: 2 }}>
            <Typography variant="caption" color="text.secondary" gutterBottom>
              选择分类：
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {sampleImageCategories.map((category) => (
                <Chip
                  key={category}
                  label={category}
                  size="small"
                  clickable
                  color={selectedCategory === category ? 'primary' : 'default'}
                  variant={selectedCategory === category ? 'filled' : 'outlined'}
                  onClick={() => onCategoryChange(category)}
                />
              ))}
            </Box>
          </Box>

          {/* 示例图片选择 */}
          <Box sx={{ maxHeight: 300, overflowY: 'auto' }}>
            {getSampleImagesByCategory(selectedCategory).map((sampleUrl, index) => (
              <Box
                key={index}
                sx={{
                  p: 1,
                  mb: 1,
                  border: 1,
                  borderColor: 'grey.300',
                  borderRadius: 1,
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  '&:hover': {
                    borderColor: 'primary.main',
                    bgcolor: 'primary.50'
                  }
                }}
                onClick={() => onSampleUrlSelect(sampleUrl)}
              >
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="body2" fontWeight="medium">
                      {sampleUrl.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {sampleUrl.description}
                    </Typography>
                    {sampleUrl.size && (
                      <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
                        ({sampleUrl.size})
                      </Typography>
                    )}
                  </Box>
                  <Chip label={sampleUrl.category} size="small" variant="outlined" />
                </Box>
              </Box>
            ))}
          </Box>
        </Paper>
      )}
    </Box>
  );
};
