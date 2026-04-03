# app/core/logger.py
from loguru import logger
import sys

# 配置日志：输出到控制台 + 保存到文件，显示行号、函数名、错误堆栈
logger.remove()  # 移除默认配置
logger.add(
    sys.stdout,  # 控制台输出
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
    level="DEBUG"
)
logger.add(
    "logs/museum_chat.log",  # 日志文件（自动创建logs目录）
    rotation="100MB",  # 日志文件超过100MB自动分割
    retention="7 days",  # 保留7天日志
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
    level="DEBUG"
)

# 导出logger实例，供其他文件使用
logger = logger