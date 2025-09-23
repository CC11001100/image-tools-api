/**
 * 认证调试工具函数
 */

import { getCookie } from './cookieUtils';
import { decodeJWTPayload, isJWTValid, extractUserFromJWT } from './jwtUtils';

export const debugAuth = () => {
  console.log('=== 认证调试开始 ===');
  
  // 1. 检查所有cookies
  console.log('1. 所有Cookies:', document.cookie);
  
  // 2. 检查jwt_token cookie
  const jwtToken = getCookie('jwt_token');
  console.log('2. JWT Token Cookie:', jwtToken);
  
  if (!jwtToken) {
    console.log('❌ 没有找到jwt_token cookie');
    return;
  }
  
  // 3. 解码JWT
  console.log('3. 开始解码JWT...');
  const payload = decodeJWTPayload(jwtToken);
  console.log('   Payload:', payload);
  
  // 4. 检查有效性
  console.log('4. 检查JWT有效性...');
  const isValid = isJWTValid(jwtToken);
  console.log('   是否有效:', isValid);
  
  // 5. 提取用户信息
  console.log('5. 提取用户信息...');
  const userInfo = extractUserFromJWT(jwtToken);
  console.log('   用户信息:', userInfo);
  
  // 6. 检查过期时间
  if (payload && payload.exp) {
    const expDate = new Date(payload.exp * 1000);
    const currentTime = new Date();
    console.log('6. 时间检查:');
    console.log('   过期时间:', expDate.toLocaleString());
    console.log('   当前时间:', currentTime.toLocaleString());
    console.log('   是否过期:', payload.exp < Math.floor(Date.now() / 1000));
  }
  
  console.log('=== 认证调试结束 ===');
  
  return {
    cookieExists: !!jwtToken,
    token: jwtToken,
    payload,
    isValid,
    userInfo
  };
};

// 在浏览器控制台中可用
if (typeof window !== 'undefined') {
  (window as any).debugAuth = debugAuth;
}
