from app.models import RiskLevel
from ml.src.risk_engine import probability_to_risk,risk_to_action
def test_risk_regression():
    assert probability_to_risk(0.01)==RiskLevel.LOW
    assert probability_to_risk(0.99)==RiskLevel.CRITICAL
    assert risk_to_action(RiskLevel.CRITICAL)=='block'
