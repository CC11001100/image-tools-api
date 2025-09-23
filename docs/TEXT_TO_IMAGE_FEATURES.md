# 文字生图功能说明

## 功能概述

新增了两个强大的文字生图功能模块：

### 1. 文字图片生成 (`/text-to-image`)
从纯文字生成精美的图片，支持丰富的样式配置。

### 2. AI文生图 (`/ai-text-to-image`)
使用AI技术从文字描述生成图片，支持多种艺术风格。

## 文字图片生成功能

### 主要特性
- ✅ 多行文字支持，自动换行
- ✅ 丰富的字体选择
- ✅ 灵活的文字对齐方式（水平、垂直）
- ✅ 纯色和渐变背景支持
- ✅ 文字阴影效果
- ✅ 边框装饰
- ✅ 预设样式模板
- ✅ 自定义图片尺寸

### 支持的参数
```json
{
  "text": "要生成的文字内容",
  "width": 800,
  "height": 600,
  "font_size": 48,
  "font_family": "Arial",
  "font_color": "#000000",
  "background_color": "#FFFFFF",
  "background_style": "solid", // solid | gradient
  "text_align": "center", // left | center | right
  "vertical_align": "middle", // top | middle | bottom
  "padding": 50,
  "line_spacing": 1.2,
  "shadow": false,
  "shadow_color": "#808080",
  "shadow_offset_x": 2,
  "shadow_offset_y": 2,
  "border": false,
  "border_color": "#000000",
  "border_width": 2,
  "gradient_start": "#FF6B6B",
  "gradient_end": "#4ECDC4",
  "gradient_direction": "horizontal" // horizontal | vertical | diagonal
}
```

### 预设样式
- 经典白底黑字
- 深色主题
- 温暖渐变
- 海洋渐变
- 紫色梦幻
- 日落黄昏
- 森林绿意
- 商务蓝

### API端点
- `POST /text-to-image/create` - 生成文字图片
- `GET /text-to-image/presets` - 获取预设样式
- `GET /text-to-image/fonts` - 获取可用字体

## AI文生图功能

### 主要特性
- ✅ 支持自然语言描述
- ✅ 负向提示词控制
- ✅ 多种艺术风格
- ✅ 可调节的生成参数
- ✅ 随机种子控制
- ✅ 预设提示词模板

### 支持的风格
- 真实风格 (realistic)
- 动漫风格 (anime)
- 艺术风格 (artistic)
- 卡通风格 (cartoon)
- 油画风格 (oil_painting)
- 水彩风格 (watercolor)

### 生成参数
```json
{
  "prompt": "描述要生成的图片内容",
  "negative_prompt": "不想要的内容",
  "width": 512,
  "height": 512,
  "num_inference_steps": 20,
  "guidance_scale": 7.5,
  "seed": null,
  "style": "realistic"
}
```

### 预设模板
- 风景摄影
- 人物肖像
- 动物摄影
- 建筑设计
- 科幻场景
- 食物摄影

### API端点
- `POST /ai-text-to-image/generate` - 生成AI图片
- `GET /ai-text-to-image/styles` - 获取可用风格
- `GET /ai-text-to-image/presets` - 获取预设模板

## AI服务配置

### 支持的AI服务
1. **Stability AI** (推荐)
   - 需要配置 `STABILITY_API_KEY` 环境变量
   - 高质量图片生成

2. **HuggingFace**
   - 需要配置 `HUGGINGFACE_API_KEY` 环境变量
   - 免费额度支持

3. **演示服务**
   - 无需配置，自动回退
   - 生成带提示词的演示图片

### 配置方法
```bash
# 设置环境变量
export STABILITY_API_KEY="your_stability_api_key"
export HUGGINGFACE_API_KEY="your_huggingface_api_key"

# 或在 .env 文件中配置
STABILITY_API_KEY=your_stability_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

## 前端页面

### 访问路径
- 文字图片：`http://localhost:38888/text-to-image`
- AI文生图：`http://localhost:38888/ai-text-to-image`

### 菜单位置
在左侧导航栏的"文字生图"分组下：
- 文字图片
- AI文生图

## 使用示例

### 文字图片生成示例
```bash
curl -X POST "http://localhost:28888/text-to-image/create" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "欢迎使用\n文字生图功能",
    "width": 800,
    "height": 600,
    "background_style": "gradient",
    "gradient_start": "#667eea",
    "gradient_end": "#764ba2",
    "font_color": "#FFFFFF"
  }'
```

### AI文生图示例
```bash
curl -X POST "http://localhost:28888/ai-text-to-image/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful sunset landscape with mountains and lake, professional photography",
    "negative_prompt": "blurry, low quality",
    "style": "realistic"
  }'
```

## 技术实现

### 后端架构
- **路由层**：`app/routers/text_to_image.py`, `app/routers/ai_text_to_image.py`
- **服务层**：`app/services/text_to_image_service.py`, `app/services/ai_text_to_image_service.py`
- **图片处理**：使用 PIL (Pillow) 库
- **AI集成**：支持多种AI服务API

### 前端组件
- **文字图片页面**：`frontend/src/pages/TextToImagePage.tsx`
- **AI文生图页面**：`frontend/src/pages/AITextToImagePage.tsx`
- **菜单集成**：已添加到左侧导航栏

### 文件存储
- 生成的图片保存在 `public/generated/` 目录
- 通过 `/generated/` 路径提供静态文件服务
- 自动生成唯一文件名避免冲突

## 注意事项

1. **AI服务限制**：
   - 未配置API密钥时使用演示服务
   - 真实AI服务可能有使用限制和费用

2. **图片存储**：
   - 生成的图片会占用磁盘空间
   - 建议定期清理旧文件

3. **性能考虑**：
   - AI图片生成需要较长时间
   - 大尺寸图片生成会消耗更多资源

4. **浏览器兼容性**：
   - 前端使用现代React组件
   - 建议使用最新版本的浏览器 