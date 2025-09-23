import uuid
import json
from typing import Optional, Dict, Any
from datetime import datetime

from ..services.user_center_client import user_center_client
from ..schemas.user_models import (
    PreChargeRequest, ActualChargeRequest, BillingCallType, 
    BillingOperationType, BillingResponse
)
from ..config import config
from ..utils.logger import logger


class BillingService:
    """计费服务"""
    
    def __init__(self):
        self.default_token_cost = config.DEFAULT_TOKEN_COST
    
    def generate_request_id(self) -> str:
        """生成唯一的请求ID"""
        return f"req_{uuid.uuid4().hex}"
    
    async def pre_charge(
        self,
        api_token: str,
        api_path: str,
        context: Dict[str, Any],
        estimated_tokens: int = None,
        call_type: BillingCallType = BillingCallType.SIMPLE,
        remark: str = ""
    ) -> Optional[str]:
        """
        预扣费

        Args:
            api_token: 用户API token
            api_path: API路径
            context: 请求上下文
            estimated_tokens: 预估token数量
            call_type: 调用类型
            remark: 备注

        Returns:
            call_id: 成功时返回调用ID，失败时返回None
        """
        if estimated_tokens is None:
            estimated_tokens = self.default_token_cost

        # 开发模式：直接返回模拟的call_id
        if config.DEVELOPMENT_MODE:
            mock_call_id = f"dev_call_{uuid.uuid4().hex[:8]}"
            logger.info(f"开发模式：模拟预扣费成功 {mock_call_id}, 预估tokens: {estimated_tokens}")
            return mock_call_id

        request_id = self.generate_request_id()

        pre_charge_request = PreChargeRequest(
            api_token=api_token,
            api_path=api_path,
            context=json.dumps(context, ensure_ascii=False),
            call_type=call_type,
            estimated_tokens=estimated_tokens,
            request_id=request_id,
            request=json.dumps(context, ensure_ascii=False),
            response="",
            remark=remark or f"{api_path}请求"
        )

        try:
            response = await user_center_client.pre_charge(pre_charge_request)

            if response and response.code == 200 and response.data:
                logger.info(f"预扣费成功: {response.data.callId}, 剩余余额: {response.data.remainingBalance}")
                return response.data.callId
            else:
                error_msg = response.message if response else "预扣费请求失败"
                logger.error(f"预扣费失败: {error_msg}")
                return None

        except Exception as e:
            logger.error(f"预扣费异常: {str(e)}")
            return None
    
    async def refund_all(self, call_id: str, remark: str = "API调用失败，返还Token") -> bool:
        """
        返还所有Token

        Args:
            call_id: 调用ID
            remark: 备注

        Returns:
            是否成功
        """
        # 开发模式：直接返回成功
        if config.DEVELOPMENT_MODE:
            logger.info(f"开发模式：模拟退费成功 {call_id}")
            return True

        request = ActualChargeRequest(
            call_id=call_id,
            operation_type=BillingOperationType.REFUND_ALL,
            remark=remark
        )

        try:
            response = await user_center_client.actual_charge(request)

            if response and response.code == 200:
                logger.info(f"退费成功: {call_id}")
                return True
            else:
                error_msg = response.message if response else "退费请求失败"
                logger.error(f"退费失败: {error_msg}")
                return False

        except Exception as e:
            logger.error(f"退费异常: {str(e)}")
            return False
    
    async def charge_more(
        self,
        call_id: str,
        additional_tokens: int,
        remark: str = "API调用超出预期，追加扣除Token"
    ) -> bool:
        """
        追加扣费

        Args:
            call_id: 调用ID
            additional_tokens: 追加token数量
            remark: 备注

        Returns:
            是否成功（追加扣费失败也返回True，因为已经预扣费过了）
        """
        # 开发模式：直接返回成功
        if config.DEVELOPMENT_MODE:
            logger.info(f"开发模式：模拟追加扣费成功 {call_id}, 追加: {additional_tokens} tokens")
            return True

        request = ActualChargeRequest(
            call_id=call_id,
            operation_type=BillingOperationType.CHARGE_MORE,
            additional_tokens=additional_tokens,
            remark=remark
        )

        try:
            response = await user_center_client.actual_charge(request)

            if response and response.code == 200:
                logger.info(f"追加扣费成功: {call_id}, 追加: {additional_tokens} tokens")
                return True
            else:
                # 追加扣费失败时也返回True，因为已经预扣费过了
                error_msg = response.message if response else "追加扣费请求失败"
                logger.warning(f"追加扣费失败，但继续执行: {error_msg}")
                return True

        except Exception as e:
            logger.warning(f"追加扣费异常，但继续执行: {str(e)}")
            return True


# 全局计费服务实例
billing_service = BillingService()
