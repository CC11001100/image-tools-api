# Resize API 计费文档

## 概述

resize相关的两个API接口已经集成了完整的计费功能，需要用户认证访问，并按照使用量进行Token扣费。

## 接口列表

### 1. `/api/v1/resize` - 上传图片缩放
- **认证要求**: 必须提供有效的API Token
- **计费策略**: 基础费用 + 上传费用

### 2. `/api/v1/resize-by-url` - URL图片缩放  
- **认证要求**: 必须提供有效的API Token
- **计费策略**: 基础费用 + 下载费用 + 上传费用

## 计费策略详情

### 费用结构
- **基础调用费用**: 100 Token（每次API调用的固定费用）
- **下载费用**: 100 Token/MB（从URL下载图片的费用）
- **上传费用**: 50 Token/MB（上传处理后图片到网盘的费用）
- **最小计费单位**: 1KB（不足1KB按1KB计算）

### 费用计算公式

#### `/api/v1/resize` 接口
```
总费用 = 基础费用 + 上传费用
总费用 = 100 + 50 × (处理后图片大小MB)
```

#### `/api/v1/resize-by-url` 接口
```
总费用 = 基础费用 + 下载费用 + 上传费用
总费用 = 100 + 100 × (原图下载大小MB) + 50 × (处理后图片大小MB)
```

### 计费示例

#### 示例1: 上传1MB图片进行缩放
- 基础费用: 100 Token
- 上传费用: 50 Token (1MB × 50)
- **总费用: 150 Token**

#### 示例2: 从URL下载2MB图片，缩放后1MB
- 基础费用: 100 Token  
- 下载费用: 200 Token (2MB × 100)
- 上传费用: 50 Token (1MB × 50)
- **总费用: 350 Token**

#### 示例3: 小图片处理（下载100KB，上传80KB）
- 基础费用: 100 Token
- 下载费用: 10 Token (0.1MB × 100)
- 上传费用: 4 Token (0.08MB × 50)
- **总费用: 114 Token**

## 认证要求

### API Token格式
```
Authorization: aigc-hub-5c5e31cf7dd2442a97bd5b7cdbbddc1a
```

### 认证失败响应
```json
{
  "code": 401,
  "message": "未授权访问，请先登录"
}
```

### 余额不足响应
```json
{
  "code": 402,
  "message": "余额不足或预扣费失败，请检查账户余额"
}
```

## 计费流程

### 三步计费流程
1. **预扣费**: 在处理前根据预估费用扣除Token
2. **执行处理**: 执行图片缩放和上传操作
3. **结算**: 
   - 成功: 保持预扣费（预估准确）
   - 失败: 返还所有费用

### 费用透明度
API响应中包含详细的计费信息：

```json
{
  "success": true,
  "message": "图片大小调整并上传成功，消耗 150 Token",
  "file": { ... },
  "processing_info": {
    "billing_info": {
      "base_cost": 100,
      "upload_cost": 50,
      "total_cost": 150,
      "breakdown": {
        "base": "100 Token (基础调用费用)",
        "upload": "50 Token (上传 1048576 字节)"
      }
    },
    "call_id": "req_abc123..."
  }
}
```

## 错误处理

### 计费相关错误
- **401 未授权**: API Token无效或过期
- **402 余额不足**: 账户Token余额不足以支付预估费用
- **500 处理失败**: 图片处理失败，已自动退费

### 自动退费机制
- 图片下载失败 → 自动退费
- 图片处理失败 → 自动退费  
- 网盘上传失败 → 自动退费
- 任何异常情况 → 自动退费

## 最佳实践

### 1. 成本优化
- 在上传前压缩图片可以减少上传费用
- 选择合适的质量参数平衡文件大小和图片质量
- 批量处理时考虑图片大小对总成本的影响

### 2. 错误处理
- 检查API响应中的计费信息
- 监控账户余额，及时充值
- 处理402错误，提示用户余额不足

### 3. 监控使用量
- 记录每次API调用的费用
- 定期检查账户余额和使用统计
- 设置费用预警机制

## 技术实现

### 计费工具类
```python
from app.utils.billing_utils import calculate_resize_billing

# 计算费用
billing_info = calculate_resize_billing(
    upload_size_bytes=result_size,
    download_size_bytes=download_size  # 仅resize-by-url需要
)

estimated_tokens = billing_info["total_cost"]
```

### 预扣费示例
```python
call_id = await billing_service.pre_charge(
    api_token=api_token,
    api_path="/api/v1/resize",
    context=context,
    estimated_tokens=estimated_tokens,
    remark="图片缩放处理"
)
```

## 更新日志

### v1.0.0 (2025-01-27)
- ✅ 集成完整的计费功能
- ✅ 强制要求API Token认证
- ✅ 实现三步计费流程
- ✅ 添加自动退费机制
- ✅ 提供详细的费用明细
