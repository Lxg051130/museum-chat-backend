"""
用户相关接口：登录/权限/历史查询
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
async def login(username: str, password: str):
    """
    用户登录接口
    
    Args:
        username: 用户名
        password: 密码
        
    Returns:
        JWT令牌
    """
    # TODO: 验证用户名密码，生成JWT
    return {
        "status": "success",
        "token": "xxx",
        "user": {
            "id": 1,
            "username": username,
            "level": "user"
        }
    }


@router.get("/history")
async def get_query_history(user_id: int, limit: int = 20):
    """
    获取用户查询历史
    
    Args:
        user_id: 用户ID
        limit: 返回记录数
        
    Returns:
        查询历史列表
    """
    # TODO: 从数据库查询用户历史
    return {
        "status": "success",
        "data": [],
        "total": 0
    }


@router.get("/permissions")
async def get_permissions(user_id: int):
    """
    获取用户权限信息
    """
    # TODO: 查询用户权限
    return {
        "status": "success",
        "permissions": []
    }
