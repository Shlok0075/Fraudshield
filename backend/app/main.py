from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import ASGIApp
from app.config.settings import settings
from app.database.session import Base, engine
from app.routes import auth, transactions, dashboard, alerts, admin
from app.services.realtime import sio

@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

fastapi_app = FastAPI(title="FraudShield AI", description="Intelligent online transaction fraud detection — academic prototype.", version="0.5.0", lifespan=lifespan)
fastapi_app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@fastapi_app.get("/health", tags=["meta"])
def health():
    return {"status":"ok"}

fastapi_app.include_router(auth.router)
fastapi_app.include_router(transactions.router)
fastapi_app.include_router(dashboard.router)
fastapi_app.include_router(alerts.router)
fastapi_app.include_router(admin.router)
app = ASGIApp(sio, other_asgi_app=fastapi_app)
