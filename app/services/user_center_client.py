import httpx
import json
from typing import Optional
from ..config import config
from ..schemas.user_models import (
    User, UserCenterResponse, PreChargeRequest, ActualChargeRequest, 
    BillingResponse, BillingCallType, BillingOperationType
)
from ..utils.logger import logger


class UserCenterClient:
    """用户中心API客户端"""
    
    def __init__(self):
        self.base_url = config.USER_CENTER_BASE_URL
        self.headers = config.get_user_center_headers()
        self.timeout = config.API_TIMEOUT
    
    async def get_user_by_jwt_token(self, jwt_token: str) -> Optional[User]:
        """根据JWT token查询用户信息"""
        try:
            url = f"{self.base_url}/api/internal/users/by-jwt-token/{jwt_token}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self.headers)
                
            if response.status_code != 200:
                logger.error(f"用户中心API请求失败: {response.status_code} - {response.text}")
                return None
                
            data = response.json()
            user_response = UserCenterResponse(**data)
            
            if user_response.code != 200:
                logger.error(f"用户中心返回错误: {user_response.message}")
                return None
                
            return user_response.data
            
        except Exception as e:
            logger.error(f"查询用户信息失败: {str(e)}")
            return None
    
    async def get_user_by_api_token(self, api_token: str) -> Optional[User]:
        """根据API token查询用户信息"""
        try:
            url = f"{self.base_url}/api/internal/users/by-api-token/{api_token}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self.headers)
                
            if response.status_code != 200:
                logger.error(f"用户中心API请求失败: {response.status_code} - {response.text}")
                return None
                
            data = response.json()
            user_response = UserCenterResponse(**data)
            
            if user_response.code != 200:
                logger.error(f"用户中心返回错误: {user_response.message}")
                return None
                
            return user_response.data
            
        except Exception as e:
            logger.error(f"查询用户信息失败: {str(e)}")
            return None
    
    async def pre_charge(self, request: PreChargeRequest) -> Optional[BillingResponse]:
        """预扣费"""
        try:
            url = f"{self.base_url}/api/internal/billing/charge"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url, 
                    headers=self.headers,
                    json=request.dict()
                )
                
            if response.status_code != 200:
                logger.error(f"预扣费API请求失败: {response.status_code} - {response.text}")
                return None
                
            data = response.json()
            billing_response = BillingResponse(**data)
            
            if billing_response.code != 200:
                logger.error(f"预扣费失败: {billing_response.message}")
                return billing_response
                
            logger.info(f"预扣费成功: {billing_response.data.callId}")
            return billing_response
            
        except Exception as e:
            logger.error(f"预扣费请求失败: {str(e)}")
            return None
    
    async def actual_charge(self, request: ActualChargeRequest) -> Optional[BillingResponse]:
        """实际扣费（返还或追加）"""
        try:
            url = f"{self.base_url}/api/internal/billing/actual-charge"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url, 
                    headers=self.headers,
                    json=request.dict()
                )
                
            if response.status_code != 200:
                logger.error(f"实际扣费API请求失败: {response.status_code} - {response.text}")
                return None
                
            data = response.json()
            billing_response = BillingResponse(**data)
            
            # 追加扣费失败时也正常返回，因为已经预扣费过了
            if billing_response.code != 200 and request.operation_type == BillingOperationType.CHARGE_MORE:
                logger.warning(f"追加扣费失败，但继续执行: {billing_response.message}")
                return billing_response
            elif billing_response.code != 200:
                logger.error(f"实际扣费失败: {billing_response.message}")
                return billing_response
                
            logger.info(f"实际扣费成功: {billing_response.data.callId}")
            return billing_response
            
        except Exception as e:
            logger.error(f"实际扣费请求失败: {str(e)}")
            return None


# 全局用户中心客户端实例
user_center_client = UserCenterClient()
