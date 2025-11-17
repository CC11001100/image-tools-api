import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Slider,
  Typography,
  Box,
  FormControlLabel,
  Checkbox,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

interface GifExtractSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const GifExtractSettingsComponent: React.FC<GifExtractSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [outputFormat, setOutputFormat] = useState('jpeg');
  const [quality, setQuality] = useState(90);
  const [extractAll, setExtractAll] = useState(true);
  const [frameRange, setFrameRange] = useState([0, 10]);
  const [skipFrames, setSkipFrames] = useState(1);

  useEffect(() => {
    const settings: any = {
      output_format: outputFormat,
      quality: quality,
      extract_all: extractAll,
    };

    if (!extractAll) {
      settings.start_frame = frameRange[0];
      settings.end_frame = frameRange[1];
      settings.skip_frames = skipFrames;
    }

    onSettingsChange(settings);
  }, [outputFormat, quality, extractAll, frameRange, skipFrames, onSettingsChange]);

  return (
    <Box sx={{ width: '100%' }}>
      {/* 基础设置 */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">输出设置</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 3 }}>
            <FormControl fullWidth>
              <InputLabel>输出格式</InputLabel>
              <Select
                value={outputFormat}
                label="输出格式"
                onChange={(e) => setOutputFormat(e.target.value)}
                disabled={isLoading}
              >
                <MenuItem value="jpeg">JPEG (更小文件)</MenuItem>
                <MenuItem value="png">PNG (透明支持)</MenuItem>
              </Select>
            </FormControl>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              JPEG适合照片类GIF，PNG适合有透明背景的GIF
            </Typography>
          </Box>

          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>
              输出质量: {quality}%
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              仅对JPEG格式有效，数值越高质量越好但文件越大
            </Typography>
            <Slider
              value={quality}
              min={10}
              max={100}
              step={5}
              onChange={(_, value) => setQuality(value as number)}
              valueLabelDisplay="auto"
              disabled={isLoading || outputFormat === 'png'}
              marks={[
                { value: 50, label: '50%' },
                { value: 75, label: '75%' },
                { value: 90, label: '90%' },
                { value: 100, label: '100%' },
              ]}
            />
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* 提取范围设置 */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">提取范围</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <FormControlLabel
            control={
              <Checkbox
                checked={extractAll}
                onChange={(e) => setExtractAll(e.target.checked)}
                disabled={isLoading}
              />
            }
            label="提取所有帧"
            sx={{ mb: 2 }}
          />

          {!extractAll && (
            <>
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>
                  帧范围: {frameRange[0]} - {frameRange[1]}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  选择要提取的帧范围（上传GIF后会自动调整最大值）
                </Typography>
                <Slider
                  value={frameRange}
                  min={0}
                  max={100}
                  onChange={(_, value) => setFrameRange(value as number[])}
                  valueLabelDisplay="auto"
                  disabled={isLoading}
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>
                  跳帧间隔: {skipFrames}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  每隔几帧提取一次，1表示连续提取，2表示每隔一帧提取
                </Typography>
                <Slider
                  value={skipFrames}
                  min={1}
                  max={10}
                  step={1}
                  onChange={(_, value) => setSkipFrames(value as number)}
                  valueLabelDisplay="auto"
                  disabled={isLoading}
                  marks={[
                    { value: 1, label: '1' },
                    { value: 3, label: '3' },
                    { value: 5, label: '5' },
                    { value: 10, label: '10' },
                  ]}
                />
              </Box>
            </>
          )}
        </AccordionDetails>
      </Accordion>

      {/* 提取提示 */}
      <Box sx={{ mt: 3, p: 2, bgcolor: 'success.main', color: 'success.contrastText', borderRadius: 1 }}>
        <Typography variant="body2">
          💡 <strong>提取建议：</strong>
          <br />
          • 大型GIF建议使用JPEG格式和适当的质量设置
          <br />
          • 需要保持透明效果的GIF请选择PNG格式
          <br />
          • 使用跳帧功能可以快速获取关键帧
        </Typography>
      </Box>

      {/* 功能特性标签 */}
      <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip label="批量提取" size="small" color="primary" variant="outlined" />
        <Chip label="格式选择" size="small" color="secondary" variant="outlined" />
        <Chip label="质量控制" size="small" color="info" variant="outlined" />
        <Chip label="范围选择" size="small" color="success" variant="outlined" />
      </Box>
    </Box>
  );
};

export default GifExtractSettingsComponent; 