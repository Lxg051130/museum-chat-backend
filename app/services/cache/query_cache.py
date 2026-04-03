"""
查询结果缓存：高频问题缓存
"""
import json
from typing import Optional, Dict, Any
from app.services.cache.base import CacheBase
from app.core.constants import CacheExpire
from app.core.logger import logger


class QueryCache(CacheBase):
    """查询结果缓存类"""
    
    async def get_query_result(self, question: str) -> Optional[Dict[str, Any]]:
        """
        获取缓存的查询结果
        
        Args:
            question: 查询问题
            
        Returns:
            缓存的查询结果
        """
        cache_key = f"query:{hash(question)}"
        
        try:
            cached = await self.get(cache_key)
            if cached:
                logger.info(f"命中查询缓存: {question}")
                return json.loads(cached)
            return None
        except Exception as e:
            logger.warning(f"缓存读取失败，继续执行: {str(e)}")
            return None
    
    async def set_query_result(self, question: str, result: Dict[str, Any]) -> None:
        """
        缓存查询结果
        
        Args:
            question: 查询问题
            result: 查询结果
        """
        cache_key = f"query:{hash(question)}"
        
        try:
            await self.set(
                cache_key,
                json.dumps(result),
                expire=CacheExpire.QUERY_RESULT
            )
        except Exception as e:
            logger.warning(f"结果缓存失败，continue: {str(e)}")
    
    async def get_user_session(self, user_id: int) -> Optional[Dict[str, Any]]:
        """获取用户会话缓存"""
        cache_key = f"session:{user_id}"
        
        try:
            cached = await self.get(cache_key)
            if cached:
                return json.loads(cached)
            return None
        except Exception as e:
            logger.warning(f"会话缓存读取失败: {str(e)}")
            return None
    
    async def set_user_session(self, user_id: int, session_data: Dict[str, Any]) -> None:
        """设置用户会话缓存"""
        cache_key = f"session:{user_id}"
        
        try:
            await self.set(
                cache_key,
                json.dumps(session_data),
                expire=CacheExpire.USER_SESSION
            )
        except Exception as e:
            logger.warning(f"会话缓存设置失败: {str(e)}")
