/**
 * JWT测试工具
 * 用于验证JWT token解析功能
 */

import { decodeJWTPayload, isJWTValid, extractUserFromJWT } from './jwtUtils';

// 真实的JWT token样例
const REAL_JWT_TOKEN = 'eyJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOjEsInBob25lIjoiMTM3OTE0ODY5MzEiLCJuaWNrbmFtZSI6IkNDMTEwMDExMDAiLCJzdWIiOiIxMzc5MTQ4NjkzMSIsImlhdCI6MTc1MjgzMDU1NywiZXhwIjo0OTA2NDMwNTU3fQ.ZOrOJcdYVt9YUdI6vHDsnQrxB0_9Ns_ExFQM7lIFv239SwQUGHB2kIN76uxxE9IJkiAKIBDbYvsA7vKTLqFcxQ';

/**
 * 测试JWT token解析功能
 */
export const testJWTFunctions = () => {
  console.log('=== JWT Token 测试 ===');
  console.log('Token:', REAL_JWT_TOKEN);
  console.log('');

  // 测试解码
  console.log('1. 解码测试:');
  const payload = decodeJWTPayload(REAL_JWT_TOKEN);
  console.log('Payload:', payload);
  console.log('');

  // 测试有效性
  console.log('2. 有效性测试:');
  const isValid = isJWTValid(REAL_JWT_TOKEN);
  console.log('Is Valid:', isValid);
  console.log('');

  // 测试用户信息提取
  console.log('3. 用户信息提取测试:');
  const userInfo = extractUserFromJWT(REAL_JWT_TOKEN);
  console.log('User Info:', userInfo);
  console.log('');

  // 返回测试结果
  return {
    payload,
    isValid,
    userInfo
  };
};

// 如果在浏览器控制台中运行，可以直接调用
if (typeof window !== 'undefined') {
  (window as any).testJWT = testJWTFunctions;
}
