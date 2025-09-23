/**
 * JWT Token工具函数
 */

export interface JWTPayload {
  sub?: string;
  exp?: number;
  iat?: number;
  userId?: number;
  phone?: string;
  nickname?: string;
  username?: string;
  email?: string;
  [key: string]: any;
}

/**
 * 解码JWT token的payload部分（不验证签名）
 * @param token JWT token
 * @returns 解码后的payload，如果解码失败返回null
 */
export const decodeJWTPayload = (token: string): JWTPayload | null => {
  try {
    // JWT token格式：header.payload.signature
    const parts = token.split('.');
    if (parts.length !== 3) {
      return null;
    }

    // 解码payload部分（Base64URL）
    const payload = parts[1];
    // 处理Base64URL编码（替换字符并添加padding）
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
    const padded = base64.padEnd(base64.length + (4 - base64.length % 4) % 4, '=');
    
    const decoded = atob(padded);
    return JSON.parse(decoded);
  } catch (error) {
    console.error('JWT解码失败:', error);
    return null;
  }
};

/**
 * 检查JWT token是否有效（格式正确且未过期）
 * @param token JWT token
 * @returns 是否有效
 */
export const isJWTValid = (token: string): boolean => {
  if (!token || typeof token !== 'string') {
    return false;
  }

  const payload = decodeJWTPayload(token);
  if (!payload) {
    return false;
  }

  // 检查是否过期
  if (payload.exp) {
    const currentTime = Math.floor(Date.now() / 1000);
    if (payload.exp < currentTime) {
      return false;
    }
  }

  return true;
};

/**
 * 从JWT token中提取用户信息
 * @param token JWT token
 * @returns 用户信息，如果提取失败返回null
 */
export const extractUserFromJWT = (token: string): {
  nickname: string;
  phone?: string;
  userId?: number;
  username?: string;
  email?: string;
} | null => {
  const payload = decodeJWTPayload(token);
  if (!payload) {
    return null;
  }

  // 优先使用nickname字段，如果没有则使用其他字段作为fallback
  const nickname = payload.nickname || payload.username || payload.sub || payload.name || payload.user || 'Unknown User';
  const phone = payload.phone;
  const userId = payload.userId;
  const email = payload.email;
  const username = payload.username;

  const result: {
    nickname: string;
    phone?: string;
    userId?: number;
    username?: string;
    email?: string;
  } = {
    nickname: String(nickname),
  };

  if (phone) result.phone = String(phone);
  if (userId) result.userId = Number(userId);
  if (username) result.username = String(username);
  if (email) result.email = String(email);

  return result;
};

/**
 * 获取JWT token的过期时间
 * @param token JWT token
 * @returns 过期时间的Date对象，如果获取失败返回null
 */
export const getJWTExpiration = (token: string): Date | null => {
  const payload = decodeJWTPayload(token);
  if (!payload || !payload.exp) {
    return null;
  }

  return new Date(payload.exp * 1000);
};

/**
 * 检查JWT token是否即将过期（默认5分钟内）
 * @param token JWT token
 * @param minutesBeforeExpiry 提前多少分钟算作即将过期，默认5分钟
 * @returns 是否即将过期
 */
export const isJWTExpiringSoon = (token: string, minutesBeforeExpiry: number = 5): boolean => {
  const expirationDate = getJWTExpiration(token);
  if (!expirationDate) {
    return false;
  }

  const currentTime = new Date();
  const timeUntilExpiry = expirationDate.getTime() - currentTime.getTime();
  const minutesUntilExpiry = timeUntilExpiry / (1000 * 60);

  return minutesUntilExpiry <= minutesBeforeExpiry;
};
