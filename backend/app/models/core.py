import enum,uuid
from datetime import datetime,timezone
from sqlalchemy import Boolean,DateTime,Enum,Float,ForeignKey,Integer,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database.session import Base

def _uuid(): return str(uuid.uuid4())
def _now(): return datetime.now(timezone.utc)
class UserRole(str,enum.Enum): ADMIN="admin"; ANALYST="analyst"; USER="user"
class RiskLevel(str,enum.Enum): LOW="low"; MEDIUM="medium"; HIGH="high"; CRITICAL="critical"
class AlertStatus(str,enum.Enum): OPEN="open"; REVIEWED="reviewed"; FALSE_POSITIVE="false_positive"; ESCALATED="escalated"; RESOLVED="resolved"
class User(Base):
    __tablename__="users"
    id:Mapped[str]=mapped_column(String,primary_key=True,default=_uuid); email:Mapped[str]=mapped_column(String,unique=True,index=True,nullable=False); hashed_password:Mapped[str]=mapped_column(String,nullable=False); full_name:Mapped[str]=mapped_column(String,nullable=True); role:Mapped[UserRole]=mapped_column(Enum(UserRole),default=UserRole.USER,nullable=False); is_active:Mapped[bool]=mapped_column(Boolean,default=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=_now)
class Merchant(Base):
    __tablename__="merchants"
    id:Mapped[str]=mapped_column(String,primary_key=True,default=_uuid); name:Mapped[str]=mapped_column(String,nullable=False); category:Mapped[str]=mapped_column(String,nullable=True); risk_rating:Mapped[float]=mapped_column(Float,default=0.0)
    transactions:Mapped[list["Transaction"]]=relationship(back_populates="merchant")
class Device(Base):
    __tablename__="devices"
    id:Mapped[str]=mapped_column(String,primary_key=True,default=_uuid); user_id:Mapped[str]=mapped_column(String,ForeignKey("users.id"),nullable=True); device_fingerprint:Mapped[str]=mapped_column(String,index=True,nullable=False); is_trusted:Mapped[bool]=mapped_column(Boolean,default=False); first_seen:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=_now)
    transactions:Mapped[list["Transaction"]]=relationship(back_populates="device")
class Transaction(Base):
    __tablename__="transactions"
    id:Mapped[str]=mapped_column(String,primary_key=True,default=_uuid); user_id:Mapped[str]=mapped_column(String,ForeignKey("users.id"),nullable=True); merchant_id:Mapped[str]=mapped_column(String,ForeignKey("merchants.id"),nullable=True); device_id:Mapped[str]=mapped_column(String,ForeignKey("devices.id"),nullable=True); amount:Mapped[float]=mapped_column(Float,nullable=False); raw_features:Mapped[str]=mapped_column(String,nullable=False); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=_now)
    merchant:Mapped["Merchant"]=relationship(back_populates="transactions"); device:Mapped["Device"]=relationship(back_populates="transactions"); prediction:Mapped["FraudPrediction"]=relationship(back_populates="transaction",uselist=False,cascade="all, delete-orphan"); alert:Mapped["FraudAlert"]=relationship(back_populates="transaction",uselist=False,cascade="all, delete-orphan")
class FraudPrediction(Base):
    __tablename__="fraud_predictions"
    id:Mapped[str]=mapped_column(String,primary_key=True,default=_uuid); transaction_id:Mapped[str]=mapped_column(String,ForeignKey("transactions.id"),unique=True,nullable=False); probability:Mapped[float]=mapped_column(Float,nullable=False); risk_level:Mapped[RiskLevel]=mapped_column(Enum(RiskLevel),nullable=False); action:Mapped[str]=mapped_column(String,nullable=False); escalated_for_amount:Mapped[bool]=mapped_column(Boolean,default=False); explanation_json:Mapped[str]=mapped_column(String,nullable=True); model_version:Mapped[str]=mapped_column(String,nullable=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=_now)
    transaction:Mapped["Transaction"]=relationship(back_populates="prediction")
    @property
    def explanation(self): import json; return json.loads(self.explanation_json) if self.explanation_json else []
class FraudAlert(Base):
    __tablename__="fraud_alerts"
    id:Mapped[str]=mapped_column(String,primary_key=True,default=_uuid); transaction_id:Mapped[str]=mapped_column(String,ForeignKey("transactions.id"),unique=True,nullable=False); status:Mapped[AlertStatus]=mapped_column(Enum(AlertStatus),default=AlertStatus.OPEN); assigned_to:Mapped[str]=mapped_column(String,ForeignKey("users.id"),nullable=True); notes:Mapped[str]=mapped_column(String,nullable=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=_now); resolved_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=True)
    transaction:Mapped["Transaction"]=relationship(back_populates="alert")
class AuditLog(Base):
    __tablename__="audit_logs"
    id:Mapped[str]=mapped_column(String,primary_key=True,default=_uuid); actor_id:Mapped[str]=mapped_column(String,ForeignKey("users.id"),nullable=True); action:Mapped[str]=mapped_column(String,nullable=False); entity_type:Mapped[str]=mapped_column(String,nullable=False); entity_id:Mapped[str]=mapped_column(String,nullable=False); details:Mapped[str]=mapped_column(String,nullable=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=_now)
