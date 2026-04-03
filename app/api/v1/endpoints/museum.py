# app/api/v1/endpoints/museum.py
import traceback

from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from app.api.schemas.request import MuseumQueryRequest
from app.api.schemas.response import BaseResponse, MuseumQueryData
from app.services.dify.main_agent import DifyMainAgentClient
from app.core.exceptions import DifyCallError, PermissionError
from app.api.v1.dependencies import api_dependencies
from app.core.logger import logger

router = APIRouter(prefix="/museum", tags=["文物查询"])
# 仅初始化主Agent客户端（无需子Agent）
main_agent_client = DifyMainAgentClient()

@router.post("/query", response_model=BaseResponse[MuseumQueryData])
def museum_query(
    request: MuseumQueryRequest,
    _: Any = Depends(api_dependencies)
) -> BaseResponse[MuseumQueryData]:
    """
    前端唯一接口：仅调用Dify主Agent（子Agent由主Agent自主调度）
    前端请求体：{"question": "商青铜树的高度？", "user_id": "user123"}
    """
    logger.info(f"收到文物查询请求：user_id={request.user_id}, question={request.question}")
    try:
        # 仅调用主Agent（子Agent由Dify内部处理）
        main_agent_result = main_agent_client.query(
            question=request.question,
            user_id=request.user_id
            
        )
        logger.info(f"主Agent返回结果：{main_agent_result}")
        # 封装为前端需要的格式（主Agent已聚合所有子Agent结果）
        response_data = MuseumQueryData(
            answer=main_agent_result["answer"],
            structured_data=None
        )

        return BaseResponse(code=200, msg="success", data=response_data)

    except PermissionError as e:
        return BaseResponse(code=403, msg=str(e), data=None)
    except DifyCallError as e:
        return BaseResponse(code=500, msg=f"主Agent调用失败：{str(e)}", data=None)
    except Exception as e:
        # 手动打印完整异常信息（关键！）
        error_type = type(e).__name__  # 异常类型（如TimeoutError/KeyError）
        error_msg = str(e)             # 异常信息
        error_stack = traceback.format_exc()  # 完整堆栈
        
        # 打印到控制台+日志
        print(f"\n===== 完整异常信息 =====")
        print(f"异常类型：{error_type}")
        print(f"异常信息：{error_msg}")
        print(f"完整堆栈：{error_stack}")
        print(f"=======================\n")
        
        logger.error(
            f"系统异常：user_id={request.user_id}, 类型={error_type}, 信息={error_msg}",
            exc_info=True
        )
        return BaseResponse(code=500, msg=f"系统异常：{str(e)}", data=None)