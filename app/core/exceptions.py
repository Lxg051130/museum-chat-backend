"""
自定义异常：Dify调用失败、权限不足等
"""


class BaseException(Exception):
    """基础异常类"""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DifyException(BaseException):
    """Dify调用异常"""
    def __init__(self, message: str, code: int = 500):
        super().__init__(f"Dify Error: {message}", code)    


class Neo4jException(BaseException):
    """Neo4j数据库异常"""
    def __init__(self, message: str, code: int = 500):
        super().__init__(f"Neo4j Error: {message}", code)


class AuthException(BaseException):
    """认证异常"""
    def __init__(self, message: str = "Authentication failed", code: int = 401):
        super().__init__(f"Auth Error: {message}", code)


class PermissionError(BaseException):
    """权限异常"""
    def __init__(self, message: str = "Permission denied", code: int = 403):
        super().__init__(f"Permission Error: {message}", code)


class RateLimitException(BaseException):
    """限流异常"""
    def __init__(self, message: str = "Rate limit exceeded", code: int = 429):
        super().__init__(f"Rate Limit Error: {message}", code)


class CacheException(BaseException):
    """缓存异常"""
    def __init__(self, message: str, code: int = 500):
        super().__init__(f"Cache Error: {message}", code)


class DifyCallError(BaseException):
    """Dify API调用失败异常（超时、鉴权错误、参数错误等）"""
    def __init__(self, message: str, code: int = 500):
        super().__init__(f"Dify Call Error: {message}", code)