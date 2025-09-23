import React from 'react';
import { Box } from '@mui/material';
import { ImageToolTabLayout } from '../components/ImageToolTabLayout';
import StitchSettingsComponent from '../components/settings/StitchSettingsComponent';
import { stitchExamples } from '../config/examples/stitchExamples';
import { stitchEndpoint } from '../config/endpoints/stitchEndpoint';

const StitchPage: React.FC = () => {
  return (
    <Box>
      <ImageToolTabLayout
        title="图片拼接"
        description="多张图片拼接处理，支持水平拼接、垂直拼接、网格拼接等多种拼接方式。可以调整图片间距和背景颜色。"
        endpoint={stitchEndpoint}
        settingsComponent={StitchSettingsComponent}
        effectExamples={stitchExamples}
        downloadFileName="stitched-image.jpg"
      />
    </Box>
  );
};

export default StitchPage; 