"""
Redis连接/基础操作
"""
import redis.asyncio as redis
from typing import Optional, Any
import json
from app.core.config import settings
from app.core.exceptions import CacheException
from app.core.logger import logger


class CacheBase:
    """缓存基础操作类"""
    
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self._connect()
    
    async def _connect(self) -> None:
        """建立Redis连接"""
        try:
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            await self.redis.ping()
            logger.info("✅ Redis连接成功！")
        except Exception as e:
            logger.error(f"❌ Redis连接失败: {str(e)}")
            raise CacheException(f"Redis connection failed: {str(e)}") from e
    
    async def get(self, key: str) -> Optional[str]:
        """获取缓存值"""
        if not self.redis:
            await self._connect()
        
        try:
            value = await self.redis.get(key)
            return value
        except Exception as e:
            logger.error(f"缓存读取失败: {str(e)}")
            raise CacheException(f"Cache get failed: {str(e)}") from e
    
    async def set(self, key: str, value: str, expire: int = 3600) -> None:
        """设置缓存值"""
        if not self.redis:
            await self._connect()
        
        try:
            await self.redis.setex(key, expire, value)
        except Exception as e:
            logger.error(f"缓存写入失败: {str(e)}")
            raise CacheException(f"Cache set failed: {str(e)}") from e
    
    async def delete(self, key: str) -> None:
        """删除缓存"""
        if not self.redis:
            await self._connect()
        
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"缓存删除失败: {str(e)}")
            raise CacheException(f"Cache delete failed: {str(e)}") from e
    
    async def close(self) -> None:
        """关闭连接"""
        if self.redis:
            await self.redis.close()
            logger.info("✅ Redis连接已关闭")
