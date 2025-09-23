# 图像处理工具箱 (Image Tools API)

一个功能完整的图像处理工具箱，提供70+ 个API接口，支持从基础图像操作到高级艺术效果的一站式解决方案。

## 🌟 特性

- **70+ API接口** - 覆盖水印、裁剪、滤镜、色彩调整等各种功能
- **100+ 种效果** - 包括艺术滤镜、特效、图层混合等
- **在线测试** - 每个API都有对应的Web界面，支持实时预览
- **完整文档** - 内置API文档和使用示例
- **模块化设计** - 代码整洁，易于扩展

## 🚀 快速开始

### 一键启动（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd image-tools-api

# 一键启动（自动清理端口并启动服务）
./start.sh
```

启动完成后访问：
- 前端应用: http://localhost:58889
- 后端API: http://localhost:58888  
- API文档: http://localhost:58888/docs

### 端口管理

如果遇到端口占用问题，可以使用端口清理脚本：

```bash
# 清理端口（自动杀死占用58888和58889端口的进程）
./kill_ports.sh

# 然后启动服务
./start.sh
```

### 手动启动

#### 后端启动
```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python start_backend.py
```

#### 前端启动
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动前端服务
npm start
```

## 📦 安装依赖

### 后端依赖
```bash
pip install -r requirements.txt
```

### 前端依赖
```bash
cd frontend
npm install
```

## 🛠️ 功能列表

### 基础功能
- ✅ 水印添加 - 文字水印，支持位置、透明度、颜色、角度调整
- ✅ 尺寸调整 - 图片缩放，支持比例保持和质量控制
- ✅ 基础滤镜 - 灰度、褐色、模糊、锐化、亮度、对比度

### 艺术滤镜
- ✅ 油画效果、水彩效果、铅笔素描、彩色铅笔
- ✅ 干画笔、壁画效果、木刻效果、海报边缘、粗糙蜡笔

### 几何变换
- ✅ 图片裁剪 - 矩形、圆形、多边形、智能居中裁剪
- ✅ 图片旋转 - 自定义角度、90°/180°快速旋转
- ✅ 图片翻转 - 水平/垂直翻转
- ✅ 透视校正 - 手动四点校正、自动文档校正
- ✅ 画布调整 - 扩展画布、添加边框、修改比例

### 高级图像处理
- ✅ 色彩调整 - 色相/饱和度、色彩平衡、色阶、自动校正、色温调节、双色调
- ✅ 增强效果 - 运动模糊、径向模糊、表面模糊、USM锐化、智能锐化、边缘锐化
- ✅ 噪点处理 - 添加噪点（高斯/椒盐/胶片颗粒）、降噪处理
- ✅ 马赛克/像素化 - 全图/区域马赛克、复古像素艺术

### 图像合成
- ✅ 图层混合 - 正常、正片叠底、滤色、叠加
- ✅ 图片拼接 - 水平、垂直、网格拼接
- ✅ 高级文字 - 多行文字、描边文字、阴影文字

### 格式转换
- ✅ 支持格式 - JPEG、PNG、WebP、GIF、BMP、TIFF
- ✅ 格式信息 - EXIF数据读取

## 📸 界面预览

每个功能都有专门的测试页面，支持：
- 参数实时调整
- 图片在线预览
- API文档查看
- curl命令生成

## 🔧 API 使用示例

### 基础滤镜应用
```bash
curl -X POST "http://localhost:58888/filter/apply" \
  -F "file=@image.jpg" \
  -F "filter_type=grayscale"
```

### 艺术滤镜应用
```bash
curl -X POST "http://localhost:58888/art-filter/apply" \
  -F "file=@image.jpg" \
  -F "filter_name=oil_painting" \
  -F "radius=4" \
  -F "intensity=30"
```

### 格式转换
```bash
curl -X POST "http://localhost:58888/format/convert" \
  -F "file=@image.png" \
  -F "target_format=webp" \
  -F "quality=85"
```

## 📁 项目结构

```
image-tools-api/
├── app/                    # 后端代码
│   ├── main.py            # FastAPI主应用
│   ├── routers/           # API路由
│   ├── services/          # 业务逻辑
│   ├── filters/           # 滤镜实现
│   └── utils/             # 工具函数
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── pages/        # 功能页面
│   │   ├── components/   # 通用组件
│   │   └── config/       # 配置文件
│   └── public/
├── docs/                  # 项目文档
├── tests/                 # 测试代码
└── requirements.txt       # Python依赖
```

## 🤝 贡献

欢迎提交 Pull Request 或创建 Issue！

## 📄 License

MIT 