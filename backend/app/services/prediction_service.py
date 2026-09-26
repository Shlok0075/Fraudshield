import json
from app.models import FraudAlert,FraudPrediction,RiskLevel,Transaction
from app.schemas import PredictionOut,RawTransactionFeatures
class ModelNotTrainedError(Exception): pass
def _risk(p): return RiskLevel.LOW if p<.25 else RiskLevel.MEDIUM if p<.5 else RiskLevel.HIGH if p<.75 else RiskLevel.CRITICAL
def create_transaction_with_prediction(db,features:RawTransactionFeatures,merchant_id=None,device_id=None):
 amount=float(features.Amount); mag=sum(abs(getattr(features,f'V{i}')) for i in range(1,29))/28; p=max(.001,min(.999,.05+.00002*amount+.01*min(mag,20))); risk=_risk(p); action={'low':'allow','medium':'flag','high':'challenge','critical':'block'}[risk.value]
 explanation=sorted([{'feature':f,'shap_value':float(getattr(features,f)),'direction':'risk' if getattr(features,f)>=0 else 'protective'} for f in [f'V{i}' for i in range(1,29)]],key=lambda x:abs(x['shap_value']),reverse=True)[:5]
 txn=Transaction(amount=amount,merchant_id=merchant_id,device_id=device_id,raw_features=features.model_dump_json());db.add(txn);db.flush();pred=FraudPrediction(transaction_id=txn.id,probability=p,risk_level=risk,action=action,escalated_for_amount=amount>=5000,explanation_json=json.dumps(explanation),model_version='development-heuristic');db.add(pred)
 if risk in {RiskLevel.HIGH,RiskLevel.CRITICAL} or amount>=5000: db.add(FraudAlert(transaction_id=txn.id))
 db.commit();db.refresh(txn);return txn,PredictionOut.model_validate(pred)
