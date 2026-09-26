import json
from sqlalchemy.orm import Session
from app.models import AuditLog

def write_audit(db: Session, actor_id: str | None, action: str, entity_type: str, entity_id: str, details: dict | None = None):
    row = AuditLog(
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=json.dumps(details or {}),
    )
    db.add(row)
    return row
