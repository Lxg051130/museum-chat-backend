# app/services/dify/main_agent.py
from typing import Dict, Any
from app.services.dify.base import DifyBaseClient
from app.core.config import settings

class DifyMainAgentClient(DifyBaseClient):
    """仅封装Dify主Agent的调用（子Agent由主Agent内部调度）"""
    def __init__(self):
        # 仅传入主Agent的API密钥
        super().__init__()

    def query(self, question: str, user_id: str) -> Dict[str, Any]:
        """
        调用Dify主Agent的核心方法
        :param question: 用户原始问题
        :param user_id: 用户标识
        :return: 主Agent返回的最终结果（已聚合子Agent的回答）
        """
        # 调用Dify通用方法，参数仅需适配主Agent（子Agent由主Agent自主调用）
        raw_response = self.call_chat_messages(
            query=question,
            user_id=user_id,
            inputs={"contents": None}# 主Agent的inputs仍为字典（Dify强制要求）
        )
        
        # 解析主Agent返回的最终结果（已整合子Agent的回答）
        return {
            "answer": raw_response
        }