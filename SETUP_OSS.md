# OSS密钥配置说明

## 问题
GIF页面图片显示黑色是因为OSS密钥未配置，导致图片上传失败。

## 解决方法

### 方式1: 配置环境变量（推荐）
在 `.env` 文件中添加真实的OSS密钥：

```bash
# 编辑.env文件
nano .env

# 添加或修改以下两行：
ALIBABA_CLOUD_ACCESS_KEY_ID=你的AccessKeyId
ALIBABA_CLOUD_ACCESS_KEY_SECRET=你的AccessKeySecret
```

### 方式2: 临时环境变量
```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID="你的AccessKeyId"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="你的AccessKeySecret"

# 然后运行生成脚本
python3 scripts/generate_gif_pages_examples.py
```

### 方式3: 直接在脚本中配置（不推荐，仅用于测试）
创建一个临时脚本：

```python
#!/usr/bin/env python3
import os
os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'] = '你的AccessKeyId'
os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'] = '你的AccessKeySecret'

# 运行生成脚本
exec(open('scripts/generate_gif_pages_examples.py').read())
```

## 获取OSS密钥

1. 登录阿里云控制台
2. 进入 **AccessKey管理**
3. 创建或查看AccessKey
4. 复制 **AccessKeyId** 和 **AccessKeySecret**

## 验证配置

```bash
# 测试OSS连接
python3 -c "from app.services.oss_client import oss_client; print('Bucket:', oss_client.bucket_name); print('Key ID:', oss_client.access_key_id[:10] + '...')"
```

## 重新生成GIF图片

配置好OSS密钥后，运行：

```bash
python3 scripts/generate_gif_pages_examples.py
```

生成完成后，刷新页面查看效果。
