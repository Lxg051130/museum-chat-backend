"""
限流工具：IP/用户频率控制
"""
from typing import Optional
from app.core.constants import RateLimit, UserLevel
from app.core.exceptions import RateLimitException
from app.core.logger import logger


class RateLimiter:
    """限流控制器"""
    
    @staticmethod
    def get_limit(user_level: str) -> int:
        """
        根据用户等级获取限流数值（每小时请求数）
        
        Args:
            user_level: 用户等级
            
        Returns:
            每小时允许的请求数
        """
        limit_map = {
            UserLevel.GUEST: RateLimit.GUEST_REQUESTS_PER_HOUR,
            UserLevel.USER: RateLimit.USER_REQUESTS_PER_HOUR,
            UserLevel.VIP: RateLimit.VIP_REQUESTS_PER_HOUR,
            UserLevel.ADMIN: RateLimit.ADMIN_REQUESTS_PER_HOUR
        }
        return limit_map.get(user_level, RateLimit.GUEST_REQUESTS_PER_HOUR)
    
    @staticmethod
    def check_rate_limit(user_id: int, current_count: int, limit: int) -> None:
        """
        检查用户是否超过限流
        
        Args:
            user_id: 用户ID
            current_count: 当前请求数
            limit: 限流数值
            
        Raises:
            RateLimitException: 超过限流
        """
        if current_count >= limit:
            logger.warning(f"用户{user_id}超过限流: {current_count}/{limit}")
            raise RateLimitException(f"Rate limit exceeded: {current_count}/{limit}", 429)
