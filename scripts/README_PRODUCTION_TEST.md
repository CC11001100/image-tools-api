# 生产环境API测试指南

## 概述

本目录包含用于测试生产环境图片工具箱API的脚本和配置文件。

## 文件说明

- `test_production_api.sh` - 生产环境API测试脚本
- `production_config.env` - 生产环境配置文件
- `quick_test.sh` - 本地快速测试脚本
- `test_api_curl.sh` - 通用API测试脚本

## 使用步骤

### 1. 配置生产环境

编辑 `production_config.env` 文件，修改以下配置：

```bash
# 生产服务器配置
PROD_HOST=your-actual-server.com      # 修改为实际的服务器地址
PROD_PORT=80                          # 修改为实际的端口号
PROD_PROTOCOL=http                    # 如果使用HTTPS，改为https

# 认证配置
TEST_TOKEN=your-actual-token          # 修改为实际的测试Token
```

### 2. 运行生产环境测试

```bash
# 运行生产环境API测试
./scripts/test_production_api.sh
```

### 3. 测试项目

脚本会自动测试以下API端点：

1. **健康检查**: `/api/health`
2. **用户信息**: `/api/v1/auth-example/user-info`
3. **计费示例**: `/api/v1/auth-example/billing-example`
4. **过滤器列表**: `/api/v1/filter/list`
5. **AI样式列表**: `/api/v1/ai-text-to-image/styles`

### 4. 测试结果

脚本会显示：
- 网络连通性测试结果
- 每个API端点的测试结果
- HTTP状态码和响应格式验证
- 总体成功率统计

## 配置示例

### HTTP服务器
```bash
PROD_HOST=api.example.com
PROD_PORT=80
PROD_PROTOCOL=http
```

### HTTPS服务器
```bash
PROD_HOST=api.example.com
PROD_PORT=443
PROD_PROTOCOL=https
```

### 带端口的服务器
```bash
PROD_HOST=192.168.1.100
PROD_PORT=8080
PROD_PROTOCOL=http
```

## 故障排查

### 网络连通性问题
- 检查服务器地址和端口是否正确
- 检查防火墙设置
- 确认服务器是否正在运行

### API测试失败
- 检查认证Token是否正确
- 检查API路径是否正确
- 查看服务器日志

### 响应格式问题
- 确认API返回统一的JSON格式
- 检查HTTP状态码是否为200
- 验证响应中是否包含code、message、data字段

## 本地测试

如果需要测试本地服务，可以使用：

```bash
# 快速本地测试
./scripts/quick_test.sh

# 完整本地测试
./scripts/test_api_curl.sh
```

## 注意事项

1. 确保生产服务器已正确部署
2. 确认网络连通性
3. 使用有效的认证Token
4. 检查服务器防火墙设置
5. 确认API服务正在运行

## 支持

如果遇到问题，请检查：
1. 配置文件是否正确
2. 网络连接是否正常
3. 服务器状态是否健康
4. API文档是否可访问
