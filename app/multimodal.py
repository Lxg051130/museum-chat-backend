import json
from fastapi import APIRouter, Form, HTTPException, UploadFile, File
import requests
import traceback

from app.core.config import settings

# 仅支持WAV格式（Dify官方支持）
SUPPORTED_FORMATS = ["wav"]
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15MB
router = APIRouter(prefix="/api/v1/multimodal", tags=["多模态"])

@router.post("/audio-to-text")
def audio_to_text(
    file: UploadFile = File(...),
    user: str = Form(...)
) -> str:
    """
    语音转文字（仅接收WAV格式，直接传给Dify）
    """
    # 1. 基础校验
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名称不能为空")
    
    # 校验文件后缀
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"仅支持WAV格式音频，当前文件格式：{file_ext}"
        )

    # 2. 读取文件并校验大小
    file_content = file.file.read()
    if len(file_content) == 0:
        raise HTTPException(status_code=400, detail="上传的音频文件为空")
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="音频文件大小超过15MB限制")

    # 3. 构造传给Dify的参数（纯WAV格式）
    files = {
        "file": (
            file.filename,          # WAV文件名
            file_content,           # 原生WAV字节流
            "audio/wav"             # 固定为WAV的MIME类型
        )
    }
    data = {"user": user}

    # 4. Dify接口配置
    API_KEY = settings.DIFY_API_KEY
    URL = "https://api.dify.ai/v1/audio-to-text"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        # 5. 发送请求（纯WAV格式）
        response = requests.post(
            URL,
            headers=headers,
            data=data,
            files=files,
            timeout=60,
            verify=False  # 解决Windows证书问题
        )

        # 打印完整调试信息
        print("="*50 + " Dify 请求详情 " + "="*50)
        print(f"[请求URL] {URL}")
        print(f"[文件信息] 名称：{file.filename} | 格式：audio/wav | 大小：{len(file_content)} 字节")
        print(f"[Dify响应状态码] {response.status_code}")
        print(f"[Dify响应内容] {response.text}")
        print("="*100)

        response.raise_for_status()
        result = response.json()
        
        # 提取文本结果
        text_result = result.get("text", "")
        if not text_result:
            raise HTTPException(status_code=500, detail="Dify返回空文本结果")

        # 返回结果（适配前端格式）
        return {"text": text_result}

    except Exception as e:
        # 打印完整错误栈
        error_stack = traceback.format_exc()
        error_detail = f"""
        调用Dify失败：{str(e)}
        Dify响应：{response.text if 'response' in locals() else '无响应'}
        错误栈：{error_stack}
        """
        print(error_detail)
        raise HTTPException(
            status_code=500,
            detail=f"语音转文字失败：{str(e)} | Dify响应：{response.text if 'response' in locals() else '无响应'}"
        )