"""
数据转换：Dify结果转前端结构化数据
"""
from typing import Dict, Any, List
from app.core.logger import logger


class DataConverter:
    """数据转换工具类"""
    
    @staticmethod
    def convert_dify_response(dify_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        将Dify返回的数据转换为前端需要的格式
        
        Args:
            dify_response: Dify返回的原始数据
            
        Returns:
            转换后的结构化数据
        """
        try:
            return {
                "status": "success",
                "message": dify_response.get("answer", ""),
                "data": dify_response.get("data", {}),
                "metadata": {
                    "source": "dify",
                    "timestamp": dify_response.get("timestamp")
                }
            }
        except Exception as e:
            logger.error(f"Dify数据转换失败: {str(e)}")
            raise
    
    @staticmethod
    def convert_neo4j_artifacts(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        将Neo4j查询的文物记录转换为前端格式
        
        Args:
            records: Neo4j查询结果
            
        Returns:
            转换后的文物列表
        """
        try:
            artifacts = []
            for record in records:
                artifact = record.get("artifact", {})
                artifacts.append({
                    "id": artifact.get("id"),
                    "name": artifact.get("name"),
                    "description": artifact.get("description"),
                    "period": artifact.get("period"),
                    "material": artifact.get("material"),
                    "location": artifact.get("location"),
                    "image_url": artifact.get("image_url")
                })
            return artifacts
        except Exception as e:
            logger.error(f"Neo4j数据转换失败: {str(e)}")
            raise
