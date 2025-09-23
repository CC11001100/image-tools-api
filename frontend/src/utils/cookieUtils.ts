/**
 * Cookie操作工具函数
 */

/**
 * 获取指定名称的cookie值
 * @param name cookie名称
 * @returns cookie值，如果不存在则返回null
 */
export const getCookie = (name: string): string | null => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    const cookieValue = parts.pop()?.split(';').shift();
    return cookieValue || null;
  }
  return null;
};

/**
 * 设置cookie
 * @param name cookie名称
 * @param value cookie值
 * @param days 过期天数，默认7天
 * @param path 路径，默认为根路径
 * @param secure 是否只在HTTPS下传输
 * @param sameSite SameSite属性
 */
export const setCookie = (
  name: string,
  value: string,
  days: number = 7,
  path: string = '/',
  secure: boolean = false,
  sameSite: 'Strict' | 'Lax' | 'None' = 'Lax'
): void => {
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  
  let cookieString = `${name}=${value}; expires=${expires.toUTCString()}; path=${path}`;
  
  if (secure) {
    cookieString += '; secure';
  }
  
  cookieString += `; samesite=${sameSite}`;
  
  document.cookie = cookieString;
};

/**
 * 删除指定名称的cookie
 * @param name cookie名称
 * @param path 路径，默认为根路径
 */
export const deleteCookie = (name: string, path: string = '/'): void => {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${path};`;
};

/**
 * 检查cookie是否存在
 * @param name cookie名称
 * @returns 是否存在
 */
export const hasCookie = (name: string): boolean => {
  return getCookie(name) !== null;
};
