"""
常量定义：意图类型、响应码、限流规则等
"""

# 响应状态码
class ResponseCode:
    """API响应状态码"""
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500


# 意图类型
class IntentType:
    """用户查询意图类型"""
    ARTIFACT_QUERY = "artifact_query"  # 文物查询
    EXHIBITION_NAVIGATE = "exhibition_navigate"  # 展厅导航
    GENERAL_KNOWLEDGE = "general_knowledge"  # 通用知识
    UNCLEAR = "unclear"  # 不清楚的意图


# 用户等级
class UserLevel:
    """用户权限等级"""
    GUEST = "guest"  # 游客
    USER = "user"  # 普通用户
    VIP = "vip"  # VIP用户
    ADMIN = "admin"  # 管理员


# 限流规则
class RateLimit:
    """API请求限流规则"""
    GUEST_REQUESTS_PER_HOUR = 20
    USER_REQUESTS_PER_HOUR = 100
    VIP_REQUESTS_PER_HOUR = 500
    ADMIN_REQUESTS_PER_HOUR = 10000


# 缓存过期时间（秒）
class CacheExpire:
    """缓存过期时间配置"""
    QUERY_RESULT = 3600  # 1小时
    USER_SESSION = 86400  # 24小时
    ARTIFACT_INFO = 86400  # 24小时
    EXHIBITION_INFO = 86400  # 24小时
