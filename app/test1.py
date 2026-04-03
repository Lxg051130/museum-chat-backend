# test_dify.py（单独运行，测试网络）
import json
from fastapi import APIRouter,Body
from fastapi.responses import StreamingResponse
import requests
import os
from app.api.schemas.request import MuseumQueryRequest
from app.core.config import settings


from app.core.exceptions import DifyCallError

router = APIRouter(prefix="/api/v1/museum", tags=["流式结果查询"])
def stream_response(query: str , user_id: str , conversation_id: str ):
    API_KEY = "app-Zjjvyq5hZUXgmpb9cFm2cbYu" # 从环境变量获取API密钥
    
    
    URL = "https://api.dify.ai/v1/chat-messages"

    headers = {
      "Authorization": f"Bearer {API_KEY}",
      "Content-Type": "application/json"
  }
    data = {
    "query": query,
    "inputs": {"contents": None},  # 主Agent的inputs仍为字典（Dify强制要求）
    "response_mode": "streaming",
    "user": user_id,
    "conversation_id": conversation_id  # 可选，前端可传入会话ID以保持上下文连续 
    }
    try:
     response = requests.post(URL, headers=headers, json=data, timeout=30,stream=True)
     print(response.text)
     full_answer = ""
     for line in response.iter_lines():
            
            if line:
                line_str = line.decode("utf-8").lstrip("data: ").strip()
                if not line_str:
                    continue
                try:
                    print(f"原始流式数据：{line_str}")
                    stream_data = json.loads(line_str)
                    final_conversation_id=conversation_id  # 默认使用前端传入的conversation_id
                    #提取会话id
                    if "conversation_id" in stream_data:
                        final_conversation_id = stream_data["conversation_id"]
                    if stream_data.get("event") == "agent_message":
                        print(True)
                        chunk = stream_data.get("answer", "")
                        full_answer += chunk
                        # 以 SSE 格式返回（前端可解析）
                        yield f"data: {json.dumps({'chunk': chunk, 'finished': False,'conversation_id': final_conversation_id})}\n\n"
                except json.JSONDecodeError:
                    continue
        # 流式结束，返回完整答案+结束标记
     yield f"data: {json.dumps({'chunk': '', 'finished': True, 'full_answer': full_answer, 'conversation_id': final_conversation_id})}\n\n"
    except requests.exceptions.RequestException as e:
     raise DifyCallError(f"Dify 流式调用失败：{str(e)}")

@router.post("/chat")
def museum_query_stream(requests: MuseumQueryRequest=Body(...)):
    return StreamingResponse(
            stream_response(requests.query, requests.user_id, requests.conversation_id),
            media_type="text/event-stream"  # SSE 媒体类型
        ) 

 


