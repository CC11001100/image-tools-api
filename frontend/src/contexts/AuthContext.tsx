import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { getCookie, setCookie, deleteCookie } from '../utils/cookieUtils';
import { isJWTValid, extractUserFromJWT, isJWTExpiringSoon } from '../utils/jwtUtils';
import { handleAuthCallback, shouldHandleAuthCallback } from '../utils/authUtils';

export interface User {
  nickname: string;
  phone?: string;
  userId?: number;
  username?: string;
  email?: string;
}

export interface AuthContextType {
  // 状态
  isAuthenticated: boolean;
  user: User | null;
  isLoading: boolean;
  
  // 操作方法
  login: (token: string) => boolean;
  logout: () => void;
  refreshAuthStatus: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export interface AuthProviderProps {
  children: ReactNode;
}

const JWT_COOKIE_NAME = 'jwt_token';

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  /**
   * 从多个位置获取JWT token
   */
  const getTokenFromMultipleSources = (): string | null => {
    // 1. 首先检查cookie
    let token = getCookie(JWT_COOKIE_NAME);
    if (token) {
      console.log('AuthContext: 从cookie获取到token');
      return token;
    }

    // 2. 检查localStorage
    try {
      token = localStorage.getItem('jwt_token') || localStorage.getItem('token') || localStorage.getItem('authToken');
      if (token) {
        console.log('AuthContext: 从localStorage获取到token');
        // 将token同步到cookie
        setCookie(JWT_COOKIE_NAME, token, 7);
        return token;
      }
    } catch (error) {
      console.warn('AuthContext: 无法访问localStorage:', error);
    }

    // 3. 检查sessionStorage
    try {
      token = sessionStorage.getItem('jwt_token') || sessionStorage.getItem('token') || sessionStorage.getItem('authToken');
      if (token) {
        console.log('AuthContext: 从sessionStorage获取到token');
        // 将token同步到cookie
        setCookie(JWT_COOKIE_NAME, token, 7);
        return token;
      }
    } catch (error) {
      console.warn('AuthContext: 无法访问sessionStorage:', error);
    }

    // 4. 检查URL参数（用于处理登录回调）
    const urlParams = new URLSearchParams(window.location.search);
    token = urlParams.get('jwt_token') || urlParams.get('token') || urlParams.get('access_token');
    if (token) {
      console.log('AuthContext: 从URL参数获取到token');
      // 保存到cookie并清除URL参数
      setCookie(JWT_COOKIE_NAME, token, 7);
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.delete('jwt_token');
      newUrl.searchParams.delete('token');
      newUrl.searchParams.delete('access_token');
      window.history.replaceState({}, document.title, newUrl.toString());
      return token;
    }

    return null;
  };

  /**
   * 检查并更新认证状态
   */
  const checkAuthStatus = () => {
    console.log('AuthContext: 开始检查认证状态...');
    console.log('AuthContext: 所有cookies:', document.cookie);

    const token = getTokenFromMultipleSources();
    console.log('AuthContext: 获取到的jwt_token:', token);

    if (!token) {
      console.log('AuthContext: 没有找到jwt_token，设置为未登录状态');
      setIsAuthenticated(false);
      setUser(null);
      return;
    }

    console.log('AuthContext: 开始验证JWT token...');
    const isValid = isJWTValid(token);
    console.log('AuthContext: JWT token有效性:', isValid);

    if (isValid) {
      const userInfo = extractUserFromJWT(token);
      console.log('AuthContext: 提取的用户信息:', userInfo);

      if (userInfo) {
        console.log('AuthContext: 设置为已登录状态');
        setIsAuthenticated(true);
        setUser(userInfo);

        // 检查token是否即将过期，如果是则提醒用户
        if (isJWTExpiringSoon(token)) {
          console.warn('JWT token即将过期，请重新登录');
        }
      } else {
        // token有效但无法提取用户信息
        console.log('AuthContext: token有效但无法提取用户信息');
        setIsAuthenticated(false);
        setUser(null);
        deleteCookie(JWT_COOKIE_NAME);
      }
    } else {
      // token无效，清除cookie
      console.log('AuthContext: token无效，清除cookie');
      setIsAuthenticated(false);
      setUser(null);
      deleteCookie(JWT_COOKIE_NAME);
    }
  };

  /**
   * 登录方法
   * @param token JWT token
   * @returns 登录是否成功
   */
  const login = (token: string): boolean => {
    if (!isJWTValid(token)) {
      console.error('提供的JWT token无效');
      return false;
    }

    const userInfo = extractUserFromJWT(token);
    if (!userInfo) {
      console.error('无法从JWT token中提取用户信息');
      return false;
    }

    // 设置cookie（7天过期）
    setCookie(JWT_COOKIE_NAME, token, 7);
    
    setIsAuthenticated(true);
    setUser(userInfo);
    
    console.log('用户登录成功:', userInfo);
    return true;
  };

  /**
   * 注销方法
   */
  const logout = () => {
    deleteCookie(JWT_COOKIE_NAME);
    setIsAuthenticated(false);
    setUser(null);
    console.log('用户已注销');
  };

  /**
   * 刷新认证状态
   */
  const refreshAuthStatus = () => {
    checkAuthStatus();
  };

  // 组件挂载时检查认证状态
  useEffect(() => {
    console.log('AuthContext: 组件挂载，开始检查认证状态...');
    checkAuthStatus();
    setIsLoading(false);
  }, []);

  // 定期检查token状态（每5分钟）
  useEffect(() => {
    const interval = setInterval(() => {
      if (isAuthenticated) {
        checkAuthStatus();
      }
    }, 5 * 60 * 1000); // 5分钟

    return () => clearInterval(interval);
  }, [isAuthenticated]);

  const value: AuthContextType = {
    isAuthenticated,
    user,
    isLoading,
    login,
    logout,
    refreshAuthStatus,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * 使用认证上下文的Hook
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth必须在AuthProvider内部使用');
  }
  return context;
};
