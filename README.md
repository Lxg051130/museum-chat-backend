# Museum Chat Backend - 博物馆智能聊天后端项目文档

## 项目概述

博物馆智能聊天后端是一个基于FastAPI的AI聊天系统，集成了Dify多Agent调度、Neo4j知识图谱查询、Redis缓存等技术，为博物馆提供智能文物查询和展厅导航服务。

## 核心功能

- 🤖 **多Agent智能调度** - 通过Dify平台集成多个专业Agent
- 🔍 **知识图谱查询** - 基于Neo4j的文物信息查询
- 📍 **展厅导航** - 实时导航和路线规划
- 🔐 **用户认证** - JWT令牌及权限管理
- ⚡ **高性能缓存** - Redis缓存热点查询
- 📊 **查询日志** - 完整的查询记录和分析
- 🛡️ **安全防护** - 敏感词过滤、限流控制

## 项目结构

```
museum_chat_backend/
├── alembic/                      # 数据库迁移工具
├── app/                          # 核心应用代码
│   ├── api/                      # API网关
│   │   ├── v1/                   # API v1版本
│   │   │   ├── endpoints/        # 具体接口实现
│   │   │   │   ├── museum.py     # 文物查询/展厅导航
│   │   │   │   ├── user.py       # 用户相关接口
│   │   │   │   └── health.py     # 健康检查
│   │   │   ├── dependencies.py   # 依赖注入
│   │   │   └── router.py         # 路由注册
│   │   └── schemas/              # 请求/响应模型
│   │       ├── request.py        # 请求参数模型
│   │       └── response.py       # 响应模型
│   ├── core/                     # 核心配置
│   │   ├── config.py            # 全局配置
│   │   ├── constants.py         # 常量定义
│   │   ├── exceptions.py        # 自定义异常
│   │   └── logger.py            # 日志配置
│   ├── services/                 # 业务服务层
│   │   ├── dify/                # Dify服务
│   │   │   ├── base.py          # 基础调用类
│   │   │   ├── main_agent.py    # 主Agent
│   │   │   └── sub_agents.py    # 子Agent
│   │   ├── neo4j/               # Neo4j服务
│   │   │   ├── base.py          # 连接/操作
│   │   │   └── queries.py       # Cypher查询
│   │   ├── cache/               # 缓存服务
│   │   │   ├── base.py          # Redis基础类
│   │   │   └── query_cache.py   # 查询缓存
│   │   ├── auth/                # 权限服务
│   │   │   ├── jwt.py           # JWT处理
│   │   │   └── permission.py    # 权限检查
│   │   └── intent/              # 意图识别
│   │       └── classifier.py    # 分类器
│   ├── models/                   # 数据模型
│   │   ├── base.py              # 基础模型
│   │   ├── user.py              # 用户模型
│   │   └── query_log.py         # 查询日志模型
│   ├── utils/                    # 工具函数
│   │   ├── http_client.py       # HTTP客户端
│   │   ├── rate_limit.py        # 限流工具
│   │   ├── data_convert.py      # 数据转换
│   │   └── sensitive_filter.py  # 敏感词过滤
│   └── main.py                   # 应用入口
├── tests/                        # 测试代码
│   ├── api/                     # API接口测试
│   ├── services/                # 服务层测试
│   └── conftest.py              # 测试配置
├── .env.example                  # 环境变量示例
├── pyproject.toml               # 项目依赖配置
├── README.md                    # 项目文档
└── start.py                     # 启动脚本
```

## 快速开始

### 1. 环境准备

**系统要求：**
- Python >= 3.10
- Neo4j >= 5.0
- Redis >= 6.0
- MySQL >= 5.7

**依赖安装：**
```bash
# 使用Poetry
poetry install

# 或使用pip
pip install -r requirements.txt
```

### 2. 配置设置

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑.env文件，填入实际配置
nano .env
```

**关键配置项：**
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

DIFY_API_URL=http://localhost:8000
DIFY_API_KEY=your_api_key

REDIS_URL=redis://localhost:6379
MYSQL_DATABASE=museum_chat
```

### 3. 启动服务

```bash
# 启动开发服务器
python start.py

# 或直接使用uvicorn
uvicorn app.main:app --reload --port 8000

# 生产环境
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

访问 http://localhost:8000/docs 查看API文档（Swagger UI）

## API文档

### 文物查询接口

**请求：**
```bash
GET /api/v1/museum/query?question=秦朝文物&limit=10
```

**响应：**
```json
{
  "status": "success",
  "data": [
    {
      "id": "artifact_001",
      "name": "瓷碗",
      "period": "秦朝",
      "material": "陶瓷"
    }
  ],
  "message": "查询成功"
}
```



### 健康检查接口

**请求：**
```bash
GET /api/v1/health
```

**响应：**
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "neo4j": "connected",
    "redis": "connected",
    "dify": "connected"
  }
}
```

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/api/test_museum.py -v

# 生成覆盖率报告
pytest --cov=app tests/
```

## 部署

### Docker部署

```bash
# 构建镜像
docker build -t museum-chat-backend:1.0.0 .

# 启动容器
docker-compose up -d
```

### 生产环境部署

首先安装gunicorn：
```bash
pip install gunicorn
```

启动服务：
```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

## 故障排查

### Neo4j连接失败
```
❌ Neo4j连接失败：服务未启动或地址错误
```
**解决方案：**
1. 检查Neo4j服务是否启动
2. 验证NEO4J_URI、NEO4J_USER、NEO4J_PASSWORD配置
3. 确保防火墙允许7687端口

### Dify服务无响应
```
❌ Dify Error: Connection timeout
```
**解决方案：**
1. 检查Dify服务是否运行
2. 验证DIFY_API_URL和DIFY_API_KEY配置
3. 检查网络连接

### Redis连接失败
**解决方案：**
1. 启动Redis服务：`redis-server`
2. 验证REDIS_URL配置
3. 检查Redis密码配置

## 监控和日志

日志文件位置：
- 应用日志：`logs/app.log`
- 错误日志：`logs/error.log`

查看实时日志：
```bash
tail -f logs/app.log
```

## 性能优化建议

1. **缓存策略** - 为热点查询启用Redis缓存
2. **数据库优化** - 为Neo4j节点添加索引
3. **API限流** - 根据用户等级设置限流阈值
4. **异步处理** - 使用FastAPI异步特性处理I/O操作

## 许可证

MIT License

## 联系方式

技术支持：support@example.com

---

**更新时间：** 2024年1月1日
**版本：** v1.0.0
