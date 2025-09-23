from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any

from ..middleware.auth_middleware import get_current_user, get_current_api_token
from ..services.billing_service import billing_service
from ..schemas.user_models import User
from ..utils.logger import logger


from ..schemas.response_models import ApiResponse
router = APIRouter(
    prefix="/api/v1/auth-example",
    tags=["认证示例"],
)


@router.get("/user-info")
async def get_user_info(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息（需要认证）"""
    return {
        "code": 200,
        "message": "获取用户信息成功",
        "data": {
            "id": current_user.id,
            "nickname": current_user.nickname,
            "phone": current_user.phone,
            "email": current_user.email,
            "token_balance": current_user.token_balance,
            "status": current_user.status
        }
    }


@router.post("/billing-example")
async def billing_example(
    request: Request,
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    api_token: str = Depends(get_current_api_token)
):
    """计费功能示例（需要认证）"""
    api_path = "/api/v1/auth-example/billing-example"
    
    # 1. 预扣费
    call_id = await billing_service.pre_charge(
        api_token=api_token,
        api_path=api_path,
        context=data,
        estimated_tokens=1,
        remark="计费功能示例"
    )
    
    if not call_id:
        raise HTTPException(
            status_code=402,
            detail="余额不足或预扣费失败"
        )
    
    try:
        # 2. 执行业务逻辑（这里只是示例）
        result = {
            "message": "业务逻辑执行成功",
            "input_data": data,
            "user": current_user.nickname,
            "call_id": call_id
        }
        
        # 3. 如果需要追加扣费（可选）
        # additional_tokens = calculate_additional_tokens(result)
        # if additional_tokens > 0:
        #     await billing_service.charge_more(call_id, additional_tokens)
        
        logger.info(f"用户 {current_user.nickname} 成功执行计费示例")
        
        return {
            "code": 200,
            "message": "执行成功",
            "data": result
        }
        
    except Exception as e:
        # 4. 业务逻辑执行失败，返还Token
        await billing_service.refund_all(call_id, f"业务逻辑执行失败: {str(e)}")
        logger.error(f"业务逻辑执行失败: {str(e)}")
        return {
            "code": 500,
            "message": f"执行失败: {str(e)}",
            "data": None
        }


@router.get("/public")
async def public_endpoint():
    """公开接口（不需要认证）"""
    return {
        "code": 200,
        "message": "这是一个公开接口，不需要认证",
        "data": {
            "timestamp": "2025-01-26",
            "service": "Image Tools API"
        }
    }
