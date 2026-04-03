"""
JWT生成/校验
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from app.core.config import settings
from app.core.exceptions import AuthException
from app.core.logger import logger


class JWTService:
    """JWT认证服务类"""
    
    @staticmethod
    def create_token(user_id: int, username: str, level: str = "user") -> str:
        """
        创建JWT令牌
        
        Args:
            user_id: 用户ID
            username: 用户名
            level: 用户等级
            
        Returns:
            JWT令牌
        """
        payload = {
            "user_id": user_id,
            "username": username,
            "level": level,
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
            "iat": datetime.utcnow()
        }
        
        try:
            token = jwt.encode(
                payload,
                settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM
            )
            logger.info(f"生成JWT令牌: user_id={user_id}, username={username}")
            return token
        except Exception as e:
            logger.error(f"JWT生成失败: {str(e)}")
            raise AuthException(f"Token creation failed: {str(e)}")
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """
        验证JWT令牌
        
        Args:
            token: JWT令牌
            
        Returns:
            令牌负载
            
        Raises:
            AuthException: 令牌无效或过期
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT令牌已过期")
            raise AuthException("Token expired", 401)
        except jwt.InvalidTokenError:
            logger.warning("JWT令牌无效")
            raise AuthException("Invalid token", 401)
