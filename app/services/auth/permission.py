"""
权限判断：管理员、普通用户等
"""
from typing import Optional
from app.core.constants import UserLevel
from app.core.exceptions import PermissionException
from app.core.logger import logger


class PermissionService:
    """权限管理服务类"""
    
    @staticmethod
    def check_admin(level: str) -> bool:
        """检查是否为管理员"""
        return level == UserLevel.ADMIN
    
    @staticmethod
    def check_vip(level: str) -> bool:
        """检查是否为VIP用户"""
        return level in [UserLevel.VIP, UserLevel.ADMIN]
    
    @staticmethod
    def check_user(level: str) -> bool:
        """检查是否为普通用户或更高级别"""
        return level in [UserLevel.USER, UserLevel.VIP, UserLevel.ADMIN]
    
    @staticmethod
    def verify_permission(user_level: str, required_level: str) -> None:
        """
        验证用户权限
        
        Args:
            user_level: 用户权限等级
            required_level: 需要的权限等级
            
        Raises:
            PermissionException: 权限不足
        """
        level_hierarchy = {
            UserLevel.GUEST: 0,
            UserLevel.USER: 1,
            UserLevel.VIP: 2,
            UserLevel.ADMIN: 3
        }
        
        user_level_value = level_hierarchy.get(user_level, 0)
        required_level_value = level_hierarchy.get(required_level, 1)
        
        if user_level_value < required_level_value:
            logger.warning(f"权限不足: user_level={user_level}, required={required_level}")
            raise PermissionException(f"Permission denied: required {required_level}")
