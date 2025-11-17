import React, { useState, useEffect } from 'react';
import {
  Slider,
  Typography,
  Box,
  TextField,
  FormControlLabel,
  Checkbox,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

interface GifOptimizeSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const GifOptimizeSettingsComponent: React.FC<GifOptimizeSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [maxColors, setMaxColors] = useState(128);
  const [resizeFactor, setResizeFactor] = useState(1.0);
  const [targetFps, setTargetFps] = useState<number | null>(null);
  const [enableFpsOptimization, setEnableFpsOptimization] = useState(false);
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      max_colors: maxColors,
      resize_factor: resizeFactor,
      quality: quality,
    };

    if (enableFpsOptimization && targetFps) {
      settings.target_fps = targetFps;
    }

    onSettingsChange(settings);
  }, [maxColors, resizeFactor, targetFps, enableFpsOptimization, quality, onSettingsChange]);

  return (
    <Box sx={{ width: '100%' }}>
      {/* 基础优化设置 */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">基础优化设置</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>
              最大颜色数: {maxColors}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              减少颜色数量可以显著降低文件大小，但可能影响图像质量
            </Typography>
            <Slider
              value={maxColors}
              min={16}
              max={256}
              step={16}
              onChange={(_, value) => setMaxColors(value as number)}
              valueLabelDisplay="auto"
              disabled={isLoading}
              marks={[
                { value: 16, label: '16' },
                { value: 64, label: '64' },
                { value: 128, label: '128' },
                { value: 256, label: '256' },
              ]}
            />
          </Box>

          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>
              输出质量: {quality}%
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              调整输出质量，数值越高质量越好但文件越大
            </Typography>
            <Slider
              value={quality}
              min={10}
              max={100}
              step={5}
              onChange={(_, value) => setQuality(value as number)}
              valueLabelDisplay="auto"
              disabled={isLoading}
              marks={[
                { value: 10, label: '10%' },
                { value: 50, label: '50%' },
                { value: 90, label: '90%' },
                { value: 100, label: '100%' },
              ]}
            />
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* 尺寸优化设置 */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">尺寸优化</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>
              缩放比例: {(resizeFactor * 100).toFixed(0)}%
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              缩小尺寸可以大幅减少文件大小，1.0表示保持原始尺寸
            </Typography>
            <Slider
              value={resizeFactor}
              min={0.1}
              max={2.0}
              step={0.1}
              onChange={(_, value) => setResizeFactor(value as number)}
              valueLabelDisplay="auto"
              disabled={isLoading}
              marks={[
                { value: 0.5, label: '50%' },
                { value: 1.0, label: '100%' },
                { value: 1.5, label: '150%' },
                { value: 2.0, label: '200%' },
              ]}
            />
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* 帧率优化设置 */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">帧率优化</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <FormControlLabel
            control={
              <Checkbox
                checked={enableFpsOptimization}
                onChange={(e) => setEnableFpsOptimization(e.target.checked)}
                disabled={isLoading}
              />
            }
            label="启用帧率优化"
            sx={{ mb: 2 }}
          />
          
          {enableFpsOptimization && (
            <Box sx={{ mb: 3 }}>
              <Typography gutterBottom>
                目标帧率: {targetFps || 'auto'} FPS
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                降低帧率可以减少文件大小，但会影响动画流畅度
              </Typography>
              <Slider
                value={targetFps || 10}
                min={1}
                max={30}
                step={1}
                onChange={(_, value) => setTargetFps(value as number)}
                valueLabelDisplay="auto"
                disabled={isLoading}
                marks={[
                  { value: 5, label: '5fps' },
                  { value: 10, label: '10fps' },
                  { value: 15, label: '15fps' },
                  { value: 24, label: '24fps' },
                  { value: 30, label: '30fps' },
                ]}
              />
            </Box>
          )}
        </AccordionDetails>
      </Accordion>

      {/* 优化提示 */}
      <Box sx={{ mt: 3, p: 2, bgcolor: 'info.main', color: 'info.contrastText', borderRadius: 1 }}>
        <Typography variant="body2">
          💡 <strong>优化建议：</strong>
          <br />
          • 对于网页使用，建议颜色数64-128，缩放比例0.7-1.0
          <br />
          • 对于社交媒体，建议启用帧率优化，目标帧率10-15fps
          <br />
          • 文件过大时，优先调整缩放比例和颜色数
        </Typography>
      </Box>
    </Box>
  );
};

export default GifOptimizeSettingsComponent; 