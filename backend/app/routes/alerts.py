from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.models import AlertStatus, FraudAlert, User, UserRole
from app.schemas import AlertOut, AlertStatusUpdate
from app.services.audit import write_audit
from app.services.realtime import emit_alert_updated

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("", response_model=list[AlertOut])
def list_alerts(status_filter: AlertStatus | None = None, limit: int = 100, db: Session = Depends(get_db), _user: User = Depends(get_current_user)):
    q = db.query(FraudAlert).order_by(desc(FraudAlert.created_at))
    if status_filter: q = q.filter(FraudAlert.status == status_filter)
    return q.limit(min(limit, 200)).all()

@router.patch("/{alert_id}/status", response_model=AlertOut)
async def update_alert_status(alert_id: str, payload: AlertStatusUpdate, db: Session = Depends(get_db), user: User = Depends(require_role(UserRole.ADMIN, UserRole.ANALYST)):
    alert = db.get(FraudAlert, alert_id)
    if not alert: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    alert.status = payload.status
    alert.notes = payload.notes
    alert.assigned_to = user.id
    if payload.status in {AlertStatus.RESOLVED, AlertStatus.FALSE_POSITIVE}: alert.resolved_at = datetime.now(timezone.utc)
    else: alert.resolved_at = None
    write_audit(db, user.id, payload.status.value, "alert", alert.id, {"transaction_id": alert.transaction_id, "notes": payload.notes})
    db.commit(); db.refresh(alert)
    await emit_alert_updated(alert)
    return alert
