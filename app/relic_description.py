import json
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import StreamingResponse
import requests
import os
from app.api.schemas.request import MuseumAudioDescriptionRequest, MuseumQueryRequest
from app.core.config import settings

from app.core.exceptions import DifyCallError

router = APIRouter(prefix="/api/v1/museum", tags=["返回文物音频讲解"])

# 修正路由装饰器（补充@符号，原代码漏写）
@router.post("/get_audio",responses={
        200: {
            "description": "成功返回流式音频（wav格式），可直接播放",
            "content": {
                "audio/wav": {
                    "schema": {
                        "type": "string",
                        "format": "binary"  # 标识为二进制流式数据
                    }
                }
            }
        },
        400: {"description": "Dify返回的音频URL无效/无法访问"},
        500: {
            "description": "Workflow执行失败/解析SSE数据失败/代理音频失败",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string", "example": "代理音频失败：Connection timeout"}
                        }
                    }
                }
            }
        }
    })
def user_tag_description(request: MuseumAudioDescriptionRequest = Body(...)):
    API_KEY = "app-X7jKBJ0GWR3vd2LArqLDIGO8" 
    URL = "https://api.dify.ai/v1/workflows/run"
    headers = {
      "Authorization": f"Bearer {API_KEY}",
      "Content-Type": "application/json"
  }
    data= {
        "inputs": {
            "user_tag": request.user_tag,
            "relic_id": request.relic_id
        },
        "response_mode": "streaming",
        "user": request.user_id,
    }
    final_output = {}  
    response = requests.post(URL, headers=headers, json=data, timeout=30, stream=True)
    # 4. 逐行解析 SSE 流式数据
    for line in response.iter_lines():
        if not line:
            continue
        
        # 去除前缀 "data: "，只保留 JSON 部分
        line = line.decode("utf-8").strip()
        if not line.startswith("data: "):
            continue
        json_str = line[len("data: "):].strip()
        if not json_str:
            continue

        # 解析 JSON 数据
        try:
            data = json.loads(json_str)
            event_type = data.get("event")
            event_data = data.get("data", {})

            # ========== 核心：提取 workflow_finished 事件（最终输出） ==========
            if event_type == "workflow_finished":
                workflow_status = event_data.get("status")
                # 工作流成功：提取 outputs（最终输出）
                if workflow_status == "succeeded":
                    final_output = event_data.get("outputs", {})
                # 工作流失败：提取错误信息
                else:
                    error_message = event_data.get("error", "Workflow 执行失败")
                
                # 工作流结束，可提前退出循环
                break
        except json.JSONDecodeError as e:
            print(f"解析 SSE 数据失败：{e}，原始数据：{json_str}")
            continue    

    audio_url=final_output.get("file")[0].get("url", "")
    try:
        # 同步获取音频流（替换异步aiohttp为同步requests）
        resp = requests.get(audio_url, timeout=30, stream=True)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="音频 URL 无法访问")
        
        # 同步流式转发给前端
        def audio_stream():
            for chunk in resp.iter_content(chunk_size=1024*1024):  # 1MB 分片
                yield chunk
        
        # 返回流式响应，指定音频格式
        return StreamingResponse(
            audio_stream(),
            media_type="audio/wav",  # 根据实际格式调整（如 audio/webm）
            headers={
                "Content-Disposition": 'inline; filename="audio.wav"',  # 前端可直接播放
                "Access-Control-Allow-Origin": "*"  # 跨域保障
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"代理音频失败：{str(e)}")

    # return tag_description_mapping.get(user_tag, "未知标签，无法提供描述。")