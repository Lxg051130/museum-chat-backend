"""
后端返回模型：标准化返回格式
"""
from pydantic import BaseModel
from typing import Optional, List, Any,Generic,TypeVar
from datetime import datetime

T=TypeVar('T')
class BaseResponse(BaseModel,Generic[T]):
    """标准API响应格式"""
    code: int  # 状态码
    msg: str
    data: Optional[T] = None
    


class ArtifactResponse(BaseModel):
    """文物查询返回模型"""
    id: str
    name: str
    description: str
    period: str
    material: str
    location: str
    image_url: Optional[str] = None

class MuseumQueryData(BaseModel):
    """博物馆查询返回模型"""
    answer: str
    structured_data: Optional[dict] = None  # 可选的结构化数据，如表格、图表等

class UserResponse(BaseModel):
    """用户信息返回模型"""
    id: int
    username: str
    email: Optional[str] = None
    level: str  # admin, user, guest
    created_at: datetime


class QueryHistoryResponse(BaseModel):
    """查询历史返回模型"""
    id: str
    user_id: int
    question: str
    answer: str
    intent: str
    created_at: datetime
