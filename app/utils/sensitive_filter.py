"""
敏感词过滤
"""
from typing import List, Tuple
from app.core.logger import logger


class SensitiveFilter:
    """敏感词过滤器"""
    
    # 敏感词列表（示例）
    SENSITIVE_WORDS = [
        "敏感词1",
        "敏感词2",
        "禁用词"
    ]
    
    @classmethod
    def filter_text(cls, text: str) -> Tuple[str, List[str]]:
        """
        过滤文本中的敏感词
        
        Args:
            text: 输入文本
            
        Returns:
            (过滤后的文本, 发现的敏感词列表)
        """
        found_words = []
        filtered_text = text
        
        for word in cls.SENSITIVE_WORDS:
            if word in filtered_text:
                found_words.append(word)
                filtered_text = filtered_text.replace(word, "*" * len(word))
        
        if found_words:
            logger.warning(f"发现敏感词: {found_words}")
        
        return filtered_text, found_words
    
    @classmethod
    def is_safe(cls, text: str) -> bool:
        """
        检查文本是否安全（不含敏感词）
        
        Args:
            text: 输入文本
            
        Returns:
            True表示安全，False表示含有敏感词
        """
        _, found_words = cls.filter_text(text)
        return len(found_words) == 0
