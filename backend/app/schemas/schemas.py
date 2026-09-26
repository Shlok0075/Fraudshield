from datetime import datetime
from pydantic import BaseModel,ConfigDict,EmailStr,Field
from app.models import AlertStatus,RiskLevel,UserRole
class UserCreate(BaseModel):
    email:EmailStr; password:str=Field(min_length=8); full_name:str|None=None; role:UserRole=UserRole.USER
class UserOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:str; email:EmailStr; full_name:str|None; role:UserRole; is_active:bool; created_at:datetime
class Token(BaseModel): access_token:str; token_type:str="bearer"
class RawTransactionFeatures(BaseModel):
    Time:float; Amount:float=Field(ge=0); V1:float; V2:float; V3:float; V4:float; V5:float; V6:float; V7:float; V8:float; V9:float; V10:float; V11:float; V12:float; V13:float; V14:float; V15:float; V16:float; V17:float; V18:float; V19:float; V20:float; V21:float; V22:float; V23:float; V24:float; V25:float; V26:float; V27:float; V28:float
class TransactionPredictRequest(BaseModel): features:RawTransactionFeatures; merchant_id:str|None=None; device_id:str|None=None
class ShapFeatureOut(BaseModel): feature:str; shap_value:float; direction:str
class PredictionOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    probability:float; risk_level:RiskLevel; action:str; escalated_for_amount:bool; explanation:list[ShapFeatureOut]=[]
class TransactionOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:str; amount:float; merchant_id:str|None; device_id:str|None; created_at:datetime; prediction:PredictionOut|None=None
class TransactionPredictResponse(BaseModel): transaction:TransactionOut; prediction:PredictionOut
class AlertOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:str; transaction_id:str; status:AlertStatus; assigned_to:str|None; notes:str|None; created_at:datetime; resolved_at:datetime|None
class AlertStatusUpdate(BaseModel): status:AlertStatus; notes:str|None=None
class AdminUserUpdate(BaseModel): role:UserRole|None=None; is_active:bool|None=None
class AuditLogOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:str; actor_id:str|None; action:str; entity_type:str; entity_id:str; details:str|None; created_at:datetime
