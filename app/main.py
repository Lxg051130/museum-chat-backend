"""
FastAPI应用入口
初始化FastAPI、路由、中间件等
"""
import sys
from pathlib import Path

# 获取项目根目录（museum_chat_backend/）
PROJECT_ROOT = Path(__file__).parent.parent
# 把根目录加入 sys.path
sys.path.append(str(PROJECT_ROOT))

from fastapi import FastAPI, Request  # 新增：导入Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # 新增：导入JSONResponse
from fastapi.exceptions import RequestValidationError  # 新增：导入验证异常
from fastapi.encoders import jsonable_encoder  # 新增：导入编码工具
from app.core.config import settings
from app.core.logger import logger

from app.api.v1.router import router as v1_router
from app.test1 import router as test_router
from app.get_history import router as history_router
from app.multimodal import router as multi_router
from app.relic_description import router as audio_router

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# ===================== 新增：全局异常处理器（解决UnicodeDecodeError） =====================
# 1. 处理请求参数验证异常（核心修复）
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        # 容错编码：用replace替换无法解码的非UTF-8字符
        return JSONResponse(
            status_code=422,
            content={
                "detail": jsonable_encoder(
                    [
                        {
                            "loc": err["loc"],
                            "msg": err["msg"].encode('utf-8', errors='replace').decode('utf-8'),
                            "type": err["type"]
                        }
                        for err in exc.errors()
                    ]
                ),
                "error": "请求参数验证失败"
            },
        )
    except UnicodeDecodeError:
        # 终极容错：避免编码问题导致的二次报错
        return JSONResponse(
            status_code=422,
            content={"detail": "请求参数格式错误（含非UTF-8字符）", "error": "Validation Error"}
        )

# 2. 处理Unicode解码异常（兜底）
@app.exception_handler(UnicodeDecodeError)
async def unicode_decode_error_handler(request: Request, exc: UnicodeDecodeError):
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"数据编码解析失败：{exc.reason}（错误位置：{exc.start}）",
            "error": "Unicode Decode Error",
            "hint": "数据包含非UTF-8编码字符，已自动容错处理"
        }
    )
# ===================== 新增结束 =====================

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(test_router)  # 注册测试路由
app.include_router(history_router)  # 注册获取历史记录路由
# app.include_router(multi_router)  # 注册多模态路由
app.include_router(audio_router)  # 注册文物描述路由

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    

@app.get("/")
async def root():
    """根路由"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("启动博物馆智能问答后端服务...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )