"""Socket.IO event hub for post-commit real-time updates."""
import socketio

from app.auth.security import InvalidTokenError, decode_access_token
from app.config.settings import settings

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.cors_origins,
)

@sio.event
async def connect(sid, environ, auth):
    token = (auth or {}).get("token") if isinstance(auth, dict) else None
    if not token:
        return False
    try:
        decode_access_token(token)
    except InvalidTokenError:
        return False
    await sio.save_session(sid, {"authenticated": True})

@sio.event
async def disconnect(sid):
    return None

async def emit_transaction_created(transaction, prediction):
    await sio.emit("transaction_created", {
        "transaction_id": transaction.id,
        "amount": transaction.amount,
        "risk_level": prediction.risk_level.value,
        "action": prediction.action,
        "probability": prediction.probability,
        "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
    })

async def emit_alert_created(alert):
    await sio.emit("alert_created", {
        "alert_id": alert.id,
        "transaction_id": alert.transaction_id,
        "status": alert.status.value,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
    })

async def emit_alert_updated(alert):
    await sio.emit("alert_updated", {
        "alert_id": alert.id,
        "transaction_id": alert.transaction_id,
        "status": alert.status.value,
        "assigned_to": alert.assigned_to,
        "updated_at": alert.resolved_at.isoformat() if alert.resolved_at else None,
    })
