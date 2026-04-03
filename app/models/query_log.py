"""
查询日志模型
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.models.base import BaseModel


class QueryLog(BaseModel):
    """查询日志模型"""
    __tablename__ = "query_logs"
    
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    question = Column(Text)
    answer = Column(Text, nullable=True)
    intent = Column(String(50))  # 用户意图分类
    agent_type = Column(String(50), nullable=True)  # 使用的Agent类型
    source = Column(String(50), nullable=True)  # dify 或 neo4j
    response_time = Column(Integer, nullable=True)  # ms
    
    def __repr__(self):
        return f"<QueryLog user_id={self.user_id} intent={self.intent}>"
