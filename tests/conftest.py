"""
测试配置（Pytest夹具）
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI测试客户端"""
    return TestClient(app)


@pytest.fixture
def test_user():
    """测试用户数据"""
    return {
        "username": "testuser",
        "password": "testpass123",
        "email": "test@example.com"
    }


@pytest.fixture
def test_token():
    """测试JWT令牌"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjogMSwgInVzZXJuYW1lIjogInRlc3QiLCAibGV2ZWwiOiAidXNlciJ9.test_signature"
