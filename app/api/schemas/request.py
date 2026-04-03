"""
前端请求参数模型（Pydantic）
"""
from fastapi import Body, UploadFile
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List


class MuseumQueryRequest(BaseModel):
    """查询请求模型"""
    query: str
    user_id: str
    conversation_id: Optional[str] = None  # 可选，前端可传入会话ID以保持上下文连续

class MuseumMultimodal_audio_to_text_Request(BaseModel):
    """多模态查询请求模型"""
    file: UploadFile
    user: str
class MuseumAudioDescriptionRequest(BaseModel):
    """文物描述请求模型"""
    user_tag: str=Body(..., description="用户标签，用于个性化描述")
    relic_id: str=Body(..., description="文物ID，指定要描述的文物,测试时用OBJ089就好")
    user_id: str=Body(..., description="用户ID，随便传一个字符串即可，用于Dify工作流的用户标识")

class NavigateRequest(BaseModel):
    """导航请求模型"""
    exhibition_id: str
    user_id: Optional[int] = None


class IntentRequest(BaseModel):
    """意图识别请求模型"""
    question: str


class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str
    password: str
