"""
用户模型
"""
from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import BaseModel


class User(BaseModel):
    """用户模型"""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    password_hash = Column(String(255))
    level = Column(String(20), default="user")  # guest, user, vip, admin
    is_active = Column(Boolean, default=True)
    last_login = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<User {self.username}>"
