# app/api/v1/dependencies.py
from fastapi import Depends, HTTPException, Request
import time
from app.core.exceptions import PermissionError

# 简单限流存储
rate_limit_store: dict[str, list[int]] = {}

async def check_permission(user_id: int) -> bool:
    """权限校验：仅允许指定用户"""
    allowed_users = [123, 456]
    if user_id not in allowed_users:
        raise PermissionError("无查询权限")
    return True

async def rate_limit(request: Request, user_id: int) -> bool:
    """限流：1分钟最多10次请求"""
    now = int(time.time())
    rate_limit_store[user_id] = [t for t in rate_limit_store.get(user_id, []) if t > now - 60]
    if len(rate_limit_store[user_id]) >= 10:
        raise HTTPException(status_code=429, detail="请求频繁，请稍后再试")
    rate_limit_store[user_id].append(now)
    return True

async def api_dependencies(request: Request) -> None:
    """组合依赖：权限+限流"""
    # 从请求体解析user_id
    body = await request.json()
    user_id = body.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id不能为空")
    await check_permission(user_id)
    await rate_limit(request, user_id)