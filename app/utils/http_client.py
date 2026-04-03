"""
异步HTTP客户端：调用Dify、Neo4j API等
"""
import httpx
from typing import Optional, Dict, Any
from app.core.logger import logger


class HttpClient:
    """异步HTTP客户端"""
    
    def __init__(self, timeout: float = 30.0):
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """GET请求"""
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"GET请求失败: {url}, {str(e)}")
            raise
    
    async def post(self, url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """POST请求"""
        try:
            response = await self.client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"POST请求失败: {url}, {str(e)}")
            raise
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
