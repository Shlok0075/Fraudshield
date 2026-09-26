# FraudShield AI

Intelligent online transaction fraud detection and real-time monitoring system — B.Tech final-year academic prototype.

## Stack
- Backend: FastAPI, SQLAlchemy, JWT/RBAC, Socket.IO
- Frontend: React, Vite, Tailwind CSS, Recharts
- ML: Python, scikit-learn/XGBoost, SHAP workflow
- Development database: SQLite by default; PostgreSQL can be supplied through `DATABASE_URL`

## Project structure
```text
backend/             FastAPI API, auth, database, alerts
frontend/            React/Vite dashboard
ml/                  ML and risk-engine code
scripts/             Transaction simulator
docs/                Report, demo and viva material
.github/workflows/   GitHub Actions CI
```

## Requirements
- Python 3.11+
- Node.js 20+ and npm
- Git

## Run locally

### 1. Clone
```bash
git clone https://github.com/Shlok0075/Fraudshield.git
cd Fraudshield
```

### 2. Backend

#### Windows PowerShell
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

#### macOS/Linux
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

### 3. Backend environment
Local defaults in `.env` are:
```env
DATABASE_URL=sqlite:///./fraudshield.db
JWT_SECRET=replace-with-a-long-random-secret
CORS_ORIGINS=["http://localhost:5173"]
```
For production, use a strong random `JWT_SECRET` and a production database.

### 4. Start the backend
Run from `backend/`:
```bash
uvicorn app.main:app --reload --port 8000
```
Then open:
- API: http://localhost:8000
- Health: http://localhost:8000/health
- Swagger: http://localhost:8000/docs

### 5. Start the frontend
Open a second terminal from the project root:
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

The frontend defaults to `http://localhost:8000`. To change it, create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

### 6. Create a user
Open http://localhost:8000/docs and use `POST /auth/register`.
Example:
```json
{
  "email": "admin@example.com",
  "password": "Admin@123",
  "full_name": "FraudShield Admin",
  "role": "admin"
}
```
Then log in at http://localhost:5173.

### 7. Test the API
```bash
curl http://localhost:8000/health
```
Use Swagger's **Authorize** button with your bearer token to test protected endpoints.

### 8. Run the transaction simulator
The simulator supports `normal`, `suspicious`, `high-value`, `rapid`, `new-device`, and `unusual-location` scenarios.
Install `requests` if needed:
```bash
pip install requests
```
From the project root:
```bash
python scripts/simulator.py --api http://localhost:8000 --token YOUR_JWT_TOKEN --scenario all
```
Examples:
```bash
python scripts/simulator.py --api http://localhost:8000 --token YOUR_JWT_TOKEN --scenario high-value
python scripts/simulator.py --api http://localhost:8000 --token YOUR_JWT_TOKEN --scenario suspicious --count 5
```

### 9. Run tests
```bash
cd backend
pytest -q
python -m compileall app tests
```
GitHub Actions CI is defined in `.github/workflows/ci.yml`.

### 10. Build frontend
```bash
cd frontend
npm install
npm run build
npm run preview
```

## ML dataset
The intended academic dataset is the ULB Credit Card Fraud Detection dataset. Place the real CSV at:
```text
ml/data/raw/creditcard.csv
```
Development verification used a synthetic proxy when the real CSV was unavailable. Final academic metrics should be regenerated with the real dataset.

## Production deployment
Backend deployment files: `backend/Dockerfile` and `render.yaml`.
Frontend deployment: Vercel or another static host.
Set production environment variables:
```env
DATABASE_URL=<production-database-url>
JWT_SECRET=<long-random-secret>
CORS_ORIGINS=["https://your-frontend-domain.example"]
VITE_API_URL=https://your-backend-domain.example
```
Use HTTPS for the application and WSS for production Socket.IO connections.

## Main features
- Transaction risk prediction and risk levels: low, medium, high, critical
- Actions: allow, flag, challenge, block
- SHAP-style investigation/explanation workflow
- JWT authentication and RBAC
- Rate limiting/security headers
- Real-time Socket.IO transaction and alert events
- Alert lifecycle and audit logs
- React dashboard with KPIs, charts and investigation views
- Six-scenario transaction simulator

## Demo flow
```text
Login → Dashboard → Run simulator → Live transaction/alert
→ Open high-risk transaction → Review explanation
→ Update alert → Review audit log
```

## Documentation
- `docs/day_log.md` — development timeline
- `docs/day6.md` — security/testing/deployment
- `docs/day7.md` — finalization
- `docs/final_report.md` — condensed report
- `docs/demo_script.md` — demo sequence
- `docs/viva_questions.md` — viva preparation

## Security
Never commit `.env`, secrets, API keys, private datasets, `node_modules/`, virtual environments, or generated model binaries. Use `.env.example` for configuration.

## Academic disclaimer
FraudShield AI is an academic prototype. A production payment-fraud system would additionally require model calibration, drift monitoring, observability, high availability, load testing, incident response and applicable security/compliance controls.