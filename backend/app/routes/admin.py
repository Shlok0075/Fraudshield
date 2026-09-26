from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.auth.dependencies import require_role
from app.database.session import get_db
from app.models import AuditLog, User, UserRole
from app.schemas import AdminUserUpdate, AuditLogOut, UserOut
from app.services.audit import write_audit

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _admin: User = Depends(require_role(UserRole.ADMIN))):
    return db.query(User).order_by(desc(User.created_at)).limit(200).all()

@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(user_id: str, payload: AdminUserUpdate, db: Session = Depends(get_db), admin: User = Depends(require_role(UserRole.ADMIN))):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if payload.role is not None: user.role = payload.role
    if payload.is_active is not None: user.is_active = payload.is_active
    write_audit(db, admin.id, "user_updated", "user", user.id, payload.model_dump(exclude_none=True))
    db.commit(); db.refresh(user)
    return user

@router.get("/audit-logs", response_model=list[AuditLogOut])
def audit_logs(db: Session = Depends(get_db), _admin: User = Depends(require_role(UserRole.ADMIN))):
    return db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(200).all()
