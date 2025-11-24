/**
 * 计费说明组件
 * 展示API的计费标准和Token计算器链接
 */

import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Link,
  Button,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CalculateIcon from '@mui/icons-material/Calculate';
import InfoIcon from '@mui/icons-material/Info';

interface BillingInfoProps {
  /** 计费类型: 'upload' | 'url' | 'dual' | 'mixed' */
  billingType?: 'upload' | 'url' | 'dual' | 'mixed';
  /** 是否默认展开 */
  defaultExpanded?: boolean;
  /** 是否显示为卡片形式 */
  asCard?: boolean;
}

export const BillingInfo: React.FC<BillingInfoProps> = ({
  billingType = 'upload',
  defaultExpanded = false,
  asCard = false,
}) => {
  
  // 计费类型说明
  const billingTypeInfo = {
    upload: {
      name: '类型A - 仅上传文件',
      formula: '100 + 50 × (主文件MB) + 50 × (结果文件MB)',
      example: '1MB文件处理 = 100 + 50 + 50 = 200 Token',
      description: '用户直接上传图片进行处理',
    },
    url: {
      name: '类型B - URL下载',
      formula: '100 + 100 × (下载文件MB) + 50 × (结果文件MB)',
      example: '下载2MB处理成1MB = 100 + 200 + 50 = 350 Token',
      description: '用户提供图片URL进行处理',
    },
    dual: {
      name: '类型C - 双文件上传',
      formula: '100 + 50 × (主文件MB) + 50 × (辅助文件MB) + 50 × (结果文件MB)',
      example: '1MB主文件 + 512KB辅助文件 = 100 + 50 + 25 + 50 = 225 Token',
      description: '需要上传两个文件进行处理（如图片水印）',
    },
    mixed: {
      name: '类型D - 混合模式',
      formula: '100 + 100 × (下载MB) + 50 × (上传MB) + 50 × (结果MB)',
      example: '下载2MB + 上传1MB = 100 + 200 + 50 + 50 = 400 Token',
      description: 'URL下载 + 文件上传的组合处理',
    },
  };

  const currentBillingInfo = billingTypeInfo[billingType];

  const content = (
    <Box>
      {/* 计费概览 */}
      <Alert 
        severity="info" 
        icon={<InfoIcon />}
        sx={{ mb: 3 }}
        action={
          <Button
            size="small"
            startIcon={<CalculateIcon />}
            href="https://token-calc.aigchub.vip/"
            target="_blank"
            rel="noopener noreferrer"
            sx={{ whiteSpace: 'nowrap' }}
          >
            Token计算器
          </Button>
        }
      >
        <Typography variant="body2">
          <strong>本接口需要消耗Token</strong>，费用根据文件大小自动计算。
          使用 <Link href="https://token-calc.aigchub.vip/" target="_blank" rel="noopener noreferrer">Token计算器</Link> 可快速估算成本。
        </Typography>
      </Alert>

      {/* 基础费用结构 */}
      <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
        💰 计费标准
      </Typography>
      
      <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>费用类型</strong></TableCell>
              <TableCell><strong>费率</strong></TableCell>
              <TableCell><strong>说明</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>基础调用费用</TableCell>
              <TableCell><Chip label="100 Token/次" color="primary" size="small" /></TableCell>
              <TableCell>每次API调用的固定费用</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>URL下载费用</TableCell>
              <TableCell><Chip label="100 Token/MB" color="warning" size="small" /></TableCell>
              <TableCell>从URL下载图片的费用</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>文件上传费用</TableCell>
              <TableCell><Chip label="50 Token/MB" color="success" size="small" /></TableCell>
              <TableCell>上传处理后图片的费用</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>最小计费单位</TableCell>
              <TableCell><Chip label="1 KB" size="small" /></TableCell>
              <TableCell>不足1KB按1KB计算</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      {/* 当前接口计费模式 */}
      <Box sx={{ mb: 3, p: 2, bgcolor: 'primary.50', borderRadius: 1, border: '1px solid', borderColor: 'primary.200' }}>
        <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
          📊 本接口计费模式
        </Typography>
        <Typography variant="body2" gutterBottom>
          <strong>{currentBillingInfo.name}</strong>
        </Typography>
        <Typography variant="body2" gutterBottom color="text.secondary">
          {currentBillingInfo.description}
        </Typography>
        <Box sx={{ mt: 1, p: 1.5, bgcolor: 'white', borderRadius: 1 }}>
          <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
            <strong>计费公式：</strong> {currentBillingInfo.formula}
          </Typography>
          <Typography variant="body2" sx={{ mt: 1, fontFamily: 'monospace', color: 'success.main' }}>
            <strong>示例：</strong> {currentBillingInfo.example}
          </Typography>
        </Box>
      </Box>

      {/* 费用示例对比 */}
      <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
        📈 费用参考
      </Typography>
      <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell><strong>文件大小</strong></TableCell>
              <TableCell><strong>本地上传</strong></TableCell>
              <TableCell><strong>URL下载</strong></TableCell>
              <TableCell><strong>成本差异</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>100KB</TableCell>
              <TableCell>110 Token</TableCell>
              <TableCell>160 Token</TableCell>
              <TableCell><Chip label="+45%" color="warning" size="small" /></TableCell>
            </TableRow>
            <TableRow>
              <TableCell>500KB</TableCell>
              <TableCell>150 Token</TableCell>
              <TableCell>200 Token</TableCell>
              <TableCell><Chip label="+33%" color="warning" size="small" /></TableCell>
            </TableRow>
            <TableRow>
              <TableCell>1MB</TableCell>
              <TableCell>200 Token</TableCell>
              <TableCell>250 Token</TableCell>
              <TableCell><Chip label="+25%" color="warning" size="small" /></TableCell>
            </TableRow>
            <TableRow>
              <TableCell>5MB</TableCell>
              <TableCell>600 Token</TableCell>
              <TableCell>850 Token</TableCell>
              <TableCell><Chip label="+42%" color="error" size="small" /></TableCell>
            </TableRow>
            <TableRow>
              <TableCell>10MB</TableCell>
              <TableCell>1100 Token</TableCell>
              <TableCell>1600 Token</TableCell>
              <TableCell><Chip label="+45%" color="error" size="small" /></TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      {/* 计费流程说明 */}
      <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
        🔄 计费流程
      </Typography>
      <Box sx={{ mb: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
        <Typography variant="body2" gutterBottom>
          <strong>1. 预扣费</strong> → 根据预估费用扣除Token
        </Typography>
        <Typography variant="body2" gutterBottom>
          <strong>2. 执行处理</strong> → 执行图像处理和上传操作
        </Typography>
        <Typography variant="body2">
          <strong>3. 结算</strong> → 成功保持预扣费，失败自动全额退费
        </Typography>
      </Box>

      {/* 自动退费机制 */}
      <Alert severity="success" sx={{ mb: 3 }}>
        <Typography variant="body2" gutterBottom>
          <strong>✅ 自动退费保护</strong>
        </Typography>
        <Typography variant="body2" component="div">
          <ul style={{ margin: '8px 0', paddingLeft: '20px' }}>
            <li>图片下载失败 → 全额退费</li>
            <li>图片处理失败 → 全额退费</li>
            <li>网盘上传失败 → 全额退费</li>
            <li>任何异常情况 → 全额退费</li>
          </ul>
        </Typography>
      </Alert>

      {/* Token计算器链接 */}
      <Box sx={{ textAlign: 'center', mt: 3 }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<CalculateIcon />}
          href="https://token-calc.aigchub.vip/"
          target="_blank"
          rel="noopener noreferrer"
        >
          打开Token计算器
        </Button>
        <Typography variant="caption" display="block" sx={{ mt: 1, color: 'text.secondary' }}>
          快速计算您的操作成本
        </Typography>
      </Box>

      {/* 成本优化建议 */}
      <Box sx={{ mt: 3 }}>
        <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
          💡 成本优化建议
        </Typography>
        <Box component="ul" sx={{ pl: 2, '& li': { mb: 1 } }}>
          <Typography component="li" variant="body2">
            <strong>选择本地上传</strong>：比URL下载便宜25-45%
          </Typography>
          <Typography component="li" variant="body2">
            <strong>压缩大图片</strong>：在上传前适当压缩可节约30-50%费用
          </Typography>
          <Typography component="li" variant="body2">
            <strong>合理设置质量</strong>：quality参数设为75-85可平衡质量和大小
          </Typography>
          <Typography component="li" variant="body2">
            <strong>批量处理优化</strong>：大文件建议先压缩再上传
          </Typography>
        </Box>
      </Box>
    </Box>
  );

  if (asCard) {
    return (
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          💰 计费说明
        </Typography>
        {content}
      </Paper>
    );
  }

  return (
    <Accordion defaultExpanded={defaultExpanded} sx={{ mb: 3 }}>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography variant="subtitle1" sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
          💰 计费说明
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        {content}
      </AccordionDetails>
    </Accordion>
  );
};
