# 阶段1：构建依赖（使用轻量Python基础镜像）
FROM python:3.10-slim AS builder

# 设置工作目录（容器内的目录，固定）
WORKDIR /app

# 安装系统依赖（解决requests等库的编译问题）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖清单到容器
COPY requirements.txt .

# 安装Python依赖到指定目录（方便后续拷贝）
# 国内用户添加-i参数用清华源加速！
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt -t /app/deps

# 阶段2：运行镜像（更小、更安全）
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 从构建阶段拷贝依赖到运行镜像
COPY --from=builder /app/deps /app/deps

# 将依赖目录加入Python路径
ENV PYTHONPATH="/app/deps:${PYTHONPATH-}"

# 复制项目代码到容器
COPY ./app /app/app

# 暴露FastAPI运行端口（和main.py中一致）
EXPOSE 8000

# 设置环境变量（替换为你的实际值，也可运行时传）
ARG DIFY_API_KEY="app-NwczDEtZuilcqutDdeli5Zbm"
ARG DIFY_API_URL="https://api.dify.ai/v1"
ARG DIFY_TIMEOUT=30
ARG DIFY_RETRY_TIMES=3

ENV DIFY_API_KEY=${DIFY_API_KEY} \
    DIFY_API_URL=${DIFY_API_URL} \
    DIFY_TIMEOUT=${DIFY_TIMEOUT} \
    DIFY_RETRY_TIMES=${DIFY_RETRY_TIMES}

# 启动命令（运行uvicorn，绑定0.0.0.0供外部访问）
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]