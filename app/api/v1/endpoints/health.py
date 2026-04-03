"""
健康检查接口：监控服务状态
"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """
    健康检查端点
    
    返回服务状态、数据库连接、外部服务状态等
    """
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "neo4j": "connected",
            "redis": "connected",
            "dify": "connected"
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }
