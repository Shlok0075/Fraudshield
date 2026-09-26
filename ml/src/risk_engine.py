from enum import Enum
class RiskLevel(str,Enum): LOW='low'; MEDIUM='medium'; HIGH='high'; CRITICAL='critical'
def probability_to_risk(p): return RiskLevel.LOW if p<.25 else RiskLevel.MEDIUM if p<.5 else RiskLevel.HIGH if p<.75 else RiskLevel.CRITICAL
def risk_to_action(risk): return {'low':'allow','medium':'flag','high':'challenge','critical':'block'}[risk.value]
