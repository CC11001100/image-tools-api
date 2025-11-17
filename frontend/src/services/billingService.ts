/**
 * 计费服务 - 处理用户余额相关的API调用
 */

import { getCookie } from '../utils/cookieUtils';

// API基础URL
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:58888';

export interface UserBalance {
  user_id: number;
  username: string;
  balance: number;
  currency: string;
}

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

/**
 * 获取用户余额
 */
export const getUserBalance = async (): Promise<UserBalance | null> => {
  try {
    // 获取JWT token
    const token = getCookie('jwt_token');
    if (!token) {
      console.warn('获取余额失败：没有找到JWT token');
      return null;
    }

    const response = await fetch(`${API_BASE_URL}/api/billing/balance`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      console.error('获取余额API响应错误:', response.status, response.statusText);
      return null;
    }

    const result: ApiResponse<UserBalance> = await response.json();
    
    if (result.code === 200 && result.data) {
      console.log('获取用户余额成功:', result.data);
      return result.data;
    } else {
      console.warn('获取余额失败:', result.message);
      return null;
    }

  } catch (error) {
    console.error('获取用户余额时出错:', error);
    return null;
  }
};

/**
 * 获取计费历史
 */
export const getBillingHistory = async (limit: number = 20, offset: number = 0) => {
  try {
    const token = getCookie('jwt_token');
    if (!token) {
      throw new Error('未找到认证令牌');
    }

    const response = await fetch(`${API_BASE_URL}/api/billing/history?limit=${limit}&offset=${offset}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API请求失败: ${response.status}`);
    }

    const result = await response.json();
    return result;

  } catch (error) {
    console.error('获取计费历史时出错:', error);
    throw error;
  }
};

// 默认导出
const billingService = {
  getUserBalance,
  getBillingHistory,
};

export default billingService; 