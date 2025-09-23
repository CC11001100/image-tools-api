/**
 * 认证测试工具函数
 * 用于生成测试用的JWT token
 */

/**
 * 生成一个测试用的JWT token
 * 注意：这只是用于前端测试，实际应用中JWT token应该由后端生成
 */
export const generateTestJWTToken = (username: string = '测试用户', email: string = 'test@test.com'): string => {
  // JWT Header
  const header = {
    alg: 'HS256',
    typ: 'JWT'
  };

  // JWT Payload
  const payload = {
    sub: '1234567890',
    username: username,
    email: email,
    iat: Math.floor(Date.now() / 1000), // 当前时间
    exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24小时后过期
  };

  // 简单的Base64URL编码（仅用于测试）
  const base64UrlEncode = (obj: any): string => {
    const jsonString = JSON.stringify(obj);
    const base64 = btoa(jsonString);
    return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
  };

  const encodedHeader = base64UrlEncode(header);
  const encodedPayload = base64UrlEncode(payload);
  
  // 模拟签名（实际应用中应该使用真实的签名算法）
  const signature = 'test_signature_' + Math.random().toString(36).substring(7);
  const encodedSignature = btoa(signature).replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');

  return `${encodedHeader}.${encodedPayload}.${encodedSignature}`;
};

/**
 * 预定义的测试用户
 */
export const TEST_USERS = [
  { username: '张三', email: 'zhangsan@test.com' },
  { username: '李四', email: 'lisi@test.com' },
  { username: '王五', email: 'wangwu@test.com' },
  { username: 'Admin', email: 'admin@test.com' },
];

/**
 * 为指定用户生成测试token
 */
export const generateTokenForUser = (userIndex: number = 0): string => {
  const user = TEST_USERS[userIndex] || TEST_USERS[0];
  return generateTestJWTToken(user.username, user.email);
};
