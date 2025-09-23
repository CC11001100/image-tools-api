from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class User(BaseModel):
    """用户信息模型"""
    id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: str
    token_balance: int
    created_at: datetime
    last_login_time: Optional[datetime] = None
    status: UserStatus
    api_token: str


class UserCenterResponse(BaseModel):
    """用户中心API响应模型"""
    code: int
    message: str
    data: Optional[User] = None


class BillingCallType(str, Enum):
    SIMPLE = "SIMPLE"
    COMPLEX = "COMPLEX"


class BillingOperationType(str, Enum):
    REFUND_ALL = "REFUND_ALL"
    CHARGE_MORE = "CHARGE_MORE"


class BillingStatus(str, Enum):
    PRE_CHARGED = "PRE_CHARGED"
    REFUNDED = "REFUNDED"
    COMPLETED = "COMPLETED"


class PreChargeRequest(BaseModel):
    """预扣费请求模型"""
    api_token: str
    api_path: str
    context: str
    call_type: BillingCallType
    estimated_tokens: int
    request_id: str
    request: str
    response: str = ""
    remark: str


class ActualChargeRequest(BaseModel):
    """实际扣费请求模型"""
    call_id: str
    operation_type: BillingOperationType
    additional_tokens: Optional[int] = None
    remark: str


class BillingData(BaseModel):
    """计费响应数据模型"""
    callId: str
    status: BillingStatus
    message: str
    remainingBalance: int


class BillingResponse(BaseModel):
    """计费响应模型"""
    code: int
    message: str
    data: Optional[BillingData] = None
