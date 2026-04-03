# app/services/dify/base.py
import requests  # 仅保留同步的requests，移除aiohttp
from typing import Dict, Any
from app.core.config import settings
from app.core.exceptions import DifyCallError

class DifyBaseClient:
    """Dify API通用调用基类（纯同步版，无任何异步代码）"""
    def __init__(self):
        self.api_key = settings.DIFY_API_KEY
        self.base_url = settings.DIFY_API_URL
        self.timeout = settings.DIFY_TIMEOUT  # 纯int类型（30秒），直接传给requests
        self.retry_times = settings.DIFY_RETRY_TIMES  # 重试次数

    def _request(self,path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        纯同步HTTP请求（仅用requests）
        :param method: HTTP方法（POST/GET）
        :param path: API路径（如/chat-messages）
        :param data: 请求体
        :return: Dify返回的JSON数据
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}{path}"

        # 重试逻辑
        for retry in range(self.retry_times + 1):
            try:
                # 关键修复：timeout参数传int类型（self.timeout=30），而非ClientTimeout对象
                response = requests.post(
                    url=url,
                    headers=headers,
                    json=data,
                    timeout=self.timeout  # ✅ 正确：int类型（30秒）
                )
                # 非200状态码抛异常
                response.raise_for_status()
                # 返回JSON结果
                return response.json()
            
            # 捕获requests的超时异常（单独处理）
            except requests.exceptions.Timeout:
                if retry == self.retry_times:
                    raise DifyCallError(f"Dify API调用超时（超时时间：{self.timeout}秒）")
                continue  # 重试
            
            # 捕获其他requests异常（连接错误、鉴权错误等）
            except requests.exceptions.RequestException as e:
                if retry == self.retry_times:
                    raise DifyCallError(f"Dify API调用失败：{str(e)}")
                continue

    def call_chat_messages(self, query: str, user_id: str, inputs: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        同步调用Dify的/chat-messages接口
        :param query: 用户问题
        :param user_id: 用户标识
        :param inputs: 必须为字典（Dify强制要求）
        :return: Dify原始返回数据
        """
        request_data = {
            "query": query,
            "inputs": {"contents": None},  # 主Agent的inputs仍为字典（Dify强制要求）
            "response_mode": "streaming",
            "conversation_id": "",
            "user": user_id,
            "files": []
        }
        return self._request("/chat-messages", request_data)