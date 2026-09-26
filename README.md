# FraudShield AI

Intelligent online transaction fraud detection and real-time monitoring system. B.Tech final year academic prototype.

## Days 1–5
- ML preprocessing, training, risk engine and SHAP explainability.
- FastAPI + SQLAlchemy + JWT/RBAC prediction backend.
- Dashboard analytics and alerts.
- React/Vite/Tailwind/Recharts dashboard.
- Day 5: JWT-authenticated Socket.IO events, six-scenario simulator, transaction investigation/SHAP panel, admin user management and audit logs.

## Quick start
See the docs for setup. Backend requires `pip install -r backend/requirements.txt`; frontend requires `npm install`.
Run `uvicorn app.main:app --reload` from `backend/` and `npm run dev` from `frontend/`.

The trained model in the development bundle uses the synthetic proxy dataset until the real ULB Kaggle CSV is placed in `ml/data/raw/creditcard.csv` and `ml/src/train.py` is rerun.
