"""
API路由注册
汇总所有endpoints到统一的API网关
"""
from fastapi import APIRouter
from app.api.v1.endpoints import museum, user, health

# 创建主路由
router = APIRouter(prefix="/api/v1")

# 注册各个子路由
router.include_router(museum.router)
router.include_router(user.router)
router.include_router(health.router)

__all__ = ["router"]
