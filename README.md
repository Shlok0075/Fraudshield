# FraudShield AI

Intelligent online transaction fraud detection and real-time monitoring system. Academic prototype built across a 7-day plan. Days 1-4 are included in this repository.

## Structure
- `ml/` preprocessing, training, prediction, risk engine, explainability and model artifacts
- `backend/` FastAPI API, JWT authentication, SQLAlchemy models and dashboard/alerts routes
- `frontend/` React + Vite + Tailwind + Recharts dashboard shell
- `docs/` architecture, requirements, model card and day logs

## Important
The bundled model artifacts were trained on the synthetic proxy dataset because the real ULB Kaggle CSV was not available in the build environment. Re-run `python ml/src/train.py` after placing the real dataset at `ml/data/raw/creditcard.csv`.
