"""
全局配置：Dify/Neo4j/Redis/MySQL的连接信息
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用全局配置"""
    
    # 应用配置
    APP_NAME: str = "Museum Chat Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Neo4j配置
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    
    # Dify配置
    DIFY_API_URL: str = os.getenv("DIFY_API_URL", "http://localhost:8000")
    DIFY_API_KEY: str = os.getenv("DIFY_API_KEY", "")
    DIFY_MAIN_AGENT_ID: str = os.getenv("DIFY_MAIN_AGENT_ID", "")
    DIFY_TIMEOUT: int = int(os.getenv("DIFY_TIMEOUT", "30"))  # 秒
    DIFY_RETRY_TIMES: int = int(os.getenv("DIFY_RETRY_TIMES", "3"))
    
    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    
    # MySQL配置
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "museum_chat")
    
    # JWT配置
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
