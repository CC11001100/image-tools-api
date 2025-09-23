import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Slider,
  FormControlLabel,
  Switch,
  Paper,
  Grid,
  Chip,
  Alert,
  Divider,
} from '@mui/material';
import {
  Speed as SpeedIcon,
  Loop as LoopIcon,
  Tune as TuneIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

interface GifCreationSettingsProps {
  onSettingsChange: (settings: any) => void;
  isLoading?: boolean;
  imageCount?: number;
}

const GifCreationSettings: React.FC<GifCreationSettingsProps> = ({
  onSettingsChange,
  isLoading = false,
  imageCount = 0,
}) => {
  const [duration, setDuration] = useState(500);
  const [loop, setLoop] = useState(0);
  const [optimize, setOptimize] = useState(true);

  useEffect(() => {
    onSettingsChange({
      duration,
      loop,
      optimize,
    });
  }, [duration, loop, optimize, onSettingsChange]);

  // 计算GIF预估信息
  const fps = Math.round(1000 / duration);
  const totalDuration = (imageCount * duration) / 1000;
  const loopText = loop === 0 ? '无限循环' : `${loop}次`;

  return (
    <Paper elevation={2} sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <TuneIcon sx={{ mr: 1, color: 'primary.main' }} />
        <Typography variant="h6">GIF 参数设置</Typography>
      </Box>

      {/* 预估信息 */}
      {imageCount > 0 && (
        <Alert severity="info" sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Chip
              icon={<InfoIcon />}
              label={`${imageCount} 张图片`}
              size="small"
              variant="outlined"
            />
            <Chip
              icon={<SpeedIcon />}
              label={`${fps} FPS`}
              size="small"
              variant="outlined"
            />
            <Chip
              icon={<LoopIcon />}
              label={loopText}
              size="small"
              variant="outlined"
            />
            <Chip
              label={`时长 ${totalDuration.toFixed(1)}秒`}
              size="small"
              variant="outlined"
            />
          </Box>
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* 帧间隔设置 */}
        <Grid item xs={12}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              帧间隔时间
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              控制每一帧显示的持续时间，数值越小动画越快
            </Typography>
          </Box>
          
          <Box sx={{ px: 2 }}>
            <Typography gutterBottom>
              {duration}ms ({fps} FPS)
            </Typography>
            <Slider
              value={duration}
              min={50}
              max={2000}
              step={50}
              onChange={(_, value) => setDuration(value as number)}
              disabled={isLoading}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => `${value}ms`}
              marks={[
                { value: 50, label: '50ms\n(20fps)' },
                { value: 100, label: '100ms\n(10fps)' },
                { value: 200, label: '200ms\n(5fps)' },
                { value: 500, label: '500ms\n(2fps)' },
                { value: 1000, label: '1000ms\n(1fps)' },
                { value: 2000, label: '2000ms\n(0.5fps)' },
              ]}
              sx={{
                '& .MuiSlider-markLabel': {
                  fontSize: '0.75rem',
                  textAlign: 'center',
                  whiteSpace: 'pre-line',
                },
              }}
            />
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Divider sx={{ my: 2 }} />
        </Grid>

        {/* 循环次数设置 */}
        <Grid item xs={12}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              循环次数
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              设置GIF播放的循环次数，0表示无限循环
            </Typography>
          </Box>
          
          <Box sx={{ px: 2 }}>
            <Typography gutterBottom>
              {loop === 0 ? '无限循环' : `${loop} 次`}
            </Typography>
            <Slider
              value={loop}
              min={0}
              max={10}
              step={1}
              onChange={(_, value) => setLoop(value as number)}
              disabled={isLoading}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => value === 0 ? '无限' : `${value}次`}
              marks={[
                { value: 0, label: '无限' },
                { value: 1, label: '1次' },
                { value: 3, label: '3次' },
                { value: 5, label: '5次' },
                { value: 10, label: '10次' },
              ]}
            />
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Divider sx={{ my: 2 }} />
        </Grid>

        {/* 优化选项 */}
        <Grid item xs={12}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              输出优化
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              优化GIF文件大小，减少不必要的颜色信息
            </Typography>
          </Box>
          
          <FormControlLabel
            control={
              <Switch
                checked={optimize}
                onChange={(e) => setOptimize(e.target.checked)}
                disabled={isLoading}
                color="primary"
              />
            }
            label="启用文件优化"
          />
        </Grid>
      </Grid>

      {/* 使用提示 */}
      <Alert severity="warning" sx={{ mt: 3 }}>
        <Typography variant="body2">
          <strong>提示：</strong>
          <br />
          • 图片数量较多时，建议设置较大的帧间隔以避免文件过大
          <br />
          • 启用优化可以显著减少文件大小，但可能会轻微影响画质
          <br />
          • 建议先用较少图片测试参数，确认效果后再处理大量图片
        </Typography>
      </Alert>
    </Paper>
  );
};

export default GifCreationSettings; 