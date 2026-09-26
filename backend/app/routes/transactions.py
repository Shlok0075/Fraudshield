from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models import Transaction, User
from app.schemas import TransactionOut, TransactionPredictRequest, TransactionPredictResponse
from app.services.prediction_service import ModelNotTrainedError, create_transaction_with_prediction
from app.services.realtime import emit_alert_created, emit_transaction_created

router=APIRouter(prefix="/transactions",tags=["transactions"])

@router.post("/predict",response_model=TransactionPredictResponse,status_code=status.HTTP_201_CREATED)
async def predict_transaction(payload:TransactionPredictRequest,db:Session=Depends(get_db),_user:User=Depends(get_current_user)):
    try:
        txn,prediction=create_transaction_with_prediction(db,payload.features,payload.merchant_id,payload.device_id)
    except ModelNotTrainedError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail=f"Fraud model not available: {e}") from e
    await emit_transaction_created(txn,prediction)
    if txn.alert is not None:
        await emit_alert_created(txn.alert)
    return TransactionPredictResponse(transaction=TransactionOut.model_validate(txn),prediction=prediction)

@router.get("",response_model=list[TransactionOut])
def list_transactions(skip:int=0,limit:int=50,db:Session=Depends(get_db),_user:User=Depends(get_current_user)):
    txns=db.query(Transaction).order_by(desc(Transaction.created_at)).offset(skip).limit(min(limit,200)).all()
    return txns

@router.get("/{transaction_id}",response_model=TransactionOut)
def get_transaction(transaction_id:str,db:Session=Depends(get_db),_user:User=Depends(get_current_user)):
    txn=db.get(Transaction,transaction_id)
    if txn is None: raise HTTPException(status_code=404,detail="Transaction not found")
    return txn
