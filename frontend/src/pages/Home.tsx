import React from 'react';
import { 
  Typography, 
  Paper, 
  Grid, 
  Box, 
  Button,
  Divider,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { featureGroups } from '../config/homeFeatures';
import { FeatureCard } from '../components/Home/FeatureCard';
import { HeroBanner } from '../components/Home/HeroBanner';

const Home: React.FC = () => {
  return (
    <>
      <HeroBanner />

      {featureGroups.map((group) => (
        <Box key={group.title} sx={{ mb: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
            {group.title}
          </Typography>
          <Divider sx={{ mb: 3 }} />
          <Grid container spacing={3}>
            {group.features.map((feature) => (
              <Grid item key={feature.title} xs={12} sm={6} md={3}>
                <FeatureCard feature={feature} />
              </Grid>
            ))}
          </Grid>
        </Box>
      ))}

      <Paper sx={{ p: 3, mt: 6, backgroundColor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          快速开始
        </Typography>
        <Typography variant="body2" paragraph>
          1. 选择您需要的功能 → 2. 上传图片 → 3. 调整参数 → 4. 下载处理后的图片
        </Typography>
        <Button
          component={RouterLink}
          to="/api-docs"
          variant="outlined"
          sx={{ mt: 1 }}
        >
          查看API文档
        </Button>
      </Paper>

      {/* 扫码加群提示 */}
      <Paper sx={{ p: 4, mt: 4, backgroundColor: '#f8f9fa', border: '1px solid #e9ecef' }}>
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h6" gutterBottom color="primary">
            没有找到想要的功能？
          </Typography>
          <Typography variant="body1" paragraph sx={{ mb: 3 }}>
            扫码加入微信群，向产品经理反馈您的需求，我们会加急开发您需要的功能！
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <img
              src="https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/common/wechat-group-qr.png"
              alt="微信群二维码"
              style={{
                width: '400px',
                height: '400px',
                border: '2px solid #ddd',
                borderRadius: '8px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
              }}
            />
          </Box>
          <Typography variant="body2" sx={{ mt: 2, color: 'text.secondary' }}>
            扫描二维码加入AI交流群
          </Typography>
        </Box>
      </Paper>
    </>
  );
};

export default Home; 