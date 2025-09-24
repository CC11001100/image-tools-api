# 🎯 Watermark API 完整参数参考

## 📋 接口信息

**端点**: `POST /api/v1/watermark-by-url`  
**域名**: `https://image-tools.aigchub.vip`  
**认证**: JWT Bearer Token  
**内容类型**: `application/json`  

## 🔑 获取JWT Token

```bash
curl -X POST "https://image-tools.aigchub.vip/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "YOUR_PHONE",
    "password": "YOUR_PASSWORD"
  }'
```

## 📋 参数说明

### 必需参数
| 参数 | 类型 | 说明 |
|------|------|------|
| `image_url` | string | 图片URL地址 |
| `watermark_text` | string | 水印文字内容 |

### 可选参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `position` | string | "center" | 水印位置: center, top-left, top-right, bottom-left, bottom-right |
| `font_size` | int | 36 | 字体大小: 1-200 |
| `font_color` | string | "#000000" | 字体颜色: 十六进制格式 #RRGGBB |
| `font_family` | string | "Arial" | 字体族: Arial, Times, Helvetica等 |
| `opacity` | float | 0.5 | 透明度: 0.0-1.0 |
| `margin_x` | int | 20 | 水平边距: 像素值 |
| `margin_y` | int | 20 | 垂直边距: 像素值 |
| `rotation` | int | 0 | 旋转角度: 0-360度 |
| `stroke_width` | int | 0 | 描边宽度: 像素值 |
| `stroke_color` | string | "#000000" | 描边颜色: 十六进制格式 #RRGGBB |
| `shadow_offset_x` | int | 0 | 阴影X偏移: 像素值 |
| `shadow_offset_y` | int | 0 | 阴影Y偏移: 像素值 |
| `shadow_color` | string | "#000000" | 阴影颜色: 十六进制格式 #RRGGBB |
| `repeat_mode` | string | "none" | 重复模式: none, tile, diagonal |
| `quality` | int | 90 | 输出质量: 1-100 |

## 🎯 Curl命令示例

### 1. 基础水印
```bash
curl -X POST "https://image-tools.aigchub.vip/api/v1/watermark-by-url" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "image_url": "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original.jpg",
    "watermark_text": "AIGC HUB",
    "position": "center",
    "font_size": 36,
    "font_color": "#FF0000",
    "opacity": 0.7,
    "quality": 90
  }' \
  --output watermark_basic.jpg
```

### 2. 完整参数水印
```bash
curl -X POST "https://image-tools.aigchub.vip/api/v1/watermark-by-url" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "image_url": "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original.jpg",
    "watermark_text": "© AIGC HUB 2024",
    "position": "bottom-right",
    "font_size": 24,
    "font_color": "#FFFFFF",
    "font_family": "Arial",
    "opacity": 0.8,
    "margin_x": 30,
    "margin_y": 30,
    "rotation": 0,
    "stroke_width": 2,
    "stroke_color": "#000000",
    "shadow_offset_x": 2,
    "shadow_offset_y": 2,
    "shadow_color": "#808080",
    "repeat_mode": "none",
    "quality": 95
  }' \
  --output watermark_full.jpg
```

### 3. 平铺水印
```bash
curl -X POST "https://image-tools.aigchub.vip/api/v1/watermark-by-url" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "image_url": "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original.jpg",
    "watermark_text": "WATERMARK",
    "position": "center",
    "font_size": 20,
    "font_color": "#FF0000",
    "opacity": 0.3,
    "repeat_mode": "tile",
    "quality": 90
  }' \
  --output watermark_tile.jpg
```

### 4. 旋转水印
```bash
curl -X POST "https://image-tools.aigchub.vip/api/v1/watermark-by-url" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "image_url": "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original.jpg",
    "watermark_text": "ROTATED WATERMARK",
    "position": "center",
    "font_size": 32,
    "font_color": "#0000FF",
    "opacity": 0.6,
    "rotation": 45,
    "quality": 90
  }' \
  --output watermark_rotated.jpg
```

### 5. 描边阴影水印
```bash
curl -X POST "https://image-tools.aigchub.vip/api/v1/watermark-by-url" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "image_url": "https://aigchub-static.oss-cn-beijing.aliyuncs.com/image-tools-api/examples/resize/original.jpg",
    "watermark_text": "STYLED WATERMARK",
    "position": "top-left",
    "font_size": 28,
    "font_color": "#FFFF00",
    "font_family": "Arial",
    "opacity": 0.9,
    "margin_x": 50,
    "margin_y": 50,
    "stroke_width": 3,
    "stroke_color": "#000000",
    "shadow_offset_x": 3,
    "shadow_offset_y": 3,
    "shadow_color": "#666666",
    "quality": 95
  }' \
  --output watermark_styled.jpg
```

## 📝 使用说明

1. **获取JWT Token**: 先调用登录接口获取认证令牌
2. **替换参数**: 将 `YOUR_JWT_TOKEN` 替换为实际的JWT令牌
3. **设置图片URL**: 将 `image_url` 替换为你要处理的图片URL
4. **调整参数**: 根据需要修改水印文字和样式参数
5. **执行请求**: 运行curl命令，处理后的图片将保存到指定文件

## ⚠️ 注意事项

- 所有接口都需要JWT认证
- 图片URL必须是可公开访问的
- 颜色值使用十六进制格式 (#RRGGBB)
- 透明度值范围为 0.0-1.0
- 质量值范围为 1-100
- 支持多种字体族和特效组合
