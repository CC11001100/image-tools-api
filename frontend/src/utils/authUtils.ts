import { getCookie, setCookie } from './cookieUtils';

/**
 * 处理用户中心登录回调
 * 检查URL参数中是否包含jwt_token，如果有则保存到cookie
 */
export const handleAuthCallback = (): boolean => {
  const urlParams = new URLSearchParams(window.location.search);
  const jwtToken = urlParams.get('jwt_token');
  
  if (jwtToken) {
    // 保存token到cookie（7天过期）
    setCookie('jwt_token', jwtToken, 7);
    
    // 清除URL中的token参数
    const newUrl = new URL(window.location.href);
    newUrl.searchParams.delete('jwt_token');
    window.history.replaceState({}, document.title, newUrl.toString());
    
    console.log('用户中心登录回调处理成功');
    return true;
  }
  
  return false;
};

/**
 * 检查是否需要处理认证回调
 */
export const shouldHandleAuthCallback = (): boolean => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.has('jwt_token');
};

/**
 * 生成登录URL
 */
export const generateLoginUrl = (redirectUrl?: string): string => {
  const currentUrl = redirectUrl || window.location.href;
  return `https://usersystem.aigchub.vip/login?redirect_url=${encodeURIComponent(currentUrl)}`;
};

/**
 * 生成注册URL
 */
export const generateRegisterUrl = (redirectUrl?: string): string => {
  const currentUrl = redirectUrl || window.location.href;
  return `https://usersystem.aigchub.vip/register?redirect_url=${encodeURIComponent(currentUrl)}`;
};
