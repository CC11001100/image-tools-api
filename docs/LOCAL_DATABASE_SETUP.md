# 本地数据库配置说明

**配置时间**: 2024-11-22  
**状态**: ✅ 已完成并测试通过

---

## 📋 配置概览

已成功配置本地MySQL和Redis连接：
- ✅ MySQL: 127.0.0.1:3306
- ✅ Redis: 127.0.0.1:6379

---

## 🔧 配置详情

### MySQL配置
```
主机: 127.0.0.1
端口: 3306
用户: root
密码: cC11001100
数据库: image_tools_api
```

### Redis配置
```
主机: 127.0.0.1
端口: 6379
密码: (无)
数据库: 0
```

---

## 📝 修改的文件

### 1. 环境变量配置 (`.env`)
创建了本地环境变量文件：
```bash
# MySQL配置
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=cC11001100
MYSQL_DATABASE=image_tools_api

# Redis配置
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
```

### 2. 配置类 (`app/config.py`)
添加了MySQL和Redis配置项：
```python
# MySQL配置
MYSQL_HOST: str = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "image_tools_api")

# Redis配置
REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
```

添加了辅助方法：
```python
@classmethod
def get_mysql_url(cls) -> str:
    """获取MySQL连接URL"""
    password = quote_plus(cls.MYSQL_PASSWORD) if cls.MYSQL_PASSWORD else ""
    return f"mysql+pymysql://{cls.MYSQL_USER}:{password}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}?charset=utf8mb4"

@classmethod
def get_redis_url(cls) -> str:
    """获取Redis连接URL"""
    if cls.REDIS_PASSWORD:
        return f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
    return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
```

### 3. 数据库连接模块 (`app/database.py`)
新建文件，提供MySQL和Redis连接：
```python
# MySQL配置
engine = create_engine(
    config.get_mysql_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis配置
redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD if config.REDIS_PASSWORD else None,
    db=config.REDIS_DB,
    decode_responses=True
)
```

提供辅助函数：
```python
def get_db():
    """获取数据库会话"""
    
def get_redis():
    """获取Redis客户端"""
```

### 4. 健康检查端点 (`app/main.py`)
更新了 `/api/health` 端点，添加数据库连接状态检查：
```python
@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    # 检查MySQL连接
    # 检查Redis连接
    # 返回详细状态
```

### 5. 依赖包 (`requirements.txt`)
添加了数据库相关依赖：
```
pymysql>=1.1.0
redis>=5.0.0
sqlalchemy>=2.0.0
```

### 6. 启动脚本 (`start_backend.py`)
添加了环境变量加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🚀 启动服务

### 1. 确保MySQL和Redis已启动
```bash
# 检查MySQL
mysql -h 127.0.0.1 -u root -p

# 检查Redis
redis-cli ping
```

### 2. 创建数据库
```bash
mysql -h 127.0.0.1 -u root -pcC11001100 -e "CREATE DATABASE IF NOT EXISTS image_tools_api CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 3. 启动服务
```bash
./start.sh
```

### 4. 检查连接状态
```bash
curl http://localhost:58888/api/health | python3 -m json.tool
```

---

## ✅ 健康检查响应示例

```json
{
    "code": 200,
    "message": "服务健康状态正常",
    "data": {
        "service": "Image Tools API",
        "version": "1.0.0",
        "status": "running",
        "database": {
            "status": "connected",
            "host": "127.0.0.1",
            "port": 3306,
            "database": "image_tools_api"
        },
        "redis": {
            "status": "connected",
            "host": "127.0.0.1",
            "port": 6379,
            "db": 0
        }
    }
}
```

---

## 📊 访问地址

- **前端界面**: http://localhost:58889
- **API文档**: http://localhost:58888/docs
- **健康检查**: http://localhost:58888/api/health

---

## 🔍 故障排查

### MySQL连接失败
1. 检查MySQL服务是否启动
2. 检查用户名密码是否正确
3. 检查数据库是否存在
4. 检查.env文件是否正确加载

### Redis连接失败
1. 检查Redis服务是否启动
2. 使用 `redis-cli ping` 测试连接
3. 检查端口是否正确

### 环境变量未加载
1. 确认.env文件存在于项目根目录
2. 确认start_backend.py包含load_dotenv()
3. 重启服务

---

## 📝 使用示例

### Python代码中使用MySQL
```python
from app.database import get_db

def some_function():
    db = next(get_db())
    try:
        # 使用db进行数据库操作
        result = db.query(...)
    finally:
        db.close()
```

### Python代码中使用Redis
```python
from app.database import get_redis

def some_function():
    redis_client = get_redis()
    if redis_client:
        # 使用redis_client进行操作
        redis_client.set("key", "value")
        value = redis_client.get("key")
```

---

## 🎯 后续工作

### 建议添加的功能
1. ✅ 数据库连接池配置
2. ✅ 健康检查端点
3. ⏳ 数据库迁移工具（Alembic）
4. ⏳ Redis缓存策略
5. ⏳ 数据模型定义
6. ⏳ 数据库操作封装

### 性能优化
1. 连接池大小调优
2. Redis缓存策略优化
3. 数据库索引优化
4. 查询性能监控

---

## 📌 注意事项

1. **.env文件安全**: .env文件已加入.gitignore，不会被提交到代码仓库
2. **密码安全**: 生产环境应使用更强的密码
3. **连接池**: 已配置pool_pre_ping和pool_recycle，确保连接有效性
4. **错误处理**: 数据库连接失败不会影响服务启动
5. **日志记录**: 连接状态会记录到日志中

---

**配置完成 ✅**

MySQL和Redis已成功集成到本地开发环境中，可以通过健康检查端点实时查看连接状态。
