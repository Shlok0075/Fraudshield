# Day 5 — Real-time + Investigation + Admin

- JWT-authenticated Socket.IO ASGI server.
- `transaction_created`, `alert_created`, and `alert_updated` events.
- No polling for live dashboard updates.
- Persistent `audit_logs` table and audit service.
- Admin user status/role management and audit-log endpoint.
- Transaction investigation page with SHAP explanation.
- Six simulator scenarios: normal, suspicious, high-value, rapid, new-device, unusual-location.
- Alert actions: reviewed, false positive, escalate, resolve.

Verification: Python source compilation passed. Frontend build requires npm install in a normal networked environment.
