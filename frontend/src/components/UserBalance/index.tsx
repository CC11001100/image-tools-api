/**
 * 用户余额显示组件
 */

import React, { useState, useEffect } from 'react';
import {
  Chip,
  Tooltip,
  CircularProgress,
  Box,
} from '@mui/material';
import {
  AccountBalanceWallet as WalletIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';

import { getUserBalance, UserBalance } from '../../services/billingService';
import { useAuth } from '../../contexts/AuthContext';

interface UserBalanceProps {
  sx?: object;
}

const UserBalanceComponent: React.FC<UserBalanceProps> = ({ sx }) => {
  const [balance, setBalance] = useState<UserBalance | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const { isAuthenticated, user } = useAuth();

  // 获取用户余额
  const fetchBalance = async () => {
    if (!isAuthenticated || !user) {
      return;
    }

    setLoading(true);
    setError('');

    try {
      const balanceData = await getUserBalance();
      setBalance(balanceData);
    } catch (err) {
      console.error('获取余额失败:', err);
      setError('获取余额失败');
    } finally {
      setLoading(false);
    }
  };

  // 用户登录状态变化时重新获取余额
  useEffect(() => {
    if (isAuthenticated && user) {
      fetchBalance();
    } else {
      setBalance(null);
      setError('');
    }
  }, [isAuthenticated, user]);

  // 如果用户未登录，不显示余额
  if (!isAuthenticated || !user) {
    return null;
  }

  // 处理点击刷新
  const handleRefresh = (e: React.MouseEvent) => {
    e.stopPropagation();
    fetchBalance();
  };

  // 格式化余额显示
  const formatBalance = (amount: number): string => {
    return amount.toFixed(2);
  };

  // 根据余额确定颜色
  const getBalanceColor = (amount: number): 'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' => {
    if (amount >= 10) return 'success';
    if (amount >= 5) return 'warning';
    if (amount >= 1) return 'info';
    return 'error';
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', ...sx }}>
      {loading ? (
        <Chip
          icon={<CircularProgress size={16} sx={{ color: 'inherit' }} />}
          label="加载中..."
          variant="outlined"
          sx={{
            color: 'white',
            borderColor: 'rgba(255, 255, 255, 0.5)',
            '& .MuiChip-label': {
              color: 'white',
            },
          }}
        />
      ) : error ? (
        <Tooltip title="点击重试">
          <Chip
            icon={<RefreshIcon />}
            label="余额获取失败"
            variant="outlined"
            color="error"
            onClick={handleRefresh}
            sx={{
              color: 'white',
              borderColor: 'rgba(255, 255, 255, 0.5)',
              '& .MuiChip-label': {
                color: 'white',
              },
              cursor: 'pointer',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          />
        </Tooltip>
      ) : balance ? (
        <Tooltip 
          title={`当前余额: $${formatBalance(balance.balance)} USD\n点击刷新余额`}
          arrow
        >
          <Chip
            icon={<WalletIcon />}
            label={`$${formatBalance(balance.balance)}`}
            variant="outlined"
            color={getBalanceColor(balance.balance)}
            onClick={handleRefresh}
            sx={{
              color: 'white',
              borderColor: 'rgba(255, 255, 255, 0.5)',
              '& .MuiChip-label': {
                color: 'white',
                fontFamily: 'monospace',
                fontWeight: 600,
              },
              '& .MuiChip-icon': {
                color: 'white',
              },
              cursor: 'pointer',
              transition: 'all 0.2s ease-in-out',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                borderColor: 'rgba(255, 255, 255, 0.7)',
                transform: 'scale(1.05)',
              },
            }}
          />
        </Tooltip>
      ) : null}
    </Box>
  );
};

export default UserBalanceComponent; 