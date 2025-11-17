"""
计费相关的路由端点
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from ..middleware.auth_middleware import get_current_user
from ..schemas.user_models import User
from ..services.billing_service import billing_service
from ..schemas.response_models import ApiResponse
from ..utils.logger import logger
from decimal import Decimal

router = APIRouter(
    prefix="/api/billing",
    tags=["计费管理"]
)

@router.get("/balance")
async def get_balance(
    current_user: User = Depends(get_current_user)
):
    """
    获取用户余额
    """
    try:
        # 获取用户余额
        balance = await billing_service.get_user_balance(current_user.user_id)
        
        logger.info(f"用户 {current_user.nickname} 查询余额: {balance}")
        
        return ApiResponse.success(
            message="余额查询成功",
            data={
                "user_id": current_user.user_id,
                "username": current_user.nickname,
                "balance": float(balance),
                "currency": "USD"
            }
        )
        
    except Exception as e:
        logger.error(f"查询余额失败: {str(e)}")
        return ApiResponse.error(
            message=f"查询余额失败: {str(e)}",
            code=500
        )

@router.get("/history")
async def get_billing_history(
    current_user: User = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    """
    获取用户计费历史
    """
    try:
        # 获取计费历史
        history = await billing_service.get_billing_history(
            current_user.user_id,
            limit=limit,
            offset=offset
        )
        
        logger.info(f"用户 {current_user.nickname} 查询计费历史, 返回 {len(history)} 条记录")
        
        return ApiResponse.success(
            message="计费历史查询成功",
            data={
                "user_id": current_user.user_id,
                "history": history,
                "total": len(history),
                "limit": limit,
                "offset": offset
            }
        )
        
    except Exception as e:
        logger.error(f"查询计费历史失败: {str(e)}")
        return ApiResponse.error(
            message=f"查询计费历史失败: {str(e)}",
            code=500
        )

@router.post("/charge")
async def charge_user(
    amount: float,
    operation: str,
    description: str = "",
    current_user: User = Depends(get_current_user)
):
    """
    对用户账户扣费（内部API，用于处理消费）
    """
    try:
        # 验证扣费金额
        if amount <= 0:
            return ApiResponse.error(
                message="扣费金额必须大于0",
                code=400
            )
        
        # 执行扣费
        success = await billing_service.charge_user(
            user_id=current_user.user_id,
            amount=Decimal(str(amount)),
            operation=operation,
            description=description
        )
        
        if success:
            # 获取更新后的余额
            new_balance = await billing_service.get_user_balance(current_user.user_id)
            
            logger.info(f"用户 {current_user.nickname} 扣费成功: {amount} USD, 操作: {operation}")
            
            return ApiResponse.success(
                message="扣费成功",
                data={
                    "user_id": current_user.user_id,
                    "charged_amount": amount,
                    "operation": operation,
                    "new_balance": float(new_balance),
                    "description": description
                }
            )
        else:
            return ApiResponse.error(
                message="余额不足，扣费失败",
                code=402  # Payment Required
            )
            
    except Exception as e:
        logger.error(f"扣费失败: {str(e)}")
        return ApiResponse.error(
            message=f"扣费失败: {str(e)}",
            code=500
        ) 