
# test_dify.py（单独运行，测试网络）
from fastapi import APIRouter
from mdurl import URL
import requests
import os
from app.core.config import settings

router = APIRouter(prefix="/api/v1/conversations", tags=["获取会话历史"])
@router.get("/messages")
def get_history(conversation_id: str,user_id: str):
    API_KEY = "app-Zjjvyq5hZUXgmpb9cFm2cbYu"  # 从环境变量获取API密钥
    URL = "https://api.dify.ai/v1/messages"

    headers = {
    "Authorization": f"Bearer {API_KEY}",
    # "Content-Type": "application/json"
    }
    data = {
    "conversation_id": conversation_id,  # 可选：指定会话ID，便于调试
    "user": user_id,  # 用户ID（字符串）
    "limit": 15

    }

    try:
        response = requests.get(url=URL, headers=headers, params=data, timeout=30)
        return response.json()  # 返回JSON格式的会话消息列表
    except Exception as e:
        print("访问失败：", str(e))


@router.get("/list")
def get_conversations(user_id:str,limit:int,sorted_by:str):
     API_KEY= "app-Zjjvyq5hZUXgmpb9cFm2cbYu"  # 从环境变量获取API密钥
     URL="https://api.dify.ai/v1/conversations"
     headers = {
    "Authorization": f"Bearer {API_KEY}",
    # "Content-Type": "application/json"
    }
     
     data={
    "user": user_id,  # 用户ID（字符串）
    "limit": limit,  # 返回会话列表的数量限制（整数）
    "sorted_by": sorted_by  # 排序方式（字符串，"created_at"或"updated_at"）
     }
     try:
        response = requests.get(url=URL, headers=headers, params=data, timeout=30)
        return response.json()  # 返回JSON格式的会话列表
     except Exception as e:
        print("访问失败：", str(e))
    
    