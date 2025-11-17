import React, { useState, useEffect } from 'react';
import {
  Slider,
  Typography,
  Box,
  FormControlLabel,
  Checkbox,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Alert,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

interface GifCreateSettingsComponentProps {
  onSettingsChange: (settings: any) => void;
  isLoading: boolean;
}

const GifCreateSettingsComponent: React.FC<GifCreateSettingsComponentProps> = ({
  onSettingsChange,
  isLoading,
}) => {
  const [duration, setDuration] = useState(500);
  const [loop, setLoop] = useState(0);
  const [optimize, setOptimize] = useState(true);
  const [quality, setQuality] = useState(90);

  useEffect(() => {
    const settings: any = {
      duration: duration,
      loop: loop,
      optimize: optimize,
      quality: quality,
    };

    onSettingsChange(settings);
  }, [duration, loop, optimize, quality, onSettingsChange]);

  const getFpsFromDuration = (duration: number) => {
    return Math.round(1000 / duration);
  };

  const getFileSizeEstimate = (duration: number, frameCount: number = 10) => {
    // 简单的文件大小估算
    const fps = getFpsFromDuration(duration);
    const baseSize = frameCount * 50; // 每帧约50KB
    const fpsMultiplier = fps / 10; // 基准10fps
    const qualityMultiplier = quality / 100;
    return Math.round(baseSize * fpsMultiplier * qualityMultiplier);
  };

  return (
    <Box sx={{ width: '100%' }}>
      {/* 动画设置 */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">动画设置</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>
              帧持续时间: {duration}ms ({getFpsFromDuration(duration)} FPS)
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              每帧显示的时间，数值越小动画越快
            </Typography>
            <Slider
              value={duration}
              min={50}
              max={2000}
              step={50}
              onChange={(_, value) => setDuration(value as number)}
              valueLabelDisplay="auto"
              disabled={isLoading}
              marks={[
                { value: 50, label: '50ms' },
                { value: 200, label: '200ms' },
                { value: 500, label: '500ms' },
                { value: 1000, label: '1s' },
                { value: 2000, label: '2s' },
              ]}
            />
            <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
              <Chip 
                label={`${getFpsFromDuration(duration)} FPS`} 
                size="small" 
                color="primary" 
                variant="outlined" 
              />
              <Chip 
                label={duration < 200 ? '快速' : duration < 800 ? '正常' : '缓慢'} 
                size="small" 
                color="secondary" 
                variant="outlined" 
              />
            </Box>
          </Box>

          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>
              循环次数: {loop === 0 ? '无限循环' : `${loop}次`}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              GIF播放的循环次数，0表示无限循环
            </Typography>
            <Slider
              value={loop}
              min={0}
              max={20}
              step={1}
              onChange={(_, value) => setLoop(value as number)}
              valueLabelDisplay="auto"
              disabled={isLoading}
              marks={[
                { value: 0, label: '∞' },
                { value: 1, label: '1' },
                { value: 5, label: '5' },
                { value: 10, label: '10' },
                { value: 20, label: '20' },
              ]}
            />
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* 质量设置 */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">质量设置</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>
              输出质量: {quality}%
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              影响最终GIF的图像质量和文件大小
            </Typography>
            <Slider
              value={quality}
              min={30}
              max={100}
              step={5}
              onChange={(_, value) => setQuality(value as number)}
              valueLabelDisplay="auto"
              disabled={isLoading}
              marks={[
                { value: 30, label: '30%' },
                { value: 60, label: '60%' },
                { value: 85, label: '85%' },
                { value: 100, label: '100%' },
              ]}
            />
          </Box>

          <FormControlLabel
            control={
              <Checkbox
                checked={optimize}
                onChange={(e) => setOptimize(e.target.checked)}
                disabled={isLoading}
              />
            }
            label="启用优化"
            sx={{ mb: 2 }}
          />
          <Typography variant="body2" color="text.secondary">
            启用后会自动优化颜色数量和压缩算法，减少文件大小
          </Typography>
        </AccordionDetails>
      </Accordion>

      {/* 预估信息 */}
      <Box sx={{ mt: 3, p: 2, bgcolor: 'info.main', color: 'info.contrastText', borderRadius: 1 }}>
        <Typography variant="body2">
          📊 <strong>预估信息：</strong>
          <br />
          • 帧率: {getFpsFromDuration(duration)} FPS
          <br />
          • 预估文件大小: ~{getFileSizeEstimate(duration)} KB
          <br />
          • 循环设置: {loop === 0 ? '无限循环' : `${loop}次循环`}
        </Typography>
      </Box>

      {/* 创建建议 */}
      <Alert severity="success" sx={{ mt: 2 }}>
        <Typography variant="body2">
          💡 <strong>创建建议：</strong>
          <br />
          • 网页使用: 200-500ms帧时间，启用优化
          <br />
          • 社交分享: 100-300ms帧时间，质量85%
          <br />
          • 高质量展示: 500-1000ms帧时间，质量100%
        </Typography>
      </Alert>

      {/* 功能特性标签 */}
      <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip label="自定义帧率" size="small" color="primary" variant="outlined" />
        <Chip label="循环控制" size="small" color="secondary" variant="outlined" />
        <Chip label="质量调节" size="small" color="info" variant="outlined" />
        <Chip label="自动优化" size="small" color="success" variant="outlined" />
      </Box>
    </Box>
  );
};

export default GifCreateSettingsComponent; 