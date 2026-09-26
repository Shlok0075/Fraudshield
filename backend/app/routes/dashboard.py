from fastapi import APIRouter,Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models import Transaction,FraudAlert,RiskLevel,User
router=APIRouter(prefix='/dashboard',tags=['dashboard'])
@router.get('/kpis')
def kpis(db:Session=Depends(get_db),_user:User=Depends(get_current_user)):
 return {'total_transactions':db.query(Transaction).count(),'alerts':db.query(FraudAlert).count(),'high_risk_transactions':0,'transaction_volume':db.query(func.coalesce(func.sum(Transaction.amount),0)).scalar() or 0}
@router.get('/trends')
def trends(_user:User=Depends(get_current_user)): return []
@router.get('/risk-distribution')
def risk_distribution(_user:User=Depends(get_current_user)): return [{'risk_level':r.value,'count':0} for r in RiskLevel]
