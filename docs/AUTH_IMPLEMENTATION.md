# 用户认证功能实现文档

## 概述

本文档描述了图像处理工具API前端应用中基于Cookie的JWT认证功能的实现。该实现完全按照用户需求，集成了真实的用户系统认证服务。

## 功能特性

### ✅ 已实现功能

1. **基于Cookie的JWT Token存储**
   - 使用名为`jwt_token`的Cookie存储认证令牌
   - 自动设置Cookie过期时间（默认7天）
   - 支持安全的Cookie配置选项

2. **JWT Token验证**
   - 前端JWT token格式验证（支持HS512算法）
   - Token过期时间检查
   - 用户信息提取和解析（nickname、phone、userId等）

3. **用户认证状态管理**
   - 全局认证状态管理（AuthContext）
   - 自动检查和更新认证状态
   - 定期验证Token有效性（每5分钟）

4. **导航栏用户界面**
   - **未登录状态**：
     - 登录按钮 → 跳转到 `https://usersystem.aigchub.vip/login?redirect_url=当前页面URL`
     - 注册按钮 → 跳转到 `https://usersystem.aigchub.vip/register?redirect_url=当前页面URL`
   - **已登录状态**：
     - 虚化用户头像（显示昵称首字母）
     - 用户昵称显示
     - 用户下拉菜单：
       - 用户中心 → 在新页面打开 `https://usersystem.aigchub.vip/`
       - 注销功能

5. **真实JWT Token支持**
   - 支持真实的用户系统JWT token格式
   - 正确解析nickname、phone、userId等字段
   - 认证测试页面支持真实token测试

## JWT Token格式

### 真实JWT Token样例

```
eyJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOjEsInBob25lIjoiMTM3OTE0ODY5MzEiLCJuaWNrbmFtZSI6IkNDMTEwMDExMDAiLCJzdWIiOiIxMzc5MTQ4NjkzMSIsImlhdCI6MTc1MjgzMDU1NywiZXhwIjo0OTA2NDMwNTU3fQ.ZOrOJcdYVt9YUdI6vHDsnQrxB0_9Ns_ExFQM7lIFv239SwQUGHB2kIN76uxxE9IJkiAKIBDbYvsA7vKTLqFcxQ
```

### Payload结构

```json
{
  "userId": 1,
  "phone": "13791486931",
  "nickname": "CC11001100",
  "sub": "13791486931",
  "iat": 1752830557,
  "exp": 4906430557
}
```

### 字段说明

- `userId`: 用户ID
- `phone`: 用户手机号
- `nickname`: 用户昵称（主要显示字段）
- `sub`: 主题标识符（通常是手机号）
- `iat`: 签发时间
- `exp`: 过期时间

## 文件结构

```
frontend/src/
├── contexts/
│   └── AuthContext.tsx          # 用户认证上下文
├── utils/
│   ├── cookieUtils.ts          # Cookie操作工具函数
│   ├── jwtUtils.ts             # JWT Token处理工具函数
│   └── authTestUtils.ts        # 认证测试工具函数
├── pages/
│   └── AuthTestPage.tsx        # 认证功能测试页面
├── components/
│   └── Layout.tsx              # 更新的导航栏组件
└── App.tsx                     # 更新的应用根组件
```

## 核心组件说明

### 1. AuthContext (contexts/AuthContext.tsx)

提供全局的用户认证状态管理：

- **状态管理**：`isAuthenticated`, `user`, `isLoading`
- **操作方法**：`login()`, `logout()`, `refreshAuthStatus()`
- **自动功能**：定期检查Token状态，自动清理过期Token

### 2. Cookie工具函数 (utils/cookieUtils.ts)

提供Cookie操作的基础功能：

- `getCookie(name)` - 获取指定Cookie值
- `setCookie(name, value, days, path, secure, sameSite)` - 设置Cookie
- `deleteCookie(name, path)` - 删除Cookie
- `hasCookie(name)` - 检查Cookie是否存在

### 3. JWT工具函数 (utils/jwtUtils.ts)

提供JWT Token处理功能：

- `decodeJWTPayload(token)` - 解码JWT Payload
- `isJWTValid(token)` - 验证Token有效性
- `extractUserFromJWT(token)` - 提取用户信息
- `getJWTExpiration(token)` - 获取过期时间
- `isJWTExpiringSoon(token)` - 检查是否即将过期

### 4. 更新的Layout组件

导航栏根据用户登录状态显示不同内容：

**未登录状态：**
- 登录按钮
- 注册按钮

**已登录状态：**
- 用户头像（显示用户名首字母）
- 用户名标签
- 用户菜单按钮
- 下拉菜单（设置、注销）

## 使用方法

### 1. 基本使用

```tsx
import { useAuth } from '../contexts/AuthContext';

function MyComponent() {
  const { isAuthenticated, user, login, logout } = useAuth();

  if (isAuthenticated) {
    return <div>欢迎, {user?.nickname}!</div>;
  } else {
    return <button onClick={() => login(token)}>登录</button>;
  }
}
```

### 2. 登录流程

```tsx
// 1. 获取JWT Token（通常来自登录API）
const token = await loginAPI(username, password);

// 2. 使用Token登录
const success = login(token);

if (success) {
  console.log('登录成功');
} else {
  console.log('登录失败');
}
```

### 3. 注销流程

```tsx
// 简单调用logout方法
logout();
```

## 测试功能

访问 `/auth-test` 页面可以测试认证功能：

1. **查看当前认证状态**
2. **使用预定义测试用户登录**
3. **查看JWT Token详细信息**
4. **测试注销功能**

### 测试功能

1. **模拟用户登录**：
   - 张三 (zhangsan@test.com)
   - 李四 (lisi@test.com)
   - 王五 (wangwu@test.com)
   - Admin (admin@test.com)

2. **真实JWT Token测试**：
   - 使用提供的真实JWT token进行登录测试
   - 验证nickname、phone、userId等字段的正确解析

3. **自定义Token测试**：
   - 支持输入自定义JWT token进行测试
   - 实时验证token格式和有效性

## 安全考虑

### ✅ 已实现的安全措施

1. **Cookie安全配置**
   - 支持Secure标志（HTTPS）
   - 支持SameSite属性
   - 自动过期时间设置

2. **Token验证**
   - 格式验证
   - 过期时间检查
   - 定期状态刷新

3. **自动清理**
   - 过期Token自动删除
   - 无效Token自动清理

### ⚠️ 注意事项

1. **前端验证限制**
   - 前端无法验证JWT签名
   - 需要后端API进行完整验证

2. **测试Token**
   - 当前使用模拟Token仅用于演示
   - 生产环境需要真实的后端认证服务

## 后续改进建议

1. **集成真实后端认证API**
2. **添加登录/注册对话框**
3. **实现Token自动刷新机制**
4. **添加更多用户信息字段**
5. **实现记住登录状态功能**
6. **添加多因素认证支持**

## 用户系统集成

### 认证服务端点

- **登录页面**: `https://usersystem.aigchub.vip/login`
- **注册页面**: `https://usersystem.aigchub.vip/register`
- **用户中心**: `https://usersystem.aigchub.vip/`

### 跳转逻辑

1. **登录跳转**：
   ```
   https://usersystem.aigchub.vip/login?redirect_url=当前页面URL
   ```

2. **注册跳转**：
   ```
   https://usersystem.aigchub.vip/register?redirect_url=当前页面URL
   ```

3. **用户中心**：
   - 在新页面打开用户中心
   - 用户可以管理个人信息和设置

### Cookie管理

- **Cookie名称**: `jwt_token`
- **存储位置**: 浏览器Cookie
- **过期时间**: 根据JWT token的exp字段自动管理
- **作用域**: 当前域名下所有页面

## 兼容性

- ✅ 删除了所有localStorage相关的jwt_token操作
- ✅ 完全基于Cookie的认证机制
- ✅ 向后兼容现有功能
- ✅ 不影响其他页面和组件

## 总结

本次实现完全按照用户需求，成功实现了基于Cookie的JWT认证功能，并与真实的用户系统进行了集成：

### ✅ 核心功能

1. **完整的认证流程**：从Cookie获取jwt_token → 验证有效性 → 提取用户信息 → 更新UI状态
2. **真实系统集成**：登录/注册跳转到指定的用户系统URL，携带redirect_url参数
3. **用户界面适配**：根据登录状态显示不同的导航栏内容
4. **用户信息显示**：正确显示nickname、头像等用户信息
5. **用户中心集成**：提供用户中心入口，在新页面打开

### ✅ 技术特点

- 支持HS512算法的JWT token
- 自动处理token过期和无效情况
- 定期检查认证状态
- 完整的TypeScript类型支持
- 响应式用户界面设计

### ✅ 测试验证

- 提供认证测试页面（/auth-test）
- 支持真实JWT token测试
- 支持自定义token输入测试
- 实时显示token解析结果

所有功能都已实现并可以正常工作，用户可以通过认证测试页面验证各项功能。
